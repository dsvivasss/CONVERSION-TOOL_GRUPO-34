import os

# Rename all files from current directory

files = os.listdir()

for i, file in enumerate(files):
    os.rename(file, f'audio{i}')
    
