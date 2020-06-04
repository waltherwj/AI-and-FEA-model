# README

This folder contains the scripts and notebooks used for preprocessing the data. They are all labelled `PREPROCESSING_<action>`. They act as helper modules to process  the data when called from a notebook or command line.

## _splitting

This module's intent is to get the raw data output from ANSYS and format it into .csv files named `input_<number>`, corresponding to boundary conditions of the sample `<number>` and `output_<number>`, corresponding to the solution displacement data from sample `<number>`.

#### .get_number(_str filename_)

This function takes a string and extracts the first contiguous integer in it, returning it as a string. It uses a regular expression to do so. If it doesn't find a number, it returns the string `no number found`.

#### .get_named_selections(_Path sample_path_)

This function takes a `pathlib.Path` object  and returns a `list` containing all the files that correspond to `glob("named_selection_*.txt")` 

`sample_path` is expected to be the path to the folder of of the sample.

#### .create_filename(_Path sample_path_)

This function takes a `pathlib.Path` object  and returns two  `pathlib.Path` objects `input_filename, output_filename ` of the format `<input>/<output>_<number>.csv`

`sample_path` is expected to be the path to the folder of of the sample.

#### .bc_files_to_df(_Path sample_folder_)

This function takes a `pathlib.Path` object  and three `pandas.Dataframe` objects `solutions_data, disp_bc_data, force_bc_data` of the format with  column headers `named_selection, unit,x_<disp>/<force>,y_<disp>/<force>,<disp>/<force>`. 

`sample_folder` is expected to be the path to the folder of of the sample. It is exactly the same as `sample_path` in the  other functions.

#### .selection_index(_str selection, pandas.Dataframe data_)

This function takes the arguments above, and runs through all the `data.named_selection` entries, comparing them to `selection`. Whenever it finds one that is exactly equal, it returns the row index of that entry on the dataframe.

#### .update_selection(_Path sample_folder, pandas.Dataframe disp_data, pandas.Dataframe force_data_)

This is a generator function that, given the arguments above, returns relevant data for each of the named selections in the sample folder. `sample_folder` is expected to be the path to the folder of of the sample. It is exactly the same as `sample_path` in the  other functions.

It returns `ns_number, ns, is_disp, is_force, values`. They are described below:

`ns_number` is an integer that corresponds to the number of the named selection

`ns` is a pandas.Dataframe object with column names  `node_number, x_loc, y_loc, z_loc` which contains the node numbers corresponding to the current named selection

`is_disp` and `is_force` are booleans that determine whether the named selection is for a force or for a displacement

`values` is a list containing the (x,y,z) components of  the selection, whether a force or a displacement

#### .create_input_df(_Path sample_folder_)

Takes the `sample_folder` path  and creates a `pandas.Dataframe` object with columns `node_number, named_selection,x_loc, y_loc, z_loc, x_disp, y_disp, z_disp,x_force, y_force, z_force`, with its `node_number` and nodal coordinate columns filled with relevant data for the sample, `named_selection` filled with `-1` and all the other columns filled with zeros, and returns that dataframe.

#### .update_df_with_ns(_pandas.Dataframe df, Int ns_number, pandas.Dataframe ns, bool is_disp, Bool is_force, list values_)

Takes the outputs from `.update_selection()` and `.create_input_df()`(refer to those functions for an explanation of their their output values/this function's arguments) and updates the general boundary condition dataframe with the values from the specified named selection, returning the updated dataframe.

#### .write_input_output(_Path sample_path, Path data_folder_path_)

Takes the path objects to the sample `sample_path`, and the path where the new files are going to be created `data_folder_path_`, and using the other functions write both the boundary conditions file `input_<number>.csv`, and the file with the solutions from ansys `output_<number>.csv`

#### .create_folders(_Path data_directory_path_)

Takes the directory ` data_directory_path`where the input and output files are going to be created, creates the folder `input` and `output` if they don't exist there, and returns two `pathlib.Path` objects `input_path, output_path` that point to those folders.

#### .delete_malformed_samples(_Generator all_samples_glob_)

Takes a generator `all_samples_glob` which is expected to generate `pathlib.Path` objects pointing to each of the sample directories, and deletes every directory for which the solutions file is somehow malformed and doesn't have the correct number of  columns. This happens because of some solve errors in ANSYS, but is somewhat rare.

#### .split_data(_Path all_samples_path, Path data_folder_path_) 

Takes two `pathlib.Path` objects and splits all the data in all the `all_samples_path` directory into input and output files inside of the `data_folder_path` directory. This function uses all other functions in the script, and by running it the function of this script is fulfilled.

## _scaling

This modules purpose is to get the data that the `_splitting` module creates and scale it to a range that can be more successfully/stably used by a neural network: [-1,1]

#### .get_sample_dfs(_Path samples_folder_path, Int sample_number_)

Takes the path  of the directory with the two folders created by `.create_folders()` and the number of a sample, and outputs two `pandas.Dataframe` objects, `sample_input_df, sample_output_df` containing the inputs and outputs of that sample.

#### .sample_iterator(_Path samples_folder_path_)

Takes the path  of the directory with the two folders created by `.create_folders()` and outputs a generator object that yields `sample_number, input_data, output_data`, respectively, a string with the sample number of the current sample, and the two dataframes that are the output of the `.get_sample_dfs()` function.

#### .get_max_disp_force(_Path samples_folder_path_)

Takes the path  of the directory with the two folders created by `.create_folders()` and returns the maximum force and displacement of the entire dataset as two floats `max_force, max_disp`

#### .scale_dataframe(_pandas.Dataframe df_unscaled, Float max_force, Float max_disp_)

Takes a `pandas.Dataframe` and two floats `max_force`, `max_disp` and divides the correct columns of the dataframe by these two floats, scaling them. If the two values `max_force` and `max_disp` come from the `get_max_disp_force` function then it is guaranteed that the resulting columns are going to be in the range [-1,1], however it will work if other values are provided as well. 

