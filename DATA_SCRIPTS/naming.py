import os

#set working directory to 04-DATA WIP (TO CLEAN)\Airbnb\Tas\Summary
os.chdir('04-DATA WIP (TO CLEAN)/Airbnb/Tas/Calendar/Fix')

#list all files in directory
files = os.listdir()

#add 'Tas_' to start of each file name
for file in files:
    split = file.split('_', 1)
    #overwrite file name with split[1]
    os.rename(file, split[1])

