## AUDIOPAC_extractor by Truc3 (Andreisgl @ Github, @truc3_8492 @ Twitter)
## Aid by Luis Filipe Sales (luisfilipels @ GitHub)
## Based on death_the_d0g's (deaththed0g @ Github, death_the_d0g @ Twitter)
## original "BGMPAC" sripts for Ace Combat Zero
##===============================================================

# This script extracts AUDIO.PAC files ("BGM.PAC" or "RADIOUSA.PAC")
# into individual files in a folder.

import os
import math
import shutil

# Data to support ACZ and AC5 modding
SUPPORTED_GAMES = ['AC5', 'ACZ']

# Data to support different file types ("BGM" and "RADIO")
PAC_TYPES = ['BGM', 'RADIO']

POSSIBLE_PAC_NAMES_ACZ = [['BGM.PAC', PAC_TYPES[0]],
                          ['RADIOUSA.PAC', PAC_TYPES[1]]]

POSSIBLE_PAC_NAMES_AC5 = [['BGM.PAC', PAC_TYPES[0]],
                          ['RADIOEE.PAC', PAC_TYPES[1]],
                          ['RADIOEJ.PAC', PAC_TYPES[1]]]

# Misc stuff
INPUT_EXIT_MESSAGE = 'PRESS ENTER TO EXIT'

# Current file data
game = '' # Selected game
PAC_type = '' # If the file is BGM or RADIO
input_PAC_file_name = '' # File name, depends on the selected game
input_PAC_file_path = '' # Path to AUDIOPAC file


# Files and paths
SCRIPT_PATH = __file__ # This script's path
BASEDIR_PATH = os.path.dirname(SCRIPT_PATH) # The script's folder
INPUT_AUDIOPAC_FOLDER = 'INPUT' # Dir where the input AUDIOPAC will stay
OUTPUT_AUDIOPAC_FOLDER = 'OUTPUT'


def prepare_paths():
    # Prepares all paths needed for the script
    global game
    global PAC_type
    global input_PAC_file_name
    global input_PAC_file_path

    global BASEDIR_PATH
    global INPUT_AUDIOPAC_FOLDER
    global OUTPUT_AUDIOPAC_FOLDER

    # Create important folders
    INPUT_AUDIOPAC_FOLDER = os.path.join(BASEDIR_PATH, INPUT_AUDIOPAC_FOLDER)
    if not os.path.exists(INPUT_AUDIOPAC_FOLDER):
        os.mkdir(INPUT_AUDIOPAC_FOLDER)
    
    OUTPUT_AUDIOPAC_FOLDER= os.path.join(BASEDIR_PATH, OUTPUT_AUDIOPAC_FOLDER)
    if os.path.exists(OUTPUT_AUDIOPAC_FOLDER):
        # Delete dir if it exists. The folder shall always start empty
        shutil.rmtree(OUTPUT_AUDIOPAC_FOLDER)
    os.mkdir(OUTPUT_AUDIOPAC_FOLDER)

    choose_file_data() # Get filename data

    if game == 'AC5': # Block AC5 from being used. Still unsupported.
        input('Sorry! AC5 is currently not supported!\n{}'
              .FORMAT(INPUT_EXIT_MESSAGE))
        exit(1)
    
    input_PAC_file_path = os.path.join(INPUT_AUDIOPAC_FOLDER,
                                       input_PAC_file_name)

    # Abort if input AUDIOPAC file does not exist
    if not os.path.exists(input_PAC_file_path):
        print('{} not found!'.format(input_PAC_file_name))
        print('Make sure you have selected the right file in the prompt')
        input(INPUT_EXIT_MESSAGE)
        exit(1)
 

def prompt_user_list(option_list):
    # This function creates a prompt to choose from a list.
    # Handles invalid answers. Answer must be an index.
    # Returns index

    for index, entry in enumerate(option_list):
        print('{} - {}'.format(index, entry))
    print()

    index_range = len(option_list)-1
    valid_index = True
    while True:
        answer = ''
        if not valid_index: # Cisplay error message accordig to flag
            print('Input a valid index!')

        try:
            answer = int(input('Enter index: ')) # Receive answer
        except ValueError:
            valid_index = False # Set flag to false on invalidity
            continue

        if answer < 0 or answer > index_range:
            valid_index = False # Set flag to false on invalidity
            continue

        break
        
    return answer

def choose_file_data():
    # Prompts user to choose file data
    # Returns nothing. Global variables are updated instantly
    global SUPPORTED_GAMES
    global POSSIBLE_PAC_NAMES_ACZ
    global POSSIBLE_PAC_NAMES_AC5

    global game
    global PAC_type
    global input_PAC_file_name

    print('Choose what game you want to work on:')
    game_answer = prompt_user_list(SUPPORTED_GAMES)
    

    print('Choose what file you want to work on:')
    match game_answer:
        case 0:
            # AC5
            aux = [x[0] for x in POSSIBLE_PAC_NAMES_AC5] # Show only filenames
            file_answer = prompt_user_list(aux)
        case 1:
            # ACZ
            aux = [x[0] for x in POSSIBLE_PAC_NAMES_ACZ] # Show only filenames
            file_answer = prompt_user_list(aux)

    

    # Assign answers to data
    game = SUPPORTED_GAMES[game_answer]

    match game_answer:
        case 0:
            name_result = POSSIBLE_PAC_NAMES_AC5[file_answer]
        case 1:
            name_result = POSSIBLE_PAC_NAMES_ACZ[file_answer]
    
    input_PAC_file_name = name_result[0]
    PAC_type = name_result[1]

    ### Remove later
    if False: # Debug stuff
        print('GAME ANSWER = {}\n{}\n'.format(game_answer, game))
        print('FILE ANSWER = {}\n{}\n'.format(file_answer, input_PAC_file_name))
        print('FILE TYPE = {}\n{}\n'.format(file_answer, PAC_type))
    ###

    

    pass


def assemble_tbl_from_audiopac(audiopac_path):
    # Assembles .TBL file for a given AUDIOPAC file.
    # Returns list with all track offsets.

    file_size = os.path.getsize(audiopac_path)
    offset_list = []
    with open(audiopac_path, 'rb') as file:
        raw_data = file.read()

        # Every b'NPSF' marks the beginning of a new track.
        current_header_index = -4 # Start at -4 so search starts at offset 0
        track_offset_list = []
        while current_header_index != -1:
            current_header_index = raw_data.find(b'NPSF', current_header_index+4)
            track_offset_list.append(current_header_index)
            print('{} / {}'.format(current_header_index, file_size))
        track_offset_list.pop() # Remove last, "-1", index.
    
    return track_offset_list

def split_audiopac(audiopac_path, output_folder, offset_tbl):
    # Splits an AUDIOPAC file using its previously created offset table.
    # Dumps extracted files into a given output folder.

    # Assemble list with track sizes based on offset_tbl
    track_size_list = []
    file_size = os.path.getsize(audiopac_path)
    offset_tbl.append(file_size) # Append file size to list to help process
    tbl_last_index = len(offset_tbl)-1

    for index, offset in enumerate(offset_tbl):
        if index == tbl_last_index:
            break # Break loop if end is reached
        curr_size = offset_tbl[index+1] - offset_tbl[index]
        track_size_list.append(curr_size)
        print(curr_size)
    

    # Read AUDIOPAC file and split data into list based on sizes
    track_data_list = []
    
    # Calculate "last_file_index" and "number_of_digits" for filename prefix
    last_file_index = len(track_size_list)-1
    number_of_digits = math.floor(math.log10(last_file_index)+1)

    with open(audiopac_path, 'rb') as file:
        for index, file_size in enumerate(track_size_list):
            # Raw track data
            data = file.read(file_size)

            # Get track name
            start = 52 # Hardcoded. Name starts in index 52 of track
            aux = data[start:256] # End trim at a big enough index
            end = aux.find(b'\x00') # Cut name at first b'\x00' found
            track_name = aux[:end]

            # Add numeration prefix to track names to keep the right order
            prefix = str(index).zfill(number_of_digits) + '_'
            track_name = prefix + track_name.decode("utf-8")
            # Change extension to ".npsf"
            track_name = track_name.split('.')[0] + '.npsf'

            # Append [data, track_name] set to list
            track_data_list.append([data, track_name])

    # Write track files into output
    

    return track_data_list

def main():
    global input_PAC_file_path
    global OUTPUT_AUDIOPAC_FOLDER

    greeting_message = ('AUDIOPAC_extractor\n'
                        'This script extracts AUDIO.PAC files '
                        '("BGM.PAC" or "RADIOUSA.PAC") into '
                        'individual files in a folder.'
                        )
    print(greeting_message)

    prepare_paths()
    
    ### def extract_audiopac(input_PAC_file_path)
    offset_tbl = assemble_tbl_from_audiopac(input_PAC_file_path)
    track_data = split_audiopac(input_PAC_file_path, OUTPUT_AUDIOPAC_FOLDER, offset_tbl)
    pass
    for track in track_data:
        filename = track[1]
        file_path = os.path.join(OUTPUT_AUDIOPAC_FOLDER, filename)

        print(filename)
        with open(file_path, 'wb') as file:
            file.write(track[0])
            pass
    
    #######



    pass



if __name__ == '__main__':
    main()