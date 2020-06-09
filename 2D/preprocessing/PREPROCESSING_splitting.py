## Imports necessary functions for the script
import os
from pathlib import Path
import traceback
import re
import pandas as pd
import numpy as np

def get_number(filename):
    # uses regular expression to match a single number in the file name
    try:
        return re.search(r'\d+', filename).group(0)
    except:
        return 'no number found'
        
def get_named_selections(sample_path):
    file_list = []
    # return all paths that correspond to a named selection
    for file in sample_path.glob("named_selection_*.txt"):
        file_list.append(file)
    return file_list
    
def create_filename(sample_path): 
    #creates a filename based on the sample number
    sample_number = get_number(sample_path.name)
    input_filename = Path("input_" + sample_number + '.csv' )
    output_filename = Path("output_" + sample_number + '.csv' )
    return input_filename, output_filename    
    
def bc_files_to_df(sample_folder):
    # creates three dataframes with the boundary conditions
    #load in solutions file
    solutions_file = sample_folder.glob("solutions_*.txt")
    for file in solutions_file:
        try:
            solutions_data = pd.read_csv(file, delimiter = '\t',
                     names = ['node_number', 'x_loc','y_loc','z_loc','x_disp','y_disp','z_disp'],
                     header=0)
        except Exception:
            print('File is not in the correct format', file)
            print("run delelete_malformed_samples() before running this")
            
    disp_file = sample_folder.glob("disp_*.txt")

    #load in displacement boundary conditions
    for file in disp_file:
        disp_bc_data = pd.read_csv(file, delimiter = '\t',
                     names = ['named_selection', 'unit','x_disp','y_disp','z_disp'],
                     header=None)

    #load in force boundary conditions
    force_file = sample_folder.glob("force_*.txt")
    for file in force_file:
        force_bc_data = pd.read_csv(file, delimiter = '\t',
                     names = ['named_selection', 'unit','x_force','y_force','z_force'],
                     header=None)
    
        
    return solutions_data, disp_bc_data, force_bc_data
    
def selection_index(selection, data):
    # runs through all named selections and returns the index
    # that corresponds to the selection name
    for i, ns_in_file in enumerate(data.named_selection.to_list()):
        if selection == ns_in_file:
            return i
    raise Exception('error: String \'' + selection +'\' not found in the rows of the data')
    
def update_selection(sample_folder, disp_data, force_data):
    # generator  function that returns all the relevant data for each of the
    # named selections in the folder
    
    named_selections = get_named_selections(sample_folder)
    
    ## Iterate Through Selections
    for ns_file in named_selections:

        ## Check selection type and get values for that selection
        is_disp = False
        selection_values_updated = False
        for selec in disp_data.named_selection:
  
            if get_number(selec) == get_number(ns_file.name):
                is_disp = True 
            
            if get_number(selec) == 'no number found' and get_number(ns_file.name) == '1':
                is_disp = True    
                
            if is_disp and not selection_values_updated:
                try:
                    ns_number = int(get_number(selec))
                    
                except:
                    ns_number = 1
 
                index =  selection_index(selec, disp_data)
                values = disp_data.x_disp.loc[index], disp_data.y_disp.loc[index], disp_data.z_disp.loc[index]
                selection_values_updated = True

        is_force = False
        selection_values_updated = False
        for selec in force_data.named_selection:
            
            if get_number(selec) == get_number(ns_file.name):
                is_force = True
                
            if get_number(selec) == 'no number found' and get_number(ns_file.name) == '1':
                is_force = True  
                
            if is_force and not selection_values_updated:
                try:
                    ns_number = int(get_number(selec))
                except:
                    ns_number = 1
                    
                index =  selection_index(selec, force_data)
                values = force_data.x_force.loc[index], force_data.y_force.loc[index], force_data.z_force.loc[index]
                selection_values_updated = True
       
        ## get named selection in the file
        ns = pd.read_csv(ns_file, delimiter = '\t',
                             names = ['node_number','x_loc','y_loc','z_loc'],
                             header=0,
                             usecols = range(4))
            
        yield ns_number, ns, is_disp, is_force, values
        
def update_df_with_ns(df, ns_number, ns, is_disp, is_force, values):
    ## updates the dataframe with a single named selection
    
    ns_list = ns.node_number.to_list()
    
    for i, node in enumerate(df.node_number.to_list()):
        if node in ns_list:
            #selects correct nodes

            df.loc[i,'named_selection'] = ns_number
            
            if is_disp:
                df.loc[i, 'x_disp'], df.loc[i, 'y_disp'], df.loc[i, 'z_disp'] = values
            if is_force:
                df.loc[i, 'x_force'], df.loc[i, 'y_force'], df.loc[i, 'z_force'] = values
    return df

def create_input_df(sample_folder):
    ## creates a dataframe with the correct columns and neutral values
    ## start empty dataframe
    df = pd.DataFrame(columns = ['node_number', 'named_selection' , 'x_loc','y_loc','z_loc',
                             'x_disp','y_disp','z_disp',
                            'x_force','y_force', 'z_force'])
    
    ##load in partial data into dataframes
    sol_data, disp_data, force_data = bc_files_to_df(sample_folder)
    
    ## start dataframe values 
    ## first fill dataframe nodes and coordinates
    df.node_number, df.x_loc, df.y_loc, df.z_loc = sol_data.node_number, sol_data.x_loc, sol_data.y_loc, sol_data.z_loc 


    ## fill rest of data with "neutral" values
    df.named_selection = np.ones_like(df.named_selection, dtype=int)*(-1)
    zero = np.zeros_like(df.named_selection, dtype = float)
    df.x_disp, df.y_disp, df.z_disp, df.x_force, df.y_force, df.z_force = zero, zero, zero, zero, zero, zero
    
    ##iterate through named selections
    selection_iterator = update_selection(sample_folder, disp_data, force_data)
    for selection in selection_iterator:
        df = update_df_with_ns(df, *selection)
    
    
    return df

def write_input_output(sample_path, data_folder_path):
    ## Writes the files corresponding to the sample to the output folder

    ## create the two  dataframes necessary for writing the files
    df_input = create_input_df(sample_path)
    df_output, _, _ = bc_files_to_df(sample_path)
    
    ## create the appropriate paths
    input_folder, output_folder = create_folders(data_folder_path)
    input_filename, output_filename = create_filename(sample_path)
    
    input_file_path = Path(input_folder, input_filename)
    output_file_path = Path(output_folder, output_filename)
    
    df_input.to_csv(input_file_path)
    df_output.to_csv(output_file_path)
    
def create_folders(data_directory_path):
    # creates the folders to split the data into input and output, and returns their path
    try:
        input_folder = Path('input')
        output_folder = Path('output')
        input_path = Path(data_directory_path, input_folder)
        output_path = Path(data_directory_path, output_folder)
        input_path.mkdir(parents = True)
        print(f'folder {input_path} created')
    except Exception:
        print(f"folder {input_path} likely already exist")
        #traceback.print_exc()
    
    try:
     
        output_path.mkdir(parents = True)
        print(f'folder {output_path} created')
    except:
        print(f"folder {output_path} likely already exist")
        #traceback.print_exc()
    
    return input_path, output_path
    
def delete_malformed_samples(all_samples_glob):
    #deletes folders that don't have the correct format
    
    for sample_folder in all_samples_glob:
        solutions_file = sample_folder.glob("solutions_*.txt")
        for file in solutions_file:
            try:
                solutions_data = pd.read_csv(file, delimiter = '\t',
                         names = ['node_number', 'x_loc','y_loc','z_loc','x_disp','y_disp','z_disp'],
                         header=0)
            except Exception:
                print('File is not in the correct format, deleting parent folder of', file)
                all_files = sample_folder.glob('*.txt')
                for file in all_files:
                    os.remove(file)
                os.rmdir(sample_folder)
                
def split_data(all_samples_path, data_folder_path):
    # runs all the other functions and separates the data into input and output files
    # for all samples inside of the samples directory by writing to the data_folder_path
    # directory
    
    all_samples_glob = all_samples_path.glob('data_dir_*')
    ##all samples_glob is exhausted in delete_malformed samples
    delete_malformed_samples(all_samples_glob)
  
    all_samples_glob = all_samples_path.glob('data_dir_*')    
        
    for sample in all_samples_glob:
        print(sample)
        write_input_output(sample, data_folder_path)
        
print('splitting functions imported')