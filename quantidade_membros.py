# Script que exibe quantidade de membros do VaporHole

from os import listdir, popen

def exibir():
    path = "/home/"
    home = listdir(path)

    membros = {}

    for users in home:
        if users != "lost+found" and "basilisco" not in users:
            user_id = popen("id -u {}".format(users)).read()
            membros[users] = user_id

    return len(membros)
