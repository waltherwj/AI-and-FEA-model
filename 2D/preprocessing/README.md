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

- *NOTE: deprecated for the scaling function in the _formatting module*

Takes a `pandas.Dataframe` and two floats `max_force`, `max_disp` and divides the correct columns of the dataframe by these two floats, scaling them. If the two values `max_force` and `max_disp` come from the `get_max_disp_force` function then it is guaranteed that the resulting columns are going to be in the range [-1,1], however it will work if other values are provided as well. 

## _formatting

This module's purpose is to get the dataframes created by the _scaling module and transform them in arrays usable by a convolutional network.

#### .create_array(_int dimensionality, int features, int resolution = 32_)

Takes the arguments and returns a numpy array of shape `resolution X resolution X resolution(as many times as dimensionality) X features` filled with zeros.

#### _class_ HiddenPrints

Class used via the 'with' command to block any prints called inside of the functions inside of the with: block.

#### .get_max_dimensions(_pathlib.Path samples_folder_path_)

Takes a folder samples_folder_path containing both input and output folders with the raw data, and returns the maximum  dimensions of the elements in that database.

#### .get_element_size(_pathlib.Path sample_folder_path, int resolution = 32_)

Takes a folder samples_folder_path containing both input and output folders with the raw data, and returns the equivalent size of one element inside of tensor with spatial dimensions represented by `resolution` entries  in each direction, based on the max dimensions of  that raw data, so that every sample can fit inside of the tensor.

#### .get_quadrant(_pandas.Dataframe sample_df_)

Takes a dataframe `sample_df` and returns what octant that element was primarily created in. It doesn't require the element to be entirely in one octant, and it can handle both 2d and 3d cases. If the element wasn't created in a particular octant, it returns a vector that points to the octant where the element has the highest absolute values.

#### .translate_df(_pandas.Dataframe sample_df, tuple max_dimensions_)

Takes the raw data from `sample_df` and a tuple or equivalent that can be unpacked with `max(*max_dimensions)` and uses these values to translate the raw dataframe values so that the element is  spatially  positioned within the first quadrant. It first "pushes" the element on one of the corners of a bounding box of dimensions `max(*max_dimensions)` in the `positive x positive` (2D) or  `positive x positive x positive` (3D) , the corner being chosen based on what quadrant is returned by `.get_quadrant()` of the raw dataframe. The element also receives some fine adjustment to make sure it is in fact inside of the tensor's space even if it wasn't created all in one octant. 

Returns the translated dataframe.

#### .interpolate_array_spatially_2D(_pandas.Dataframe sample_array_)

Takes an array of dimensions [32, 32, 1] and convolves it with a 5x5 gaussian blur kernel. Returns the convolved array of same dimensions.

#### .convolve_with_kernel(_pandas.Dataframe sample_array, str kernel_name = 'edge_detection'_)

Takes an array of dimensions [32, 32, 1] and convolves it with a 3x3 kernel selected through `kernel_name`. As of yet, only `'edge_detection'` has been implemented.

#### .create_concat_array(_pandas.Dataframe sample_df, numpy.array empty_array, float element_size, str dataframe_type_)

Takes a `sample_df`, and a numpy array `empty_array` of the correct  dimension filled with zeros, and based on the `element_size` variable, and what type of dataframe it is (`'input'` or `'output'`), iterates through the dataframe and fills a copy of  the empty array with correct values.  Returns the filled array.

#### .get_unscaled_arrays(_pathlib.Path data_folder_path, int resolution = 32_)

This generator function takes a path `data_folder_path` to the folder containing the input and output folders with the raw dataframes, returning `sample_number, concatenated_input, concatenated_output`, which are, respectively, the number of the sample depending on file name, the array with seven features corresponding to `material existence, x_displacement, y_displacement, z_displacement, x_force, y_force, z_force` (the inputs/boundary conditions) and another array with 4 features corresponding to `material existence, x_displacement, y_displacement, z_displacement` (the outputs/results of the simulation)

#### .save_arrays(_Iterator array_iterator,pathlib.Path save_path, str array_type = 'unscaled'_)

Takes an iterator that returns sample numbers and arrays as the `.get_unscaled_arrays()` function does, and a `array_type` of either `'unscaled'` or `'scaled'` and  saves each of the arrays in the iterator to the folders `<input>` and `<output>` created at the `save_path` location. Also writes a log file to that location to record the time it took and if the file was created or  overwritten.

#### .saved_array_iterator(_pathlib.Path array_folder_path, str glob_parameter = '*.npy'_)

Takes the `array_folder_path` that is  expected to contain the  `<input>` and `<output>` folders created by the `.save_arrays()` function and creates an iterator that returns `sample_number, input_array, output_array`. 

Only gets the arrays that match the `glob_parameter` in a pathlib.Path.glob statement.

#### .get_max_array(_pathlib.Path array_folder_path, str glob_parameter = '*.npy'_)

Takes  the folder `array_folder_path` that is  expected to contain the  `<input>` and `<output>` folders created by the `.save_arrays()` function and iterates through all samples to find the maximum absolute force and displacements in the inputs and outputs alike. Returns `max_disp, max_forcce`

#### .create_scaled_arrays_iterator(_pathlib.Path array_folder_path, tuple max_values, glob_parameter = '*.npy'_)

Takes  the folder `array_folder_path` that is  expected to contain the  `<input>` and `<output>` folders created by the `.save_arrays()` function and iterates through all samples, scaling them based on the `max_disp, max_force` values contained  in the `max_values` variable, creates a batch dimension in the beggining of the tensor and moves the features dimension to be the second one. Thus, in 2d, it does `[resolution x resolution x features] -> [1 x features x resolution x resolution]`. Returns `sample_number, scaled_input_array, scaled_output_array`.