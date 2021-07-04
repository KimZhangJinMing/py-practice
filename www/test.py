import asyncio

from www import User
from www.db.Mysql import *

loop = asyncio.get_event_loop()
config_dict = {'user':'root','password':'123','db':'py_practice'}
create_pool(loop,**config_dict)


def findUser():
    user = User.find('1')
    print(user)

if __name__ == '__main__':
    findUser()