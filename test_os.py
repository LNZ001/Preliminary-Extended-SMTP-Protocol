import os
import json

# print("1:",os.path.join('aaaa','/bbbb','ccccc.txt'))
#
# print("2:",os.path.join('/aaaa','/bbbb','/ccccc.txt'))
#
# print("3:",os.path.join('aaaa','./bbb','ccccc.txt'))

# with open('./auth.json', 'r') as load_f:
#     test = json.load(load_f)
#     print(repr(test))
# with open('./auth.json', 'r') as load_f:
#     auth = json.load(load_f)
#     if auth.get('lnz', None) == '123':
#         owner = 'lnz'
#         print('250 OK')
#     else:
#         print('599 FAIL')
import time
data = [b'123',b'345',b'4556']
with open('/home/lnz/Workspace/email/15181059110@lnz.com/new/1550750966.1789703.txt', 'w', encoding="UTF-8") as file:
    for x in data:
        file.write(x.decode())