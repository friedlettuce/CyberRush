# Used to rename groups of frames by ranged input from 0 to frames
# Don't enter in last shown number into counter, aka frame counter
# Must move to directory renaming files in

import os

cwd = os.getcwd()
cwd += '\\'

frames = int(input("Enter number of frames: "))
old_name = input("Enter old name: ")
new_name = input("Enter new name: ")

ext = r'.png'


for frame in range(frames):
    os.rename(cwd + old_name + str(frame) + ext, cwd + new_name + str(frame) + ext)

