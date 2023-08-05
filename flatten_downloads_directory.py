import os
import shutil


def flatten_dir(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            source = os.path.join(root, file)
            destination = os.path.join(root_dir, file)

            # Only move if the file doesn't exist in the destination already
            if not os.path.exists(destination):
                shutil.move(source, destination)
            else:
                print(f'Skipped file {source} because it already exists in {destination}.')

def remove_empty_dirs(root_dir):
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for name in dirs:
            try:
                os.rmdir(os.path.join(root, name))
            except OSError:
                print(f"Directory {os.path.join(root, name)} not removed. It may not be empty.")

if __name__ == "__main__":
    directory = './data/downloads'
    flatten_dir(directory)
    remove_empty_dirs(directory)