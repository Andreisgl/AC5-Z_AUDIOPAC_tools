## AUDIOPAC_extractor by Truc3 (Andreisgl @ Github, @truc3_8492 @ Twitter)
## Aid by Luis Filipe Sales (luisfilipels @ GitHub)
## Based on death_the_d0g's (deaththed0g @ Github, death_the_d0g @ Twitter)
## original "BGMPAC" sripts for Ace Combat Zero
##===============================================================

# This script extracts AUDIO.PAC files ("BGM.PAC", "RADIOUSA.PAC", "RADIOEE.PAC", "RADIOEJ.PAC")
# into individual files in a folder.

import os
import sys
import shutil

import math
# setting path
sys.path.append('../bgm_pac_ace')
from modules import presets


# Misc stuff
INPUT_EXIT_MESSAGE = presets.INPUT_EXIT_MESSAGE

# Files and paths
SCRIPT_PATH = __file__ # This script's path
BASEDIR_PATH = os.path.dirname(SCRIPT_PATH) # The script's folder
INPUT_AUDIOPAC_FOLDER = 'INPUT' # Dir where the input AUDIOPAC will stay
OUTPUT_AUDIOPAC_FOLDER = 'OUTPUT'


def prepare_paths():
    # Prepares all paths needed for the script
    global SUPPORTED_GAMES
    global POSSIBLE_PAC_NAMES_ACZ
    global POSSIBLE_PAC_NAMES_AC5

    global game
    global PAC_type
    global input_PAC_file_name
    global input_PAC_file_path

    global BASEDIR_PATH
    global INPUT_AUDIOPAC_FOLDER
    global OUTPUT_AUDIOPAC_FOLDER


    presets.choose_file_data() # Get filename data

    # Gets game and file names from module
    game = presets.game
    PAC_type = presets.PAC_type
    input_PAC_file_name = presets.input_PAC_file_name
    #input_PAC_file_path

    if game == 'AC5': # Block AC5 from being used. Still unsupported.
        input('Sorry! AC5 is currently not supported!\n{}'
              .format(INPUT_EXIT_MESSAGE))
        exit(1)
    

    SUPPORTED_GAMES = presets.SUPPORTED_GAMES
    POSSIBLE_PAC_NAMES_ACZ = presets.POSSIBLE_PAC_NAMES_ACZ
    POSSIBLE_PAC_NAMES_AC5 = presets.POSSIBLE_PAC_NAMES_AC5

    # Create important folders
    INPUT_AUDIOPAC_FOLDER = os.path.join(BASEDIR_PATH, INPUT_AUDIOPAC_FOLDER)
    if not os.path.exists(INPUT_AUDIOPAC_FOLDER):
        os.mkdir(INPUT_AUDIOPAC_FOLDER)
    
    OUTPUT_AUDIOPAC_FOLDER= os.path.join(BASEDIR_PATH, OUTPUT_AUDIOPAC_FOLDER)
    if os.path.exists(OUTPUT_AUDIOPAC_FOLDER):
        # Delete dir if it exists. The folder shall always start empty
        shutil.rmtree(OUTPUT_AUDIOPAC_FOLDER)
    os.mkdir(OUTPUT_AUDIOPAC_FOLDER)

    
    
    input_PAC_file_path = os.path.join(INPUT_AUDIOPAC_FOLDER,
                                       input_PAC_file_name)

    # Abort if input AUDIOPAC file does not exist
    if not os.path.exists(input_PAC_file_path):
        print('{} not found!'.format(input_PAC_file_name))
        print('Make sure you have selected the right file in the prompt')
        input(INPUT_EXIT_MESSAGE)
        exit(1)
 






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
                        '("BGM.PAC", "RADIOUSA.PAC", '
                        '"RADIOEE.PAC", "RADIOEJ.PAC") into '
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

    print('\nDone!')
    input(INPUT_EXIT_MESSAGE)

    pass



if __name__ == '__main__':
    main()