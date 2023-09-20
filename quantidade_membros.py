# Script que exibe quantidade de membros do VaporHole
# Créditos ao usuário 'lich' pelo código

import re
import requests

# r = requests.get("http://localhost:80/membros.html")
r = requests.get("http://vaporhole.xyz/membros.html")
reg = re.compile(r"(?<=li>)[\w]+")

members = []

for member in reg.finditer(r.text):
    m = member.group()
    members.append(m)


def exibir():
    return len(members)


def lista():
    return members
