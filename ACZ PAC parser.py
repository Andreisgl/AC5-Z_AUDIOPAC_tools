##ACZ BGM.APC parser by by Andrei Segal (Andreisgl @ Github)
##Aid by Luis Filipe Sales (luisfilipels @ GitHub)
##===============================================================

import os
import shutil
import textwrap

ORIGINAL_FILE_NAME = "BGM.PAC" # Change this for fast debugging
RESULTING_FILE_NAME = "RADIO_TBL.acd"

def write_tbl_from_pac():
    if os.path.exists("BGM"):
        shutil.rmtree("BGM")

    os.mkdir("BGM")

    print(textwrap.fill("///INFO///: Extracting files, please wait...", width=72))

    offset_list = []
    tbl_nof = os.path.getsize(ORIGINAL_FILE_NAME)

    with open(ORIGINAL_FILE_NAME, 'rb') as pac_file:
        for f in range(0, tbl_nof, 4):
            data = pac_file.read(4)
            if not data:
                break
            if data == b'NPSF':
                offset_list.append(f)

                print('AAA')

    with open(RESULTING_FILE_NAME, "wb") as tbl_file:
        tbl_file.write(len(offset_list).to_bytes(byteorder="little", length=4))
        for element in offset_list:
            tbl_file.write(element.to_bytes(4, byteorder="little"))

    return


print(textwrap.fill("Ace Combat Zero BGM.PAC unpacker by death_the_d0g (death_the_d0g @ Twitter)", width=80))
print(textwrap.fill("===========================================================================", width=80))
print()
print("Extracts the contents found inside ACZs BGM.PAC files.")

write_tbl_from_pac()
exit()
