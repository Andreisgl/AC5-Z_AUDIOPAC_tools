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
from modules import pac_modules


# Misc stuff
INPUT_EXIT_MESSAGE = presets.INPUT_EXIT_MESSAGE

# Files and paths
SCRIPT_PATH = __file__ # This script's path
BASEDIR_PATH = os.path.dirname(SCRIPT_PATH) # The script's folder
INPUT_AUDIOPAC_FOLDER = 'INPUT' # Dir where the input AUDIOPAC will stay
OUTPUT_AUDIOPAC_FOLDER = 'OUTPUT'

DAT_DATA_FOLDER_PATH = 'DAT_DATA'

def prepare_paths():
    # Prepares all paths needed for the script
    #region # Set global variables
    global SUPPORTED_GAMES
    global POSSIBLE_PAC_NAMES_ACZ
    global POSSIBLE_PAC_NAMES_AC5

    global game
    global PAC_type
    global output_PAC_file_name
    global output_PAC_file_path

    global BASEDIR_PATH
    global INPUT_AUDIOPAC_FOLDER
    global OUTPUT_AUDIOPAC_FOLDER

    global DAT_DATA_FOLDER_PATH

    # DAT_DATA PATHS
    global AC5_DAT_FOLDER_PATH
    global ACZ_DAT_FOLDER_PATH

    global AC5_DAT_BGM_FOLDER
    global AC5_DAT_RADIO_FOLDER
    global ACZ_DAT_BGM_FOLDER
    global ACZ_DAT_RADIO_FOLDER
    #endregion

    presets.choose_file_data() # Get filename data

    # Gets game and file names from module
    game = presets.game
    PAC_type = presets.PAC_type
    output_PAC_file_name = presets.PAC_file_name

    #region AC5 abort
    if game == 'AC5': # Block AC5 from being used. Still unsupported.
        input('Sorry! AC5 is currently not supported!\n{}'
              .format(INPUT_EXIT_MESSAGE))
        exit(1)
    #endregion
  
    #region Get names from presets.py
    SUPPORTED_GAMES = presets.SUPPORTED_GAMES
    POSSIBLE_PAC_NAMES_ACZ = presets.POSSIBLE_PAC_NAMES_ACZ
    POSSIBLE_PAC_NAMES_AC5 = presets.POSSIBLE_PAC_NAMES_AC5
    #endregion
    
    #region Check/create important folders
    # INPUT FOLDER
    INPUT_AUDIOPAC_FOLDER = os.path.join(BASEDIR_PATH, INPUT_AUDIOPAC_FOLDER)
    if not os.path.exists(INPUT_AUDIOPAC_FOLDER):
        os.mkdir(INPUT_AUDIOPAC_FOLDER)
    
    # OUTPUT FOLDER
    OUTPUT_AUDIOPAC_FOLDER= os.path.join(BASEDIR_PATH, OUTPUT_AUDIOPAC_FOLDER)
    if os.path.exists(OUTPUT_AUDIOPAC_FOLDER):
        # Delete dir if it exists. The folder shall always start empty
        shutil.rmtree(OUTPUT_AUDIOPAC_FOLDER)
    os.mkdir(OUTPUT_AUDIOPAC_FOLDER)

    # DAT_DATA FOLDERS
    # These folders will contain the data from the dat files that contain the
    # tbls required to read the tracks.
    # e.g. ACZ: "0000.dat" for BGM table, "0001.dat" for RADIO table
    DAT_DATA_FOLDER_PATH = os.path.join(BASEDIR_PATH, DAT_DATA_FOLDER_PATH)
    AC5_DAT_FOLDER_PATH = os.path.join(DAT_DATA_FOLDER_PATH, SUPPORTED_GAMES[0])
    ACZ_DAT_FOLDER_PATH = os.path.join(DAT_DATA_FOLDER_PATH, SUPPORTED_GAMES[1])
    
    # Subfolders
    AC5_DAT_BGM_FOLDER = os.path.join(AC5_DAT_FOLDER_PATH, presets.PAC_TYPES[0])
    AC5_DAT_RADIO_FOLDER = os.path.join(AC5_DAT_FOLDER_PATH, presets.PAC_TYPES[1])
    ACZ_DAT_BGM_FOLDER = os.path.join(ACZ_DAT_FOLDER_PATH, presets.PAC_TYPES[0])
    ACZ_DAT_RADIO_FOLDER = os.path.join(ACZ_DAT_FOLDER_PATH, presets.PAC_TYPES[1])
    #endregion
    
 
    output_PAC_file_path = os.path.join(OUTPUT_AUDIOPAC_FOLDER,
                                       output_PAC_file_name)
    
    pass
    


def assemble_audiopac_file():
    # Assembles output ADUIO.PAC file from "INPUT_AUDIOPAC_FOLDER"'s contents.
    global output_PAC_file_path
    global INPUT_AUDIOPAC_FOLDER

    track_name_list = os.listdir(INPUT_AUDIOPAC_FOLDER)
    track_path_list = [os.path.join(INPUT_AUDIOPAC_FOLDER, x)
                       for x in track_name_list]

    with open(output_PAC_file_path, 'wb') as pac_file:
        for track in track_path_list:
            with open(track, 'rb') as track_file:
                pac_file.write(track_file.read())

def assemble_dat_file():
    # Assemble .dat file based on the offset table
    # How it works:
    # The .dat files contain their own data, with the offset tbl in the middle
    # For ACZ, the .dat for BGM is 0000.dat, for RADIO it is 0001.dat.
    # In the DAT_DATA folders, the .dat is split in two:
    # The data before the table, and the data after it.
    # This method will stitch it all together:
    # 0_acz_0000.dat - offset_tbl - 1_acz_0000.dat

    #region # Set global variables
    global game
    global PAC_type
    global OUTPUT_AUDIOPAC_FOLDER

    global AC5_DAT_BGM_FOLDER
    global AC5_DAT_RADIO_FOLDER
    global ACZ_DAT_BGM_FOLDER
    global ACZ_DAT_RADIO_FOLDER
    #endregion

    #region # Filenames for the .dats and parts
    AC5_BGM_dat_parts_file_names = ['?.acd', '?.acd']
    AC5_BGM_final_dat_file_name = '?.dat'
    AC5_RADIO_dat_parts_file_names = ['?.acd', '?.acd']
    AC5_RADIO_final_dat_file_name = '?.dat'

    ACZ_BGM_dat_parts_file_names = ['0_acz_0000.acd', '1_acz_0000.acd']
    ACZ_BGM_final_dat_file_name = '0000.dat'
    ACZ_RADIO_dat_parts_file_names = ['0_acz_0001.acd', '1_acz_0001.acd']
    ACZ_RADIO_final_dat_file_name = '0001.dat'
    #endregion
    
    # Determine which files to use
    cur_dat_parts_file_names = []
    cur_final_dat_file_name = ''
    cur_dat_parts_paths = []
    cur_final_dat_path = ''
    dat_folder_path = ''
    #region
    match game:
        case 'AC5':
            match PAC_type:
                case 'BGM':
                    cur_dat_parts_file_names = AC5_BGM_dat_parts_file_names
                    cur_final_dat_file_name = AC5_BGM_final_dat_file_name
                    dat_folder_path = AC5_DAT_BGM_FOLDER
                case 'RADIO':
                    cur_dat_parts_file_names = AC5_RADIO_dat_parts_file_names
                    cur_final_dat_file_name = AC5_RADIO_final_dat_file_name
                    dat_folder_path = AC5_DAT_RADIO_FOLDER

        case 'ACZ':
            match PAC_type:
                case 'BGM':
                    cur_dat_parts_file_names = ACZ_BGM_dat_parts_file_names
                    cur_final_dat_file_name = ACZ_BGM_final_dat_file_name
                    dat_folder_path = ACZ_DAT_BGM_FOLDER
                case 'RADIO':
                    cur_dat_parts_file_names = ACZ_RADIO_dat_parts_file_names
                    cur_final_dat_file_name = ACZ_RADIO_final_dat_file_name
                    dat_folder_path = ACZ_DAT_RADIO_FOLDER
    #endregion

    # Join paths for files
    cur_dat_parts_paths = [os.path.join(dat_folder_path, x) for x in cur_dat_parts_file_names]
    cur_final_dat_path = os.path.join(OUTPUT_AUDIOPAC_FOLDER, cur_final_dat_file_name)

    # Assemble final file
    with open(cur_final_dat_path, 'wb') as final_dat:
        # Write first part of dat
        with open(cur_dat_parts_paths[0], 'rb') as acd0:
            final_dat.write(acd0.read())

        # Write table
        # Convert int to bin and write
        offset_table = pac_modules.assemble_tbl_from_audiopac(output_PAC_file_path)
        for offset in [x.to_bytes(4, 'little') for x in offset_table]:
            final_dat.write(offset)
        
        # How many bytes to add to finish line. Line lenght is 16 bytes
        # Padding bytes are "b'x\00'"
        padding_len = pac_modules.line_fill(final_dat.tell(), 16)
        for bt in range(padding_len):
            final_dat.write(b'\x00')
        
        # Write second part of dat
        with open(cur_dat_parts_paths[1], 'rb') as acd1:
            final_dat.write(acd1.read())
    
    #pac_modules.export_tbl(offset_table, BASEDIR_PATH)


    

def main():
    global output_PAC_file_path
    global OUTPUT_AUDIOPAC_FOLDER

    greeting_message = ('AUDIOPAC_repacker\n'
                        'This script repack track.npsf files '
                        'into a single AUDIO.PAC file'
                        'and a .dat file.'
                        )
    print(greeting_message)

    prepare_paths()
    
    assemble_audiopac_file()
    assemble_dat_file()
    

    #print('\nDone!')
    #input(INPUT_EXIT_MESSAGE)

    pass



if __name__ == '__main__':
    main()