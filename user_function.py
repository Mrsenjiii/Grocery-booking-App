
from app import *


def authentication(username, password, user_list):
    for user in user_list:
        if user.user_name == username and user.user_password == password:
            return True
    return False
