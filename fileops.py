import os
import tarfile

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        os.chown(folder, os.getuid(), os.getgid())
        print("Directory " , folder ,  " Created ")
    else:    
        print("Directory " , folder ,  " already exists") 

def create_file(filename):
    file = Path(filename)
    file.touch(exist_ok=True)

def extract_tarball(tarball_path):
    if not os.path.isfile(tarball_path):
        print(f"File {tarball_path} does not exist.")
        return
    with tarfile.open(tarball_path, "r:*") as tar:
        tar.extractall()
    print("Tarball extracted successfully.")

def delete_file(file_path):
    os.remove(file_path)
    print(f"File {file_path} deleted successfully.")

def move_to_install_folder(path):
    os.chdir(path)
    print(f"Moved to {path} successfully.")