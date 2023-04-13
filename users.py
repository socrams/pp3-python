import datetime

class Users:
    def __init__(self, id, name, comments, email, enable, full_name, password, phone = '', 
                status = 1, creations = datetime, creation_user_id = -1, should_reset_password = 0, last_reset_password = datetime, last_change_password = datetime):
        self.id = id
        self.name = name
        self.comments = comments
        self.email = email
        self.enable = enable
        self.full_name = full_name
        self.password = password
        self.phone = phone
        self.status = status
        self.creations = creations
        self.creation_user_id = creation_user_id
        self.should_reset_password = should_reset_password
        self.last_resetpassword = last_reset_password
        self.last_change_password = last_change_password
    
