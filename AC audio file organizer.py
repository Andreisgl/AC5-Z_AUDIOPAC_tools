## AC Audio File Organizer - by Andreisgl @ Github
# Manipulates the folder with audio files in order to organize each file to aid editing.

import subprocess




## Argument list for MFAudio, with indexes for the lists used in this code
#0 -  /IFnnnnn	Input frequency
#1 -  /ICn	Input channels
#2 -  /IIxxxx	Input interleave (hex)
#3 -  /IHxxxx	Input headerskip (hex)
#4 -  /OTtttt	Output type (WAVU, VAGC,
# 	            SS2U, SS2C, RAWU, RAWC)
#5 -  /OFnnnnn	Output frequency
#6 -  /OCn	Output channels
#7 -  /OIxxxx	Output interleave (hex)
#8 -  "InputFile"	Input file to play/convert
#9 -  "OutputFile"	Output file to convert to

numArguments = 10

inputFilename = 'lol.npsf'
outputFilename = 'lol.wav'
aczRADIOArguValues = [22050, 1, 320, 0, 'WAVU', 22050, 1, 320] # Temporary. Argument value set for ACZ RADIOUSA files.

ARGU = ['/IF', '/IC', '/II', '/IH', '/OT', '/OF', '/OC', '/OI'] #Contains the core arguments.

currentArguValue = [] #The current set of argument VALUES currently being used.

concatArgu = [] #Concatenated Arguments and values


argumentBuffer = ''

currentArguValue = aczRADIOArguValues


for i in range(len(ARGU)):
    concatArgu.append( ARGU[i] + str(currentArguValue[i]) )

for i in range(len(ARGU)):
    argumentBuffer = argumentBuffer + concatArgu[i] + ' '

argumentBuffer = argumentBuffer + '"' + inputFilename + '"' + ' ' + '"' + outputFilename + '"'


subprocess.run(["MFAudio.exe", argumentBuffer], shell=True)
#subprocess.run( ["MFAudio.exe", '/IF22050 /IC1 /II320 /IH0 /OTWAVU /OF22050 /OC1 /OI320', '"lol.npsf"', '"lol.wav"'], shell=True )
