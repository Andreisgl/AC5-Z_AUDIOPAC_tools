## AUDIOPAC_repacker by Truc3 (Andreisgl @ Github, @truc3_8492 @ Twitter)
## Aid by Luis Filipe Sales (luisfilipels @ GitHub)
## Based on death_the_d0g's (deaththed0g @ Github, death_the_d0g @ Twitter)
## original "BGMPAC" sripts for Ace Combat Zero
##===============================================================

# This script repacks extracted .npsf files into a single .PAC file

import os
import sys
import shutil
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
 



def main():
    global input_PAC_file_path
    global OUTPUT_AUDIOPAC_FOLDER

    greeting_message = ('AUDIOPAC_repacker\n'
                        'This script repack track.npsf files '
                        'into a single AUDIO.PAC file'
                        'and a .dat file.'
                        )
    print(greeting_message)

    prepare_paths()
    
    

    #print('\nDone!')
    #input(INPUT_EXIT_MESSAGE)

    pass



if __name__ == '__main__':
    main()