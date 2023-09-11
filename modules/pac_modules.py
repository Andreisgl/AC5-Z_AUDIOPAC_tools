# This module holds methods common to the extractor and unpacker.

import os

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