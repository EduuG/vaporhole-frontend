import requests
import sys
sys.path.append('dependencies/')
from bs4 import BeautifulSoup


def show():
    # r = requests.get("http://localhost:80/membros.html")
    r = requests.get("https://vaporhole.xyz/last-gopher.html")
    users = []
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        for heading in soup.find_all(attrs={"class": "homepage-link"}):
            users.append(heading.string)

    return users
