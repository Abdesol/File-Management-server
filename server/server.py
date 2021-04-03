"""
The below are used libraries
pickle for encoding
json for reading and writing to the database
"""
import socket
import threading
import pickle
import json
import sys
from user_handler import UserHandler # user handler object
from file_handler import FileHandler # data or file handler object



class Serverclass(): # server class
    """
    server class
    """
    def __init__(self,PORT):
        """
        In the below two 'with' methods, we are trying to make all
        clients status off if they are not off.
        this is because if the server code is terminated suddenly
        every data is not changed.
        """
        with open('users_data.json') as user_data: # this
            user_data = json.loads(user_data.read())
            for i in user_data:
                user_data[i]['status'] = "OFF"
        with open('users_data.json', 'w+') as file: # and this
            json.dump(user_data, file, indent=4)
            file.close()

        global_ip = '0.0.0.0'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # created socket object
        self.server.bind((global_ip, PORT)) # preparing to listen
        self.server.listen() # listening
        ip = socket.gethostbyname(socket.gethostname()) # trying to get the server pc ip address
        self.active_clients = [] # where active clients data is stored
        print(f"Server is listening on {ip}:{PORT}")

    def listening(self): # where the server accepts clients
        """
        listening part
        """
        while True:
            try:
                client, _ = self.server.accept() # trying to accept incoming connection
                # passing them to the authorization
                thread = threading.Thread(target=self.authorize, args=(client,))
                thread.start()
            except:
                print("Error Occured!!")
                sys.exit()

    def authorize(self, client): # where we authorize the user.
        """
        In this method we are trying to get password and user name from the client
        and check if he has logged on another pc or if his credinitals are correct
        """
        while True:
            try:
                data = client.recv(1024)
                user_and_pass = pickle.loads(data)
                user = UserHandler(user_and_pass[1], user_and_pass[2])
                if user_and_pass[0] == 'Register': # if user was trying to register
                    auth = user.register()
                    auth_ = pickle.dumps(auth)
                    client.send(auth_)
                    if auth == "Successfully Registered":
                        self.receive(client, user_and_pass[1], user)

                    else:
                        continue
                else: # if user was trying to login
                    auth = user.login()
                    auth_ = pickle.dumps(auth)
                    client.send(auth_)
                    if auth == "Successfully Logged In":
                        self.receive(client, user_and_pass[1], user)
                        break
                    else:
                        continue
            except:
                break

    def receive(self, client, user, user_obj):
        """
        Here we have succesfully authorized the user now we will try to receive any commands
        from the user
        """
        client_info = [client, user]
        self.active_clients.append(client_info)
        print(f"Client '{user} logged in'")
        user_file_obj = FileHandler(user) # the file_handler object
        while True:
            try:
                data = client.recv(1024) # command received from the user
                data = pickle.loads(data)
                # passing the command to the processing
                data_prc = self.data_process(data, user_file_obj, user_obj)
                data_prc = pickle.dumps(data_prc)
                client.send(data_prc) # sending a data that the user requested
            except: # when the client disconnects
                self.active_clients.remove(client_info) # removing it from the active users list
                print(f"Client '{user} logged out'")
                user_obj.logout() #loggin him out
                break # breaking the loop

    def data_process(self, data, file_obj, user_obj):
        """
        Here is a method where data's received from clients is processed
        """
        if data == '..':
            return file_obj.back()
        elif data == 'list':
            return file_obj.list_dir()
        else: # the others condition will be find here
            data = data.split()
            if len(data) == 2:
                if data[0] == 'change_folder':
                    return file_obj.change_dir(data[1])
                elif data[0] == 'read_file':
                    return file_obj.read_file(data[1])
                elif data[0] == 'create_folder':
                    return file_obj.create_dir(data[1])
                else: # no more option is found for it
                    return ["",
                    'Command not Found!\nPlease try to type "commands" to see available commands']
            elif len(data) == 3:
                if data[0] == 'register':
                    reg_data = user_obj.register_second(data[1], data[2])
                    if reg_data[0] != "":
                        file_obj.change_user(reg_data[0])
                    return reg_data

                elif data[0] == 'login':
                    log_data = user_obj.login_second(data[1], data[2])
                    if log_data[0] != "":
                        file_obj.change_user(log_data[0])
                    return log_data

                elif data[0] == "write_file":
                    return file_obj.write_file(data[1], data[2])
                else: # no more option is found for it
                    return ["",
                    'Command not Found!\nPlease try to type "commands" to see available commands']
            else: # no more option is found for it
                return ["",
                'Command not Found!\nPlease try to type "commands" to see available commands']

    def run(self): # the running method
        """
        run the code
        """
        self.listening() # the root processing


PORT = 8088 # port of the server
server = Serverclass(PORT) # the class object
server.run() # class object started working
