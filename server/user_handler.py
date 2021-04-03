"""
json and os are used modules
"""
import json
import os

class UserHandler():
    """
    User login, register and logout handler
    """
    def __init__(self, user, passw):
        self.user = user
        self.passw = passw

        with open('users_data.json') as data:
            self.users_data = json.loads(data.read())
            self.all_users = list(self.users_data)

    def update(self): # when we call this method we are saving the changes made with the database
        """
        update the database
        """
        with open('users_data.json', 'w+') as data:
            json.dump(self.users_data, data, indent=4) # SAVING it

    def register(self): # where new clients will register
        """
        register a new user
        """
        if self.user in self.all_users:
            return "User with this username found"

        self.users_data[self.user] = {"passw":self.passw, "status":"ON"}
        self.update()
        os.mkdir(f'./DataBase/{self.user}') # created a folder for the client
        self.user = self.user

        return "Successfully Registered" # DOne!!

    def login(self): # where clients login
        """
        login a user
        """
        if self.user not in self.all_users:
            return "User Not Found"

        true_passw = self.users_data[self.user]['passw']
        if true_passw != self.passw:
            return "Password Not Correct"

        status = self.users_data[self.user]['status']
        if status == "ON":
            """
            This is when use is trying to login while it is logged in from other device.
            """
            return "This user is logged in with other account"

        self.users_data[self.user]['status'] = 'ON'
        self.update()
        self.user = self.user

        return "Successfully Logged In"

    def register_second(self, user, passw):
        """
        this method is when clients try to register while they are passing commands
        register <username> <password>
        """
        if user in self.all_users:
            return ["","User with this username found"]

        self.users_data[self.user]["status"] = "OFF"

        self.users_data[user] = {"passw":passw, "status":"ON"}
        self.update()
        os.mkdir(f'./DataBase/{user}') # created a folder for the client
        self.user = user

        return [self.user,"Successfully Registered"]

    def login_second(self, user, passw):
        """
        this method is when clients try to login while they are passing commands
        login <username> <password>
        """
        if user not in self.all_users:
            return ["","User Not Found"]

        true_passw = self.users_data[user]['passw']
        if true_passw != passw:
            return ["","Password Not Correct"]

        status = self.users_data[user]['status']
        if status == "ON":
            return ["","This user is logged in with other account"]

        self.users_data[user]['status'] = 'ON'
        self.users_data[self.user]["status"] = "OFF"
        self.update()
        self.user = user

        return [self.user,"Successfully Logged In"]

    def logout(self):
        """
        logout the user
        """
        # this is a logout method
        self.users_data[self.user]['status'] = 'OFF'
        self.update()
        