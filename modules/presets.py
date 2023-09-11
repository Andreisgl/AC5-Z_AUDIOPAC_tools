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