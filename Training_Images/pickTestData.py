import os
import random
import shutil

source_dir = r"C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\Edits"
dest_dir = r"C:\Users\aedan\Downloads"

# get a list of all files in the source directory
files = os.listdir(source_dir)

# randomly select 10 files from the list
selected_files = random.sample(files, 10)

# copy the selected files to the destination directory
for file in selected_files:
    src_file = os.path.join(source_dir, file)
    dest_file = os.path.join(dest_dir, file)
    shutil.copy(src_file, dest_file)
