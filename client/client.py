"""
Socket for the connection
pickle for encoding and decoding
"""
import socket
import pickle
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = '127.0.0.1'
PORT = 8088
try:
    client.connect((IP, PORT))
except:
    print("Server not avaliable :(")
    exit()

all_commmands = [
"",
"=> create_folder <foldername> | usage -> Create a new folder inside the current directory.",
"=> write_file <filename> <filedata> | usage -> Create a file and write in the current directory.",
"=> read_file <filename> | usage -> read from an existing file in the current directory.",
"=> .. | usage -> Go back from the current directory.",
"=> change_folder <foldername> | usage -> Change to another directory.",
"=> list | usage -> list all avaliable files and folders inside the current directory.",
"=> register <username> <password> | usage -> Register a new user.",
"=> login <username> <password> | usage -> Login to another user.",
"=> quit | usage -> logout from the server and terminate the code.",
""
]
#------------------------------the initial login and register process----------------
while True:
    print("""
\tFile Server
(1) Register
(2) Login
(3) quit
    """)
    log_choice = input("Enter any option from the above: ")

    if log_choice == '1':
        username = input("Enter a New username: ")
        passw = input("Enter a New password: ")
        all_data = ["Register"]
        all_data.append(username)
        all_data.append(passw)
        all_data = pickle.dumps(all_data)
        client.send(all_data)

        auth_data = client.recv(1024)
        auth_data = pickle.loads(auth_data)
        if auth_data == "Successfully Registered":
            print(auth_data + "\nNow we will log you in to this account!!")
            break

        print(auth_data)
        continue

    elif log_choice == '2':
        username = input("Enter your username: ")
        passw = input("Enter your password: ")
        all_data = ["Login"]
        all_data.append(username)
        all_data.append(passw)
        all_data = pickle.dumps(all_data)
        client.send(all_data)

        auth_data = client.recv(1024)
        auth_data = pickle.loads(auth_data)
        if auth_data == "Successfully Logged In":
            print(auth_data)
            break
        print(auth_data)
        continue

    elif log_choice == '3':
        print("Closed")
        sys.exit()

    else: # if they entered something randomly
        continue

# ------------------actual function started!!-----------------------
try:
    current_dir = f":{username}> "
    while True:
        user_in = input(current_dir) # client input
        if user_in == 'commands':
            print("\n".join(all_commmands))
        elif user_in == 'quit':
            print("Logging out!")
            sys.exit()
        else:
            user_in = pickle.dumps(user_in)
            client.send(user_in) # sending the client input
            data_recv = client.recv(1024) # receving the request
            data_recv = pickle.loads(data_recv)
            if data_recv[0] != "":
                current_dir = f":{data_recv[0]}> " # changing the current path
            if data_recv[1] != "":
                print(data_recv[1]) # printing the request

except: # if any error occured
    print("Error Occured!")
    sys.exit()
    