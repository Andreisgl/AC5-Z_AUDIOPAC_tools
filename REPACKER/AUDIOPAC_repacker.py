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