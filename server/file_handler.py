"""
stat used to check the time when folders and file are created.
"""
from stat import ST_CTIME
import os
import time


class FileHandler():
    """
    The file handler class
    """
    def __init__(self, user):
        self.user = user # setting the user
        self.current_dir = f"./DataBase/{self.user}" # setting the user with its directory
        self.current_dir_out = "/".join(self.current_dir.split('/')[2:]) # this is what we print out
        """
        we are sending a list of data [current_path , the actual request]
        this is because for the current_path we are trying to give the
        client in which directory he is now working.
        and the request is the actual thing that the user requested for
        """

    def list_dir(self): # list all folder and files in the current dir
        """
        List all files and folders in the current path
        """
        data = map(lambda name: os.path.join(self.current_dir, name), os.listdir(self.current_dir))
        data = ((os.stat(path), path) for path in data)
        data = ((stat[ST_CTIME], path) for stat, path in data)
        all_files = []
        for cdate, path in sorted(data):
            file = [os.path.basename(path), time.ctime(cdate)]
            all_files.append(file)
        try:
            max_size = len(max([i[0] for i in all_files], key=len))
            main_size=max_size+3
            output = []
            for i in all_files:
                space = " "*(main_size - len(i[0]))
                output.append(f"{i[0]} {space} {i[1]}")
            return [self.current_dir_out, '\n'.join(output)]
        except:
            return [self.current_dir_out, "Empty Folder"]
    def create_dir(self, dir_name): # this will create a new folder
        """
        creates folder
        """
        try:
            os.mkdir(f"{self.current_dir}/{dir_name}")
            self.current_dir = f"{self.current_dir}/{dir_name}"
            self.current_dir_out = "/".join(self.current_dir.split('/')[2:])
            return [self.current_dir_out, ""]
        except:
            return [self.current_dir_out, "Folder with this name is found"]

    def change_dir(self, dir_name): # this will change directory
        """
        changes the current path
        """
        if os.path.isdir(f"{self.current_dir}/{dir_name}") == False:
            return [self.current_dir_out, "Folder with this name is not found"]
        self.current_dir = f"{self.current_dir}/{dir_name}"
        self.current_dir_out = "/".join(self.current_dir.split('/')[2:])
        return [self.current_dir_out, ""]

    def read_file(self,file_name): # this will read a file
        """
        read file
        """
        try:
            file = open(f"{self.current_dir}/{file_name}", 'r')
            file = file.read()
            return [self.current_dir_out, f"\n{file}"]
        except:
            return [self.current_dir_out, "File Not Found"]

    def write_file(self,file_name, data): # this will write a file
        """
        write to a file
        """
        if os.path.isfile(file_name):
            return [self.current_dir_out, "File found with this file name"]
        try:
            file = open(f"{self.current_dir}/{file_name}", 'w')
            file.write(data)
            file.close()
            return [self.current_dir_out, "Successfully written the file"]
        except:
            return [self.current_dir_out, "Error Occured while trying to write the data"]

    def back(self): # go back to the before path
        """
        one step backward the path
        """
        if self.current_dir == f"./DataBase/{self.user}":
            return ["",""]
        current_split = self.current_dir.split('/')
        self.current_dir = '/'.join(current_split[:len(current_split)-1])
        self.current_dir_out = "/".join(self.current_dir.split('/')[2:])
        return [self.current_dir_out, ""]

    def change_user(self,user): # changing the user will passing commands
        """
        change the current user and the path
        """
        self.current_dir = f"./Database/{user}"
        if os.path.isdir(self.current_dir) == False:
            os.mkdir(f"{self.current_dir}/{user}")
        self.user = user
        self.current_dir_out = "/".join(self.current_dir.split('/')[2:])
