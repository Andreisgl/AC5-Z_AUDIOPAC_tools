## AC Audio File Organizer - by Andreisgl @ GitHub
# Refactoring by luisfilipels @ GitHub
# Manipulates the folder with audio files in order to organize each file to aid editing.

# Dependencies:
    # MFAudio

## TODO:
# Please, for everything that is holy, simplify the folder path creation, future Andrei!
import os
import shutil
import subprocess
from enum import Enum


class ManipulateMode(Enum):
    CONVERT = 0
    REPRODUCE = 1


BASE_DIRECTORY = 'files'

EXTRACT_DIRECTORY = 'BGM'

MAIN_METADATA_FILE = 'mainMeta.txt'  # Contains the names of all audio files to be worked with
SAVE_FOLDER = 'Organizer Projects'
PROJECT_NAME = ''
WORK_FOLDER = 'Work'

MANIPULATE_MODE = ManipulateMode.CONVERT  # Mode for 'manipulateFile' function.

ACZ_RADIO_ARG_VALUES = [22050, 1, 320, 0, 'WAVU', 22050, 1, 320]  # Temporary. Argument value set for ACZ RADIOUSA files.
PARAMETER_LIST = ['CHARACTER', 'MISSION', 'ACESTYLE', "PHRASE"]  # This list stores all parameters that will be used to separate files. E.g: "CHARACTER", "MISSION"...

IS_NEW_PROJECT = True  # If this is a new project, create new lists. If not, retrieve saved files.

number_of_files = 0 # Contains number of files of current project

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

    DESTINATION_PATH = BASE_DIRECTORY

    args = ['/IF', '/IC', '/II', '/IH', '/OT', '/OF', '/OC', '/OI'] #Contains the core arguments.
    current_arg_value = [] #The current set of argument VALUES currently being used.
    concat_args = [] #Concatenated Arguments and values
    argument_buffer = ''
    current_arg_value = arg_values

    for i in range(len(args)):  # Concatenates each core parameter with it's value individually, by list index.
        concat_args.append(args[i] + str(current_arg_value[i]))

    for i in range(len(args)):  # Creates string based on 'concatArgu' list contents.
        argument_buffer = argument_buffer + concat_args[i] + ' '

    # Adds a input filename to 'argumentBuffer' string and...
    argument_buffer = exe_filename + ' ' + argument_buffer + '"' + DESTINATION_PATH + '\\'+ input_filename + '"'

    if mode == 0:  # ... if the mode is "Convert (0)", add output filename as well.
        argument_buffer = argument_buffer + ' ' + '"' + output_filename + '"'

    subprocess.Popen(argument_buffer)




def init_project(): # Initializes project name and savefile stuff. MUST BE FIRST FUNCTION TO RUN!
    global IS_NEW_PROJECT
    global PROJECT_NAME
    global SAVE_FOLDER
    global BASE_DIRECTORY
    global WORK_FOLDER
    

    
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
    
    PROJECT_NAME = SAVE_FOLDER + '/' + PROJECT_NAME
    BASE_DIRECTORY = PROJECT_NAME + '/' + BASE_DIRECTORY
    WORK_FOLDER = PROJECT_NAME + '/' + WORK_FOLDER

    if not os.path.exists(WORK_FOLDER):
        os.mkdir(WORK_FOLDER)
    
    if IS_NEW_PROJECT:
        
        if not os.path.exists(PROJECT_NAME):
            os.mkdir(PROJECT_NAME)
        else:
            print('Project already exists!')
            exit('Project already exists!')

        # Copy extracted files to project folder
        shutil.copytree(EXTRACT_DIRECTORY, BASE_DIRECTORY)
        number_of_files = len(os.listdir(BASE_DIRECTORY))
        
        

        for f in os.listdir(BASE_DIRECTORY): # Lists all files to be worked with.
            file_list.append(f)

        # Store all those filenames in save_file_list.
        with open(PROJECT_NAME + '/' + save_file_list, 'w') as meta_file: 
            meta_file.write(str(number_of_files) + '\n')
            for i in range(number_of_files):
                meta_file.write(file_list[i])
                if i < number_of_files - 1:
                    meta_file.write('\n')
        
        for i in range(number_of_files): # Defines size of list.
            file_data_list.append('')
    
    else:
        try:
            with open(PROJECT_NAME + '/' + save_file_list) as SFL:
                number_of_files = int(SFL.readline().strip('\n'))

                for i in range(number_of_files):
                    file_list.append(SFL.readline().strip('\n'))

            with open(PROJECT_NAME + '/' + save_file_data_list) as SFDL:
                for i in range(number_of_files):
                    file_data_list.append(SFDL.readline().strip('\n'))
        except FileNotFoundError:
            print('Project not found!')
            input('Press any key to exit...')
            exit('Project not found')
    

def save_project(): # Saves current project.
    global SAVE_FOLDER
    global PROJECT_NAME
    with open(PROJECT_NAME + '/' + save_file_list, 'w') as sFL:
        sFL.write(str(number_of_files) + '\n')
        for i in range(len(file_list)):
            w = file_list[i] + '\n'
            sFL.write(w)
    with open(PROJECT_NAME + '/' + save_file_data_list, 'w') as sFDL:
        for i in range(len(file_data_list)):
            w = file_data_list[i] + '\n'
            sFDL.write(w)
    print('Saving project...')
    input('Done! Press any key to continue...')

def work_on_files():
    check_file_data_list()
    valid_answer = False
    index_jump = -1 # Index to which jump to.
                    # If == -1, start from first incomplete file.
    order_of_increment = 1
    loop_end = number_of_files # Where the "for" loop shall progress towards
                                   #Changes wheter "order_of_increment is == 1 or ==- 1"
    validity__status_checker = 1 # Whick validity status to check;

    work_mode = 1 # Work mode. 0 = READ ONLY, 1 = WRITE

    while valid_answer == False: # Index Jump
        index_jump = int(input('Jump to index:\n\t -1 to continue at first incomplete file: '))
        if (not (0 <= index_jump <= number_of_files - 1)) and (not(type(index_jump) == int)):
            print('Invalid input!')
            valid_answer = False
        else:
            if index_jump == -1:
                index_jump = 0
            valid_answer = True

    valid_answer = False 
    while valid_answer == False: # Order of increment:
        order_of_increment = (
            int(input('Order of increment:\n\t 1 to progress in ASCENDING order,\n\t -1 to progress in DESCENDING ORDER: ')) )
        if order_of_increment != 1 and order_of_increment != -1: # Invalid answer!
            print('Invalid input!')
            valid_answer = False
        else: # Valid answer!
            if order_of_increment == 1:
                loop_end = number_of_files
            else:
                loop_end = 0
            valid_answer = True

    valid_answer = False 
    while valid_answer == False: # Which indexes to check:
                                    # 0: Empty.
                                    # 1: Full.
                                    # 2: Incomplete.
        validity__status_checker = (int(input(
            'Validity Checker:\n\t 0: Check only empty indexes,\n\t 1: Check only complete indexes,\n\t 2: Check only incomplete indexes.\n')))
            
        if not (0 <= validity__status_checker <= 2): # Invalid answer!
            print('Invalid input!')
            valid_answer = False

        else: # Valid answer!
            valid_answer = True
    
    valid_answer = False
    while valid_answer == False: # Work mode:
                                    # 0: READ ONLY
                                    # 1: WRITE
        work_mode = (int(input('Work Mode:\n\t 0: READ ONLY,\n\t 1: WRITE.')))
            
        if not (0 <= work_mode <= 1): # Invalid answer!
            print('Invalid input!')
            valid_answer = False

        else: # Valid answer!
            valid_answer = True

    
    for i in range(index_jump, loop_end, order_of_increment):
        if fdl_validation_index[i] == validity__status_checker: # If validity index equals the one being checked:
            should_exit = False
            e = input('Press Enter to continue, or "exit" to exit...')
            if e == 'exit':
                should_exit = True
            if should_exit:
                print('Exiting...')
                should_exit = False
                break

            print('File: ' + file_list[i] + '\nINDEX: ' + str(i))
            for g in range(len(PARAMETER_LIST)): # Display current values for index.
                print(PARAMETER_LIST[g] + ': ' + fdl_parameter_parser(i)[g])
                
            manipulate_file(file_list[i], '', ACZ_RADIO_ARG_VALUES, 0)
            if work_mode == 1: # WRITE
                file_data_list[i] = ''
                for g in PARAMETER_LIST:
                    print('Input parameter ' + g + ': ')
                    x = input()
                    file_data_list[i] = file_data_list[i] + g + '.' + x + ','
                file_data_list[i] = file_data_list[i].rstrip(file_data_list[i][-1])
                save_project()
    
    input('Work done! Press any key to continue...')
            
            


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
        # 0: No parameters.
        # 1: Fully filled in.
        # 2: Incomplete
    # Intended use: work_on_files() will check 'fdl_validation_index' and ignore indexes that have all complete parameters.
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
        
        final_validation = 0
        # If all parameters are VALID:
        if all( parameter_validation_buffer[i] == 1 for i in parameter_validation_buffer ):
            fdl_validation_index[i] = 1
        # If all parameters are INVALID:
        elif all( parameter_validation_buffer[i] == 0 for i in parameter_validation_buffer ):
            fdl_validation_index[i] = 0
        # If parameters are incomplete:
        else:
            fdl_validation_index[i] = 2


def separate_by_parameter(): # Separates files by chosen parameter.    
    global PARAMETER_LIST
    global fdl_validation_index
    reference_parameter = 0 # Parameter index in "PARAMETER_LIST" to be checked.

    # List contains all parameter values in file for given parameter.
    #Creates a folder for each value, if not empty.
    parameter_value_index = []
    parameter_value_buffer = ''

    valid_answer = False

    check_file_data_list() # Updates validation index.

    print('Separate files by parameter in folders. Maintains base folder intact.')
    print('Choose which parameter to separate by: \n----------')
    for g in range(len(PARAMETER_LIST)):
        print(str(g) + ': ' + PARAMETER_LIST[g])
    print('----------')
    
    while valid_answer == False: # Index Jump
        reference_parameter = int(input('Parameter: '))
        # If input is not between first and last indexes in "PARAMETER_LIST"
        if not(
            int((PARAMETER_LIST.index(PARAMETER_LIST[0])))
            <= reference_parameter
            <= int((PARAMETER_LIST.index(PARAMETER_LIST[-1])))
            ):
            
            print('Invalid input!')
            valid_answer = False
        else:
            valid_answer = True
    
    
    for i in range(number_of_files):
        parameter_value_buffer = fdl_parameter_parser(i)[reference_parameter]
        
        # List all folders to be created:
        # If index is not empty:
        if fdl_validation_index[i] == 1 or fdl_validation_index[i] == 2:
            if parameter_value_buffer: # If parameter value is not empty:
                # If value is not already present in the list:
                if not(parameter_value_buffer in parameter_value_index):
                    # Add it to the list.
                    parameter_value_index.append(parameter_value_buffer)
    
    # Create folders and copy files for each parameter value.

        buffer_folder_path = WORK_FOLDER + '/' + PARAMETER_LIST[reference_parameter] + '/'
        if not os.path.exists(buffer_folder_path):
            os.mkdir(buffer_folder_path)

    for p in range(len(parameter_value_index)):
        buffer_folder_path = WORK_FOLDER + '/' + PARAMETER_LIST[reference_parameter] + '/' + parameter_value_index[p]
        if not os.path.exists(buffer_folder_path):
            os.mkdir(buffer_folder_path)
        for l in range(number_of_files):
            parameter_value_buffer = fdl_parameter_parser(l)[reference_parameter]
            if parameter_value_buffer == parameter_value_index[p]:
                shutil.copy(BASE_DIRECTORY + '/' + file_list[l], buffer_folder_path)
    

            
        
    print('lol')



init_project()

separate_by_parameter()
# work_on_files()
save_project()