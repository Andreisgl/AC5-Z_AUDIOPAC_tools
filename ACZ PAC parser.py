##ACZ BGM.APC parser by by Andrei Segal (Andreisgl @ Github)
##Aid by Luis Filipe Sales (luisfilipels @ GitHub)
## Adapted from unpacker by death_the_d0g (death_the_d0g @ Twitter)
##===============================================================

import os
from os import listdir
from os.path import isfile, join

import pathlib
import shutil
import textwrap


BASE_FOLDER = "./PARSER"
INPUT_FOLDER = BASE_FOLDER + "/" + "IN"
OUTPUT_FOLDER = BASE_FOLDER + "/" + "OUT"


def write_tbl_from_pac():
    print(textwrap.fill("///INFO///: Processing files, please wait...", width=72))

    

    

    if not os.path.exists(BASE_FOLDER):
            os.mkdir(BASE_FOLDER)

    if not os.path.exists(INPUT_FOLDER):
            os.mkdir(INPUT_FOLDER)
            print ()
            errormsg = "///ERROR///: INPUT folder does not exist!"
            print (errormsg)
            print ()
            input("///INPUT///: Press any key to exit...")
            exit(errormsg)

    if not os.path.exists(OUTPUT_FOLDER):
            os.mkdir(OUTPUT_FOLDER)
            
    in_file_list = listdir(INPUT_FOLDER)
    for i in range(-len(in_file_list), 0):
        if not isfile(INPUT_FOLDER + "/" + in_file_list[i]):
            in_file_list.pop(i)
        if not pathlib.Path(INPUT_FOLDER + "/" + in_file_list[i]).suffix == ".PAC":
            in_file_list.pop(i)

    #[f for f in listdir(BASE_FOLDER) if isfile(join(BASE_FOLDER, f))]

    for i in range(len(in_file_list)):
        ORIGINAL_FILE_NAME = in_file_list[i] # Change this for fast debugging
        RESULTING_FILE_NAME = pathlib.Path(in_file_list[i]).stem + "_TBL.acd"
        ORIGINAL_FILE_NAME = INPUT_FOLDER + "/" + ORIGINAL_FILE_NAME
        RESULTING_FILE_NAME = OUTPUT_FOLDER + "/" + RESULTING_FILE_NAME

        offset_list = []
        
        try:
            tbl_size = os.path.getsize(ORIGINAL_FILE_NAME)
            
        except FileNotFoundError as x:
            print ()
            errormsg = "///ERROR///: .PAC file not found."
            print (errormsg)
            print ()
            input("///INPUT///: Press any key to exit...")
            exit(errormsg)
        
        with open(ORIGINAL_FILE_NAME, 'rb') as pac_file:
            for bytes_offset in range(0, tbl_size, 4):
                data = pac_file.read(4)
                if not data:
                    break
                if data == b'NPSF':
                    offset_list.append(bytes_offset)

        with open(RESULTING_FILE_NAME, "wb") as tbl_file:
            tbl_file.write(len(offset_list).to_bytes(byteorder="little", length=4))
            for element in offset_list:
                tbl_file.write(element.to_bytes(4, byteorder="little"))
        print(in_file_list[i] + " done")


        
    return



print(textwrap.fill("Ace Combat 5/Zero .PAC parser by Andrei Segal (Andrei_sgl@ Github) and Luis Filipe Sales (luisfilipels @ GitHub)", width=80))
print(textwrap.fill("Adapted from death_the_d0g's (death_the_d0g @ Twitter) original ACZ BGM.PAC unpacker", width=80))
print(textwrap.fill("===========================================================================", width=80))
print()
print("Creates a TBL.acd file for a given .PAC file (Supports multiple files at once!)\n")
print("(ONLY BGM AND RADIO FILES SUPPORTED).")

print("\n\nPlace all .PAC files in " + INPUT_FOLDER + " and get all TBL's in " + OUTPUT_FOLDER)
print("All non-PAC files and folders will be ignored!")

write_tbl_from_pac()

input("All Files done! Press any key to continue...")

exit()
