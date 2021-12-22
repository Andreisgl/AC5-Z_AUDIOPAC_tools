##ACZ BGM.APC parser by by Andrei Segal (Andreisgl @ Github)
##===============================================================

import os
import shutil
import textwrap


def tbl():
    try:
        tbl_file = open("BGM_TBL.acd", "rb")
    except FileNotFoundError as x:
        print()
        print("///ERROR///: BGM_TBL.acd file not found.")
        print()
        a = input("///INPUT///: Press any key to exit...")
        if a:
            exit(0)
        else:
            exit(0)
    else:
        return tbl_file


def pac():
    try:
        pac_file = open("BGM.pac", "rb")
    except FileNotFoundError as x:
        print()
        print("///ERROR///: BGM.pac file not found.")
        print()
        a = input("///INPUT///: Press any key to exit...")
        if a:
            exit(0)
        else:
            exit(0)
    else:
        pac_file.seek(0, os.SEEK_END)
        pac_file_s = pac_file.tell()
        return pac_file


def extraction(tbl_file, pac_file):
    if os.path.exists("BGM"):
        shutil.rmtree("BGM")

    os.mkdir("BGM")

    print(textwrap.fill("///INFO///: Extracting files, please wait...", width=72))

    val = 0
    val2 = 1
    f_n = 0
    f_offset = 0
    offset_list = []
    #pac_file.seek(0, 0)
    tbl_nof = os.path.getsize(
        'BGM.pac')  # int.from_bytes(tbl_file.read(4), byteorder = "little")    #First byte from BGM_TBL.acd is the number of files present.

    # tbl_nof = 1 #Disable parser loop for easier experimentation and extraction

    found_first_header = False
    count_bytes = 0
    with open('BGM.PAC', 'rb') as pac_file:
        for f in range(tbl_nof):
            data = pac_file.read(4)
            if not data:
                break
            if data == b"NPSF":
                if not found_first_header:
                    found_first_header = True
                else:
                    if len(offset_list) == 0:
                        offset_list.append(f)
                    else:
                        offset_list.append(f - offset_list[len(offset_list) - 1])
                print('AAA')
        offset_list.append(tbl_nof - offset_list[len(offset_list) - 1])

    ''''for f in range(tbl_nof):  # File parser
        pac_file.seek(f_offset, 0)

        readBuffer = pac_file.read(4)

        if readBuffer == b'NPSF':
            if not found_first_header:
                found_first_header = True
            else:
                if len(offset_list) == 0:
                    offset_list.append(f)
                else:
                    offset_list.append(f - offset_list[len(offset_list) - 1])
                print('AAA')

        f_offset = f_offset + 4
    offset_list.append(tbl_nof - offset_list[len(offset_list) - 1])''' # REMOVE THESE COMMENTS IF ALTERNATIVE CODE IS CORRECT
    #   ## CRIAR ARQUIVO AQUI. DEVE CONTER OS DADO DA LISTA 'offset_list'

    tbl_file = open("RADIO_TBL.acd", "wb")
    tbl_file.write(len(offset_list).to_bytes(byteorder="little", length=4))

    for element in offset_list:
        tbl_file.write(element.to_bytes(4, byteorder="little"))

    tbl_file.close()

    return # TODO: Remove when the TBL generator is working
    for f in range(tbl_nof):
        pac_file.seek(offset_list[val], 0)
        f_size = (offset_list[val2]) - (offset_list[val])
        data = pac_file.read(f_size)
        pac_file.seek((offset_list[val] + 52), 0)
        tag_str = pac_file.read(64)

        try:  # Now each error will be displayed, but the code will go on!!!
            s = tag_str.decode('UTF-8')  # This is the problem.
        except:
            print("Tag decoding error")

        d = s.replace("\x00", "")
        a = d.replace(".wav", "")
        aif = a.replace(".aif", "")
        fname = "BGM//" + str(f_n).zfill(4) + "_" + aif + ".npsf"
        file = open(fname, "wb")  # There is an 'invalid argument' going on here.
        file.write(data)
        print(f_size, fname)
        val = val + 1
        val2 = val2 + 1
        f_n = f_n + 1


print(textwrap.fill("Ace Combat Zero BGM.PAC unpacker by death_the_d0g (death_the_d0g @ Twitter)", width=80))
print(textwrap.fill("===========================================================================", width=80))
print()
print("Extracts the contents found inside ACZs BGM.PAC files.")

tbl_file = tbl()
pac_file = pac()
extraction(tbl_file, pac_file)
tbl_file.close()
pac_file.close()
##os.remove("BGM.pac")  ##Disable BGM.PAC removal for easier experimentation
exit()
