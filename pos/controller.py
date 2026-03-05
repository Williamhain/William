# controller.py

class Controller:
    def __init__(self):
        self._logged_in = False #set log-in flag initially to false (user is not logged in)

    def logout(self):
        if not self._logged_in: #if not logged in, do nothing
            return False #logout fails because user isn't logged in
        self._logged_in = False #set to logged out
        return True #succesfully completed the self.assertTrue(self.controller.logout())
    
    def login(self, username, password):

        if self._logged_in: #already logged in
            return False #login attempt fails because user is already logged in

        if username == "user" and password == "pos2026": #should be user, not "theuser"
            self._logged_in = True #user is now logged in successfully
            return True #login succeeds
        return False #login fails because of incorrect username or password
    
