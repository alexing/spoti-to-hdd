import os
import hashlib


def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def delete_duplicate_files(dir_path):
    if not os.path.isdir(dir_path):
        print(f"{dir_path} is not a directory")
        return

    file_hashes = {}
    for foldername, subfolders, filenames in os.walk(dir_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            file_hash = get_file_hash(file_path)
            if file_hash in file_hashes:
                print(f"Duplicate file found: {file_path}")
                os.remove(file_path)
            else:
                file_hashes[file_hash] = file_path

if __name__ == "__main__":
    directory = '/Users/alex/Music/afterglow'
    delete_duplicate_files(directory)