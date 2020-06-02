# README

This folder contains the scripts and notebooks used for preprocessing the data. They are all labelled `PREPROCESSING_<action>`. They act as helper modules to process  the data when called from a notebook or command line.

## _splitting

This module's intent is to get the raw data output from ANSYS and format it into .csv files named `input_<number>`, corresponding to boundary conditions of the sample `<number>` and `output_<number>`, corresponding to the solution displacement data from sample `<number>`.

#### .get_number(_str filename_)

This function takes a string and extracts the first contiguous integer in it, returning it as a string. It uses a regular expression to do so. If it doesn't find a number, it returns the string `no number found`.

#### .get_number(_str filename_)

This function takes a string and extracts the first contiguous integer in it, returning it as a string. It uses a regular expression to do so. If it doesn't find a number, it returns the string `no number found`.