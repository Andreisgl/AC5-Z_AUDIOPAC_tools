# This module holds shared game and file presets between unpacker and repacker


# Data to support ACZ and AC5 modding
SUPPORTED_GAMES = ['AC5', 'ACZ']

# Data to support different file types ("BGM" and "RADIO")
PAC_TYPES = ['BGM', 'RADIO']

POSSIBLE_PAC_NAMES_ACZ = [['BGM.PAC', PAC_TYPES[0]],
                          ['RADIOUSA.PAC', PAC_TYPES[1]]]

POSSIBLE_PAC_NAMES_AC5 = [['BGM.PAC', PAC_TYPES[0]],
                          ['RADIOEE.PAC', PAC_TYPES[1]],
                          ['RADIOEJ.PAC', PAC_TYPES[1]]]


# Current file data
game = '' # Selected game
PAC_type = '' # If the file is BGM or RADIO
PAC_file_name = '' # File name, depends on the selected game
input_PAC_file_path = '' # Path to AUDIOPAC file

# Misc stuff
INPUT_EXIT_MESSAGE = 'PRESS ENTER TO EXIT'

def choose_file_data():
    # Prompts user to choose file data
    # Returns nothing. Global variables are updated instantly
    global SUPPORTED_GAMES
    global POSSIBLE_PAC_NAMES_ACZ
    global POSSIBLE_PAC_NAMES_AC5

    global game
    global PAC_type
    global PAC_file_name

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
    
    PAC_file_name = name_result[0]
    PAC_type = name_result[1]

    ### Remove later
    if False: # Debug stuff
        print('GAME ANSWER = {}\n{}\n'.format(game_answer, game))
        print('FILE ANSWER = {}\n{}\n'.format(file_answer, PAC_file_name))
        print('FILE TYPE = {}\n{}\n'.format(file_answer, PAC_type))
    ###

    

    pass

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