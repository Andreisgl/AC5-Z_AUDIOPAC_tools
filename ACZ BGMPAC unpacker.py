##ACZ BGM.PAC unpacker by death_the_d0g (death_the_d0g @ Twitter)
##
##Further expansion and experimentation by Andrei Segal (Andreisgl @ Github)
##and Luis Filipe Sales (luisfilipels @ GitHub)
##===============================================================
##TODO: clean this sorry mess of code.

import os
from os import listdir
from os.path import isfile, join

import pathlib
import shutil
import textwrap



BASE_FOLDER = "./UNPACKER"
PAC_IN_FOLDER = BASE_FOLDER + "/" + "PAC"
TBL_IN_FOLDER = BASE_FOLDER + "/" + "TBL"
OUTPUT_FOLDER = BASE_FOLDER + "/" + "OUT"

RESULTING_FOLDER_NAME = ""

ORIGINAL_PAC_NAME = ""
ORIGINAL_TBL_NAME = ""

#ORIGINAL_FILE_NAME = in_file_list[i] # Change this for fast debugging
#RESULTING_FILE_NAME = pathlib.Path(in_file_list[i]).stem + "_TBL.acd"
#ORIGINAL_FILE_NAME = INPUT_FOLDER + "/" + ORIGINAL_FILE_NAME
#RESULTING_FILE_NAME = OUTPUT_FOLDER + "/" + RESULTING_FILE_NAME




def find_files():
    #Checks if only one file of each type is present
    p = len(listdir(PAC_IN_FOLDER))
    if len(listdir(PAC_IN_FOLDER)) > 1 or len(listdir(TBL_IN_FOLDER)) > 1:
        error_msg = "Make sure to use only one .PAC and _TBL.acd file set at once!"
        input(error_msg)
        exit(error_msg)

    pac_file_list = listdir(PAC_IN_FOLDER)
    tbl_file_list = listdir(TBL_IN_FOLDER)

    global ORIGINAL_PAC_NAME
    global ORIGINAL_TBL_NAME
    global RESULTING_FOLDER_NAME

    ORIGINAL_PAC_NAME = PAC_IN_FOLDER + "/" + pac_file_list[0]
    ORIGINAL_TBL_NAME = TBL_IN_FOLDER + "/" + tbl_file_list[0]
    RESULTING_FOLDER_NAME = OUTPUT_FOLDER + "/" + pathlib.Path(pac_file_list[0]).stem + "/"
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)
    if not os.path.exists(RESULTING_FOLDER_NAME):
        os.mkdir(RESULTING_FOLDER_NAME)

    

def tbl():
    try:
        tbl_file = open(ORIGINAL_TBL_NAME, "rb")
    except FileNotFoundError as x:
        print ()
        print ("///ERROR///: .acd file not found.")
        print ()
        a = input("///INPUT///: Press any key to exit...")
        if a:
            exit(0)
        else:
            exit(0)
    else:
        return tbl_file

def pac():
    try:
        pac_file = open(ORIGINAL_PAC_NAME, "rb")
    except FileNotFoundError as x:
        print ()
        print ("///ERROR///: .PAC file not found.")
        print ()
        a = input("///INPUT///: Press any key to exit...")
        if a:
            exit(0)
        else:
            exit(0)
    else:
        pac_file.seek(0, os.SEEK_END)
        pac_file_s = pac_file.tell()
        if 0:   ##pac_file_s != 832665600:      ##File checking is disabled to allow for experimentation
            print()
            print(textwrap.fill("///ERROR///: Modified BGM.PAC files are not compatible with this script", width = 72))
            print()
            a = input("///INFO///: Press any key to exit...")
            if a:
                exit(0)
            else:
                exit(0)
        else:
            return pac_file

def extraction(tbl_file, pac_file):
    #if os.path.exists("BGM"):
    #    shutil.rmtree("BGM")
    if not os.path.exists(RESULTING_FOLDER_NAME):
        os.mkdir(RESULTING_FOLDER_NAME)
    
    print (textwrap.fill("///INFO///: Extracting files, please wait...", width = 72))
           
    val = 0
    val2 = 1
    f_n = 0
    f_offset = 4
    offset_list = []
    tbl_file.seek(0, 0)
    tbl_nof = int.from_bytes(tbl_file.read(4), byteorder = "little")    #First byte from BGM_TBL.acd is the number of files present.
    #tbl_nof = 1 #Disable parser loop for easier experimentation and extraction

    for f in range(tbl_nof):       #File parser
        tbl_file.seek(f_offset, 0)
        offset_list.append(int.from_bytes(tbl_file.read(4), byteorder = "little"))
        f_offset = f_offset + 4
    
    last_off = pac_file.seek(0, os.SEEK_END)
    offset_list.append(last_off)
    for f in range(tbl_nof):
        pac_file.seek(offset_list[val], 0)
        f_size = (offset_list[val2]) - (offset_list[val])
        data = pac_file.read(f_size)
        pac_file.seek((offset_list[val] + 52), 0)
        tag_str = pac_file.read(64)

        try:        #Now each error will be displayed, but the code will go on!!!
            s = tag_str.decode('UTF-8', errors ='replace')    #This is the problem.
        except:
            print("Tag decoding error")


        d = s.replace("\x00", "")
        wut = d.replace("�", "")
        a = wut.replace(".wav", "")
        aif = a.replace(".aif", "")
        fname = RESULTING_FOLDER_NAME + str(f_n).zfill(6) + "_" + aif + ".npsf"
        file = open(fname, "wb")    #There is an 'invalid argument' going on here.
        file.write(data)
        print (f_size, fname)
        val = val + 1
        val2 = val2 + 1
        f_n = f_n + 1

print(textwrap.fill("Ace Combat Zero BGM.PAC unpacker by death_the_d0g (death_the_d0g @ Twitter)", width = 80))
print(textwrap.fill("Further improvement by Andrei Segal (Andrei_sgl@ Github) and Luis Filipe Sales (luisfilipels @ GitHub)", width=80))
print(textwrap.fill("===========================================================================", width = 80))
print()
print("Extracts the contents found inside ACZs BGM.PAC files.")

#print("\n\nPlace all .PAC files in " + INPUT_FOLDER + " and get all TBL's in " + OUTPUT_FOLDER)
#print("All non-PAC files and folders will be ignored!")

find_files()
tbl_file = tbl()
pac_file = pac()
extraction(tbl_file, pac_file)
tbl_file.close()
pac_file.close()
##os.remove("BGM.pac")  ##Disable BGM.PAC removal for easier experimentation
exit()

