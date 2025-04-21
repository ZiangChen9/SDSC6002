import os
import shutil

target_dir = '../../results-Easom/raw_data'

if not os.path.exists(target_dir):
    os.makedirs(target_dir)
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)

            destination_file_path = os.path.join(target_dir, file)

            shutil.copy(file_path, destination_file_path)
            print(f'File {file_path} copied to {destination_file_path}')

print('All CSV files have been copied.')
