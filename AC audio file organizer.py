## AC Audio File Organizer - by Andreisgl @ GitHub
# Refactoring by luisfilipels @ GitHub
# Manipulates the folder with audio files in order to organize each file to aid editing.

# Dependencies:
    # MFAudio

import os
import shutil
import subprocess
from enum import Enum


class ManipulateMode(Enum):
    CONVERT = 0
    REPRODUCE = 1


BASE_DIRECTORY = 'BGM'
METADATA_FOLDER = 'orgMeta'
MAIN_METADATA_FILE = 'mainMeta.txt'  # Contains the names of all audio files to be worked with
SAVE_FOLDER = 'Organizer Projects'
PROJECT_NAME = ''

MANIPULATE_MODE = ManipulateMode.CONVERT  # Mode for 'manipulateFile' function.

ACZ_RADIO_ARG_VALUES = [22050, 1, 320, 0, 'WAVU', 22050, 1, 320]  # Temporary. Argument value set for ACZ RADIOUSA files.
PARAMETER_LIST = ['CHARACTER', 'MISSION', 'ACESTYLE']  # This list stores all parameters that will be used to separate files. E.g: "CHARACTER", "MISSION"...

IS_NEW_PROJECT = True  # If this is a new project, create new lists. If not, retrieve saved files.

number_of_files = len(os.listdir(BASE_DIRECTORY))

file_list = []  # List of all filenames in 'basedir'.
file_data_list = []  # List of filenames and their metadata, which is generated by this script.
fdl_validation_index = [] # Contains which indexes of "file_data_list" are valid or not

save_file_list = 'FL.txt'  # File that stores the list 'FileList' to resume work later
save_file_data_list = 'FDL.txt'  # File that stores the list 'FileDataList' to resume work later


def manipulate_file(input_filename, output_filename, arg_values, mode):
    # Parameter list for function:
        # inputFilename - Name of file to be read.
        # outputFilename - Name of resulting file. Mandatory, but only really used if convert mode is selected ('mode' == 0).
        # arguValues - List of the values for the MFAudio arguments, minus input and output filenames, described below. Contais 8 indexes
        # mode - Selects function mode.
            # mode == 0: Convert audio
            # mode == 1: Reproduce audio

    # Argument list for MFAudio, with indexes for the lists used in this code
        # 0 -  /IFnnnnn	Input frequency
        # 1 -  /ICn	Input channels
        # 2 -  /IIxxxx	Input interleave (hex)
        # 3 -  /IHxxxx	Input headerskip (hex)
        # 4 -  /OTtttt	Output type (WAVU, VAGC,
        # 	            SS2U, SS2C, RAWU, RAWC)
        # 5 -  /OFnnnnn	Output frequency
        # 6 -  /OCn	Output channels
        # 7 -  /OIxxxx	Output interleave (hex)
        # 8 -  "InputFile"	Input file to play/convert
        # 9 -  "OutputFile"	Output file to convert to

    exe_filename = 'MFAudio.exe'

    bat_filename = 'temp.bat' # Temporary .bat file to execute MFAudio.exe (It only worked when I did this...)

    args = ['/IF', '/IC', '/II', '/IH', '/OT', '/OF', '/OC', '/OI'] #Contains the core arguments.
    current_arg_value = [] #The current set of argument VALUES currently being used.
    concat_args = [] #Concatenated Arguments and values
    argument_buffer = ''
    current_arg_value = arg_values

    for i in range(len(args)):  # Concatenates each core parameter with it's value individually, by list index.
        concat_args.append(args[i] + str(current_arg_value[i]))

    for i in range(len(args)):  # Creates string based on 'concatArgu' list contents.
        argument_buffer = argument_buffer + concat_args[i] + ' '

    argument_buffer = exe_filename + ' ' + argument_buffer + '"' + input_filename + '"' # Adds a input filename to 'argumentBuffer' string and...

    if mode == 0:  # ... if the mode is "Convert (0)", add output filename as well.
        argument_buffer = argument_buffer + ' ' + '"' + output_filename + '"'

    with open(bat_filename, 'w') as bat_file:
        bat_file.write(argument_buffer)

    subprocess.run(bat_filename)
    os.remove(bat_filename)




def init_project(): # Initializes project name and savefile stuff. MUST BE FIRST FUNCTION TO RUN!
    global IS_NEW_PROJECT
    global PROJECT_NAME
    global SAVE_FOLDER

    
    global number_of_files
    valid_input = False

    if not os.path.exists('./' + SAVE_FOLDER):
            os.mkdir('./' + SAVE_FOLDER)
    
    while not valid_input:
        answer = input('Open existing project? (y/n)')
        if answer == 'y' or answer == 'n': # If answer is valid
            if answer =='y':
                IS_NEW_PROJECT = False
                PROJECT_NAME = input("Input project name: ")
                
            else:
                IS_NEW_PROJECT = True
                PROJECT_NAME = input("Input NEW project name: ")
            valid_input = True
            
        else: # If answer is invalid
            valid_input = False
            print('Invalid Answer!')

    if IS_NEW_PROJECT:
        if not os.path.exists(SAVE_FOLDER + '/' + PROJECT_NAME):
            os.mkdir(SAVE_FOLDER + '/' + PROJECT_NAME)

        for f in os.listdir(BASE_DIRECTORY):
            file_list.append(f)

        with open(SAVE_FOLDER + '/' + PROJECT_NAME + '/' + save_file_list, 'w') as meta_file: # Store all filenames in metaFile
            meta_file.write(str(number_of_files) + '\n')
            for i in range(number_of_files):
                meta_file.write(file_list[i])
                if i < number_of_files - 1:
                    meta_file.write('\n')
        
        for i in range(number_of_files):
            file_data_list.append('')
    
    else:
        try:
            with open(SAVE_FOLDER + '/' + PROJECT_NAME + '/' + save_file_list) as SFL:
                number_of_files = int(SFL.readline().strip('\n'))

                for i in range(number_of_files):
                    file_list.append(SFL.readline().strip('\n'))

            with open(SAVE_FOLDER + '/' + PROJECT_NAME + '/' + save_file_data_list) as SFDL:

                for i in range(number_of_files):
                    file_data_list.append(SFDL.readline().strip('\n'))
        except FileNotFoundError:
            print('Project not found!')
            input('Press any key to exit...')
            exit('Project not found')
    

def save_project(): # Saves current project.
    global SAVE_FOLDER
    global PROJECT_NAME
    with open(SAVE_FOLDER + '/' + PROJECT_NAME + '/' + save_file_list, 'w') as sFL:
        sFL.write(str(number_of_files) + '\n')
        for i in range(len(file_list)):
            w = file_list[i] + '\n'
            sFL.write(w)
    with open(SAVE_FOLDER + '/' + PROJECT_NAME + '/' + save_file_data_list, 'w') as sFDL:
        for i in range(len(file_data_list)):
            w = file_data_list[i] + '\n'
            sFDL.write(w)
    print('Saving project...')
    input('Done! Press any key to continue...')

def work_on_files():
    for i in range(number_of_files):
        should_exit = False
        e = input('Press Enter to continue, or "exit" to exit...')
        if e == 'exit':
            should_exit = True
        if should_exit:
            print('Exiting...')
            should_exit = False
            break

        print('File: ' + file_list[i] + '\n')

        npath = BASE_DIRECTORY + '/' + file_list[i]
        # manipulate_file(npath, '', ACZ_RADIO_ARG_VALUES, 0)

        for g in PARAMETER_LIST:
            print('Input parameter ' + g + ': ')
            x = input()
            file_data_list[i] = file_data_list[i] + g + '.' + x + ','
        file_data_list[i] = file_data_list[i].rstrip(file_data_list[i][-1])

def fdl_parameter_parser(fdl_index): # Checks a file_data_list index and parse it's data.
    global PARAMETER_LIST
    parameter_ammount = len(PARAMETER_LIST)
    storage = []
    str_data = ''
    str_data = file_data_list[fdl_index]
    for i in range(parameter_ammount): # Define size of list
        storage.append('')
    for i in range(parameter_ammount):
        part_buffer = str_data.partition(',') # Separate arguments
        storage[i] = part_buffer[0]
        
        storage[i] = (storage[i].partition('.'))[2] # Separate value from argument
        str_data = part_buffer[2]
    return storage

def check_file_data_list(): # Checks 'save_file_data_list' and creates an index of files without parameters
    # Types of index values:
        # 0: No parameters or incomplete.
        # 1: Fully filled in.
    global fdl_validation_index # List of all indexes in filde_data_list
    parameter_value_buffer = [] # List of values for each parameter
    parameter_validation_buffer = [] # List of validation for individual parameters
    number_of_parameters = len(PARAMETER_LIST)
    
    for i in range(number_of_files): # Define list size
        fdl_validation_index.append('')
    for i in range(number_of_parameters): # Define list size
        parameter_validation_buffer.append('')
        parameter_value_buffer.append('')
   
    for i in range(number_of_files): # Check all files in file_data_list
        parameter_value_buffer = fdl_parameter_parser(i)
        for c in range(number_of_parameters): # Check data for all parameters in PARAMETER_LIST
            if not parameter_value_buffer[c]: # If this parameter is empty:
                parameter_validation_buffer[c] = 0
            else: # If parameter is NOT empty
                parameter_validation_buffer[c] = 1
        
        for j in range(number_of_parameters):
            if parameter_validation_buffer[j] != 1:
                fdl_validation_index[i] = 0
            else: fdl_validation_index[i] = 1


            




    


if not os.path.exists(BASE_DIRECTORY):  # Check if the folder to be accessed exists. If not, the program quits.
    print('File directory not found. Press any key to exit...')
    exit('Base directory not found')



init_project()
check_file_data_list()
# work_on_files()
save_project()