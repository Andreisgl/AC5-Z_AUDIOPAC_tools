##ACZ BGM.APC parser by by Andrei Segal (Andreisgl @ Github)
##Aid by Luis Filipe Sales (luisfilipels @ GitHub)
## Adapted from unpacker by death_the_d0g (death_the_d0g @ Twitter)
##===============================================================

import os
import shutil
import textwrap

ORIGINAL_FILE_NAME = "DATA.PAC" # Change this for fast debugging
RESULTING_FILE_NAME = "DATA_TBL.acd"

WORK_FOLDER = "./WORK"


ORIGINAL_FILE_NAME = WORK_FOLDER + "/" + ORIGINAL_FILE_NAME
RESULTING_FILE_NAME = WORK_FOLDER + "/" + RESULTING_FILE_NAME

def write_tbl_from_pac():
    print(textwrap.fill("///INFO///: Processing files, please wait...", width=72))

    

    if not os.path.exists(WORK_FOLDER):
            os.mkdir(WORK_FOLDER)
    
    offset_list = []
    tbl_size = os.path.getsize(ORIGINAL_FILE_NAME)

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


        
    return



print(textwrap.fill("Ace Combat 5/Zero .PAC parser by Andrei Segal (Andrei_sgl@ Github) and Luis Filipe Sales (luisfilipels @ GitHub)", width=80))
print(textwrap.fill("Adapted from death_the_d0g's (death_the_d0g @ Twitter) original ACZ BGM.PAC unpacker", width=80))
print(textwrap.fill("===========================================================================", width=80))
print()
print("Creates a TBL.acd file for a given .PAC file (DATA.PAC and BGM.PAC supported).")

write_tbl_from_pac()

exit()
