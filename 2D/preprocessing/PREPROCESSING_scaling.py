from pathlib import Path
import pandas as pd
import numpy as np
from PREPROCESSING_splitting import get_number

def get_sample_dfs(samples_folder_path, sample_number):
    ## returns the input and output dataframe for the sample specified
    
    input_folder_path = Path(samples_folder_path, 'input')
    output_folder_path = Path(samples_folder_path, 'output')
    
    glob_string = "*_" + str(sample_number) + ".csv"
    
    input_sample_glob = input_folder_path.glob(glob_string)
    
    for i, sample_input_file in enumerate(input_sample_glob):
        if i == 0:
            sample_input_df = pd.read_csv(sample_input_file, index_col = 0)
        else:
            raise Exception('error: more than one input sample with label' + str(sample_number))
    
    output_sample_glob = output_folder_path.glob(glob_string)
    
    for i, sample_output_file in enumerate(output_sample_glob):
        if i == 0:
            sample_output_df = pd.read_csv(sample_output_file, index_col = 0)
        else:
            raise Exception('error: more than one output sample with label' + str(sample_number))
    
    return sample_input_df, sample_output_df
    
def sample_iterator(samples_folder_path):
    ## generates dataframes for each of the samples in the samples folder
    
    input_folder_path = Path(samples_folder_path, 'input')
    output_folder_path = Path(samples_folder_path, 'output')
    
    glob_string = "*.csv"
    
    ## gets all input files
    input_sample_glob = input_folder_path.glob(glob_string)
    
    for input_sample in input_sample_glob:
        sample_number = get_number(input_sample.name)
        input_data, output_data = get_sample_dfs(data_folder_path, sample_number)
        yield sample_number, input_data, output_data
        
def get_max_disp_force(samples_folder_path):
    ## iterates through all data to get the max force and displacement
    samples = sample_iterator(samples_folder_path)
    
    max_force = 0
    max_disp = 0
    
    for sample in samples:
        sample_number, input_data, output_data = sample
        
        ## run through input data for displacement and force
        # first absolute, then max in the columns, then max over the three directions 
        updated = False
        max_force_temp = (input_data.loc[:,['x_force','y_force','z_force']].abs().max()).max()
        if max_force_temp > max_force:
            max_force = max_force_temp
            updated = True
            
        max_disp_temp = (input_data.loc[:,['x_disp','y_disp','z_disp']].abs().max()).max()
        if max_disp_temp > max_disp:
            max_disp = max_disp_temp
            updated = True
            
        ## run through output data for displacement
        max_disp_temp = (output_data.loc[:,['x_disp','y_disp','z_disp']].abs().max()).max()
        if max_disp_temp > max_disp:
            max_disp = max_disp_temp
            updated = True
            
        if updated:
            print(f'UPDATED MAX \t sample #{sample_number} \t force: {max_force:.2f} \t displacement: {max_disp:.6f} ')
            
    return max_force, max_disp
    
def scale_dataframe(df_unscaled, max_force, max_disp):
    df = df_unscaled.copy()
    
    try: 
        df.loc[:,['x_disp','y_disp','z_disp']] = df.loc[:,['x_disp','y_disp','z_disp']].values/max_disp
    except:
        raise Exception('error: displacement data error during scaling. Check sample')
    
    ## handle the error that happens when it's an output because it doesnt force columns
    try: 
        df.loc[:,['x_force','y_force','z_force']] = df.loc[:,['x_force','y_force','z_force']].values/max_force
    except:
        pass
    
    return df