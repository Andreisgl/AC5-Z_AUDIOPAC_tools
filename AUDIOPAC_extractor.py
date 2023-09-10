## AUDIOPAC_extractor by Truc3 (Andreisgl @ Github, @truc3_8492 @ Twitter)
## Aid by Luis Filipe Sales (luisfilipels @ GitHub)
## Based on death_the_d0g's (deaththed0g @ Github, death_the_d0g @ Twitter)
## original "BGMPAC" sripts for Ace Combat Zero
##===============================================================

# This script extracts AUDIO.PAC files ("BGM.PAC" or "RADIOUSA.PAC")
# into individual files in a folder.

import os

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
    if not os.path.exists(OUTPUT_AUDIOPAC_FOLDER):
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

def assemble_tbl(audiopac_path):
    # Assembles .TBL file for current AUDIOPAC file.
    # Returns list with all track offsets.

    tbl_size = os.path.getsize(audiopac_path)
    offset_list = []
    with open(audiopac_path, 'rb') as file:
        raw_data = file.read()

        # Every b'NPSF' marks the beginning of a new track.
        current_header_index = -4 # Start at -4 so search starts at offset 0
        track_offset_list = []
        while current_header_index != -1:
            current_header_index = raw_data.find(b'NPSF', current_header_index+4)
            track_offset_list.append(current_header_index)
            print('{} / {}'.format(current_header_index, tbl_size))
        track_offset_list.pop() # Remove last, "-1", index.
    
    return track_offset_list

    




def main():
    global input_PAC_file_path
    greeting_message = ('AUDIOPAC_extractor\n'
                        'This script extracts AUDIO.PAC files '
                        '("BGM.PAC" or "RADIOUSA.PAC") into '
                        'individual files in a folder.'
                        )
    print(greeting_message)

    prepare_paths()
    
    assemble_tbl(input_PAC_file_path)


    pass



if __name__ == '__main__':
    main()