import numpy as np
import PREPROCESSING_scaling as scale
import PREPROCESSING_splitting as split
from pathlib import Path
import pandas as pd
import os, sys
import torch.nn.functional as F
import torch
import datetime

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
    
def get_max_dimensions(samples_folder_path):
    ## iterates through all data to get the max dimensions
    samples = scale.sample_iterator(samples_folder_path)
    
    max_x = 0
    max_y = 0
    max_z = 0
    
    for sample in samples:
        sample_number, input_data, output_data = sample
        #print(samples)
        
        ## run through all data
        # first absolute, then max in the columns 
        updated = False
        
        ## get ranges of data in sample
        range_x = [input_data.loc[:,['x_loc']].max().item(), input_data.loc[:,['x_loc']].min().item()]
        max_x_temp = abs(range_x[0] - range_x[1])
        
        range_y = [input_data.loc[:,['y_loc']].max().item(), input_data.loc[:,['y_loc']].min().item()]
        max_y_temp = abs(range_y[0] - range_y[1])
        
        range_z = [input_data.loc[:,['z_loc']].max().item(), input_data.loc[:,['z_loc']].min().item()]
        max_z = abs(range_z[0] - range_z[1])
        
        max_y_temp, max_z_temp = input_data.loc[:,['y_loc','z_loc']].abs().max()
        
        if max_x_temp > max_x:
            max_x = max_x_temp
            updated = True
            
        if max_y_temp > max_y:
            max_y = max_y_temp
            updated = True
            
        if max_z_temp > max_z:
            max_z = max_z_temp
            updated = True
            
        if updated:
            print(f'UPDATED MAX \t sample #{sample_number} \t x: {max_x:.4f} \t y: {max_y:.4f} \t z: {max_z:.4f}')
            
    return max_x, max_y, max_z

    
def get_element_size(samples_folder_path, resolution = 32):
    ## runs through all samples to get the element size based on the resolution
    with HiddenPrints():
        max_x, max_y, max_z = get_max_dimensions(samples_folder_path)
    
    largest_dim = max([max_x, max_y, max_z])
   
    element_size = largest_dim/resolution
    
    return element_size
    
def get_quadrant(sample_df):
    ## gets the sample's main octant by returning a 3 component vector that points to that octant. 
    ## a zero in the last component means that it is a 2d problem and thus it points to a 2d 
    ## quadrant
    
    #gets the maximum absolute values
    max_x_abs, max_y_abs, max_z_abs = sample_df.loc[:,['x_loc','y_loc','z_loc']].abs().max()
    
    ## checks if 2d or 3d problem
    Is_2D = True
    if max_z_abs != 0:
        Is_2D = False
    ## get index of the maximum absolute values
    x_index = np.where(sample_df.loc[:,['x_loc']].abs().values.squeeze() == [max_x_abs])
    y_index = np.where(sample_df.loc[:,['y_loc']].abs().values.squeeze() == [max_y_abs])
    if not(Is_2D):
        z_index = np.where(sample_df.loc[:,['z_loc']].abs().values.squeeze() == [max_z_abs])
    else:
        z_index = [[0]]
        
    ## gets the value in that index
    values = np.array([sample_df.loc[x_index[0],['x_loc']].values[0][0],
                      sample_df.loc[y_index[0],['y_loc']].values[0][0],
                      sample_df.loc[z_index[0],['z_loc']].values[0][0]])
    
    ## create array with information about the octant via a vector
    octant = np.zeros(3)
    octant[0:2] =  values[0:2]/abs(values[0:2])
    if not(Is_2D):
        octant[2] = values[2]/abs(values[2])
    
    return octant
    
def  translate_df(sample_df, max_dimensions):
    ## gets a dataframe and translates the values to the correct position to place in the tensor
    
    octant = get_quadrant(sample_df)
    
    df_temp = sample_df.copy()
    largest_dim = max(*max_dimensions)
    
    ## general translation: translates according to the overall octant
    for i, direction in enumerate(octant):
        direction_is_negative = direction < 0
        if direction_is_negative:
            if i == 0:
                df_temp.loc[:,['x_loc']] = df_temp.loc[:,['x_loc']] + largest_dim - df_temp.loc[:,['x_loc']].max().item()
            if i == 1:
                df_temp.loc[:,['y_loc']] = df_temp.loc[:,['y_loc']] + largest_dim - df_temp.loc[:,['y_loc']].max().item()
            if i == 2:
                df_temp.loc[:,['z_loc']] = df_temp.loc[:,['z_loc']] + largest_dim - df_temp.loc[:,['z_loc']].max().item()
        
        ## minor translation: if some parts of the element are still "sticking out"
        ## after the general translation, move it just enough to ensure that it fits inside
        if not(direction_is_negative):
            min_val = df_temp.loc[:,['x_loc','y_loc', 'z_loc']].iloc[:, i].min()
            
            if min_val < 0.0:
                if i == 0:
                    df_temp.loc[:,['x_loc']] = df_temp.loc[:,['x_loc']] + abs(min_val)
                    #print('0',min_val)
                if i == 1:
                    df_temp.loc[:,['y_loc']] = df_temp.loc[:,['y_loc']] + abs(min_val)
                    #print('1',min_val)
                if i == 2:
                    df_temp.loc[:,['z_loc']] = df_temp.loc[:,['z_loc']] + abs(min_val)
                    #print('2',min_val)
    
    return df_temp
    
def interpolate_array_spatially_2D(sample_array):
    ## use gaussian blur kernel to smooth out the tensor
    
    ## define kernel
    kernel_blur = 1/256*torch.Tensor([[1, 4, 6, 4, 1],
                                [4, 16, 24, 16, 4],
                                [6, 24, 36, 24, 6],
                                [4, 16, 24, 16, 4],
                                [1, 4, 6, 4, 1]])
    
    ## add redundant batch_size and _feature dimensions because of torch requirements
    kernel_blur = kernel_blur.view([1,1,5,5])
    
    ## convert
    tensor = torch.from_numpy(sample_array)
    
    ## convolve filter and tensor
    smoothed_array = F.conv2d(input = tensor.view([1,1,32,32]), weight = kernel_blur.double(), stride = 1, padding=2)   
    
    ## return it as a correctly shaped numpy arra
    return smoothed_array.view([32,32,1]).numpy()
    
def convolve_with_kernel(sample_array, kernel_name='edge_detection'):
    ## use kernel on sample
    
    ## define kernel
    
    if kernel_name == 'edge_detection':
        kernel = torch.Tensor([[-1,-1,-1],
                              [-1,8,-1],
                              [-1,-1,-1]])
    
    ## add redundant batch_size and _feature dimensions because of torch requirements
    kernel = kernel.view([1,1,3,3])
    
    ## convert
    tensor = torch.from_numpy(sample_array)
    
    ## convolve filter and tensor
    convolved_array = F.conv2d(input = tensor.view([1,1,32,32]), weight = kernel.double(), stride = 1, padding=1)   
    
    ## return it as a correctly shaped numpy array
    return convolved_array.view([32,32,1]).numpy()
    
def create_concat_array(sample_df, empty_array, element_size, dataframe_type):
    ## takes a sample dataframe and creates the concatenated tensor with it
    
    ## initialize empty array copy
    concat_array = empty_array.copy()
    
    ## get resolution of array
    resolution = len(empty_array[0])

    ## check dimensionality of array
    if len(concat_array.shape) == 3:
        dimensionality = 2
        
    if len(concat_array.shape) == 4:
        dimensionality = 3

    ## create dictionary to store number of nodes for each array location
    nodes_dictionary = {}
    
    for i, row in enumerate(sample_df.itertuples()): #itertuples is much faster than iterrows
        ## get spacial locations
        x_loc, y_loc, z_loc = row.x_loc, row.y_loc, row.z_loc
        
        ## calculate tensor locations
        ## points at the very edge of an element at the edge of the array 
        ## should fall to the previous index, not to the next
        x = x_loc / element_size 
        y = y_loc / element_size 
        z = z_loc / element_size
        
        x,y,z = int(x), int(y), int(z)
        
        
        ## check for upper edge case
        if  x >= resolution:
            x -= 1
        if  y >= resolution:
            y -= 1
        if  z >= resolution:
            z -= 1
        
        
        ## create feature vector to update location
        if dataframe_type.lower() == 'input':
            feature_vector = np.array([1, row.x_disp, row.y_disp, row.z_disp, row.x_force, row.y_force, row.z_force])
            
        if dataframe_type.lower() == 'output':
            feature_vector = np.array([1, row.x_disp, row.y_disp, row.z_disp])
            
        elif dataframe_type.lower() != 'input':
            raise Exception(f'Incorrect dataframe type. Expected \'input\' or \'output\', got {dataframe_type}')
       
        ## update values at location
        if dimensionality == 2:
            
           
            try:
                 ## update material existence
                concat_array[x,y,0] = feature_vector[0]
                
                ## only do operation if there is a value to add
                if any(feature_vector[1:] != 0.0):
                    
                    if any(feature_vector[1:4] != 0.0):
                        ## add displacements
                        concat_array[x,y,1:4] += feature_vector[1:4]

                        ## add item to dictionary
                        ## control whether to create or update dictionary entry
                        if (x,y) in nodes_dictionary:
                            nodes_dictionary[(x,y)] +=1
                        else:
                            nodes_dictionary[(x,y)] = 1
                    
                    ## add forces if input
                    if dataframe_type.lower() == 'input':
                        concat_array[x,y,4:7] += feature_vector[4:7]
                
            except IndexError:
                print(f'out of bounds, check sample at x:{x_loc} y:{y_loc} z:{z_loc}, indices {x,y,z}')
               
            
            
        elif dimensionality > 2:
            raise Exception(f'Three dimensional or higher not implemented yet')
        
        
        
    ## divide the displacements by the number of nodes
    for key in nodes_dictionary.keys():
        #print(concat_array[*key,1], concat_array[*key,1]/nodes_dictionary[key])
        concat_array[(*key, [1,2,3])] = concat_array[(*key, [1,2,3])]/nodes_dictionary[key]
    
    
    ## smooth out material existence feature
    concat_array[:,:,0:1] = interpolate_array_spatially_2D(concat_array[:,:,0:1])
    return concat_array
    
def get_unscaled_arrays(data_folder_path, resolution = 32):
    ## takes the path to the folder with all samples and creates
    ## an iterator that goes through all of them and returns the corresponding
    ## array to each sample
    
    with HiddenPrints():
        # get max dimensions for the dataset
        max_dimensions = get_max_dimensions(data_folder_path)
    
    # get element size for this dataset
    element_size = get_element_size(data_folder_path, resolution)
    
    # create an iterator for all samples
    samples_iterator = scale.sample_iterator(data_folder_path)
    
    # create empty arrays to use in functions
    dimensionality = 2
    input_features = 7
    output_features = 4
    empty_arr_input = create_array(dimensionality, input_features, resolution)
    empty_arr_output = create_array(dimensionality, output_features, resolution)
    
    # iterates through all samples
    for sample_number, input_dataframe, output_dataframe in samples_iterator:
        
        
        # translate the data
        translated_input_df = translate_df(input_dataframe, max_dimensions)
        translated_output_df = translate_df(output_dataframe, max_dimensions)
        
        # creates the arrays
        concatenated_input = create_concat_array(translated_input_df, empty_arr_input, element_size, dataframe_type='input')
        concatenated_output = create_concat_array(translated_output_df, empty_arr_output, element_size, dataframe_type='output')
    
        yield sample_number, concatenated_input, concatenated_output
        
def save_arrays(array_iterator, save_path, array_type = 'unscaled'):
    # take the folder where the samples are and the folder where the samples are going to be
    # saved to, create the folder and save the arrays
    
    ## create save path
    save_path = Path(save_path, 'arrays')
    
    ## create save folders
    input_save_path, output_save_path = split.create_folders(save_path)
    
    #sample_number, input_array, output_array = next(array_iterator)
    
    if 'nscaled' in array_type.lower():
        input_file_root = array_type.lower()
        output_file_root = array_type.lower()
        
    elif 'scaled' in array_type.lower():
        input_file_root = array_type.lower()
        output_file_root = array_type.lower()
        
    else:
        raise Exception(f'Expected \'scaled\' or \'unscaled\' strings for argument <array_type>, got \'{array_type}\'')
        
    ## create log file
    log_file = Path(save_path,'log.txt')
    
    with open(log_file, mode = '+a') as log:
        log.write('\n' + str(datetime.datetime.now()) + '\n')
        log.write(f"{'SAMPLE': <20} {'INPUT': <20} {'OUTPUT': <20} {'PATH': <20} {'TIME': >40}\n")
        
        initial_time = time.time()
        for sample_number, input_array, output_array in array_iterator:
            tic = time.time()
            input_file_ending = '_input_' + str(sample_number) + '.npy'
            output_file_ending = '_output_' + str(sample_number) + '.npy'
            
            input_array_path = Path(input_save_path, input_file_root + input_file_ending)
            output_array_path = Path(output_save_path, output_file_root + output_file_ending)
            
  
            if not(input_array_path.is_file()) :
                action_input = 'CREATE'
            else:
                action_input = 'OVRWRT'
                
            if not(output_array_path.is_file()):
                action_output = 'CREATE'
            else:
                action_output = 'OVRWRT'
            
            np.save(input_array_path, input_array)
            np.save(output_array_path, output_array)
            
            
            log.write(f'{sample_number: <20} {action_input: <20} {action_output: <20} {str(save_path): <20} {time.time()-tic: >40}s \n')
        
        log.write(f'OVERALL TIME: {time.time()-initial_time}s \n')
        
def saved_array_iterator(array_folder_path, glob_parameter = '*.npy'):
    ## generates arrays for each of the saved arrays in the arrays folder
    
    input_array_folder_path = Path(array_folder_path,'input')
    output_array_folder_path = Path(array_folder_path,'output')
    
    ## gets array file iterator
    input_array_iterator = input_array_folder_path.glob(glob_parameter)
    output_array_iterator = output_array_folder_path.glob(glob_parameter)
    array_iterators = zip(input_array_iterator, output_array_iterator)
    
    ## iterate over array files
    for input_array_path, output_array_path in array_iterators:
        sample_number = get_number(input_array_path.name)
        
        input_array = np.load(input_array_path)
        output_array = np.load(output_array_path)
        
        yield sample_number, input_array, output_array
        
def get_max_array(array_folder_path, glob_parameter = '*.npy'):
    ##  takes a path and for all the files inside of the folder 
    ## input and output that match glob, rescale and reshape them
    
    # create array iterator
    array_iterator = saved_array_iterator(array_folder_path, glob_parameter)
        
    # initialize  displacemente and forces
    max_disp = 0
    max_force = 0
    updated = False
    
    ## open log file
    log_file = Path(array_folder_path,'log.txt')
    with open(log_file, 'a+') as log:
        log.write(f" UPDATE MAX VALUES \n")
        log.write(f"{'SAMPLE': <20} {'FORCE': <20} {'DISPLACEMENT': <20}\n")
        
        # iterate through all arrays updates max displacement and force
        for sample_number, unscaled_input_array, unscaled_output_array in array_iterator:
            # get sample max values
            max_disp_temp = max(np.abs(unscaled_input_array[:,:,1:4]).max(), np.abs(unscaled_output_array[:,:,1:4]).max())
            max_force_temp = np.abs(unscaled_input_array[:,:,4:7]).max()
            
            if max_disp_temp > max_disp:
                max_disp = max_disp_temp
                updated  = True
            
            if max_force_temp > max_force:
                max_force = max_force_temp
                updated  = True
            
            if updated:
                print(f'UPDATED MAX \t sample #{sample_number} \t force: {max_force:.5f} \t disp: {max_disp:.6f} ')
                log.write(f'{sample_number:<20} {max_force: <20} {max_disp: <20} \n')
                updated = False
    return max_disp, max_force   
    
def create_scaled_arrays_iterator(array_folder_path, max_values, glob_parameter = '*.npy'):
    #takes a file path and creates all the arrays scaled between -1 and 1, and shaped
    # correctly for the convolutional layers
    
    # create array iterator
    array_iterator = saved_array_iterator(array_folder_path, glob_parameter)
    
    # get max values
    max_disp, max_force = max_values
    
    for sample_number, unscaled_input_array, unscaled_output_array in array_iterator:
            
            scaled_input_array = unscaled_input_array.copy()
            scaled_output_array = unscaled_output_array.copy()
            
            scaled_input_array[:,:,1:4] = (unscaled_input_array[:,:,1:4]/max_disp)
            scaled_output_array[:,:,1:4] = (unscaled_output_array[:,:,1:4]/max_disp)
            scaled_input_array[:,:,4:7] = (unscaled_input_array[:,:,4:7]/max_force)
            
            #first move the features axis to be the first
            scaled_input_array = np.moveaxis(scaled_input_array, source = 2, destination = 0)
            scaled_output_array = np.moveaxis(scaled_output_array, source = 2, destination = 0)
      
            #add empty dimension at beggining of array
            scaled_input_array = np.expand_dims(scaled_input_array, axis = 0)
            scaled_output_array = np.expand_dims(scaled_output_array, axis = 0)
            
            yield sample_number, scaled_input_array, scaled_output_array
            
print('formatting functions imported')