#!/bin/python
# Um frontend para o VaporHole
# By: "eduuG"

import sys
import os
from getpass import getuser
from time import sleep, strftime, localtime
from textwrap import wrap
from colorama import Fore, Back, Style
from simple_term_menu import TerminalMenu
import quantidade_membros
import last_gopher
import last_web
import re
import importlib


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def validar_resposta(pergunta):
    while True:
        try:
            resp = int(input(pergunta))

            if resp >= len(options):
                print_delay("\n- Valor inválido -", 3)
                continue
            else:
                break

        except ValueError:
            print_delay("\n- Valor inválido -", 3)
            continue

        except KeyboardInterrupt:
            print_delay("\n- Até mais! -\n")
            exit()

    return resp


def ascii(subtitulo, animation=False):
    os.system("clear")
    ascii_path = resource_path("ascii")
    f = open(ascii_path, 'r')

    if animation:
        print_delay(" {}".format(curr_time), breakline=False)
        print_delay("{} Membros: {}".format(' ' * 33, exibir_quantidade_membros))
        print_delay("")

        content = f.readlines()
        for line in content:
            print_delay(Fore.GREEN + line + Style.RESET_ALL, breakline=False)

        print_delay("")
        separador(Fore.BLUE + subtitulo + Style.RESET_ALL)
        print_delay("")

    else:
        print(" {}".format(curr_time), end=' ')
        print("{} Membros: {}".format(' ' * 32, exibir_quantidade_membros))
        print("")

        content = f.read()
        print(Fore.GREEN + content + Style.RESET_ALL)

        separador(Fore.BLUE + subtitulo + Style.RESET_ALL)
        print("")

    f.close()

    return subtitulo


# Função para realçar a apresentação do programa
def realce(titulo):
    print("{}{}{}".format('+', '-' * (len(titulo) + 2), '+'))
    print("{}{}{}".format('| ', titulo, ' |'))
    print("{}{}{}".format('+', '-' * (len(titulo) + 2), '+'))


# Função que permite criar separadores de maneira dinâmica,
# alterando seu tamanho, se deve conter um título ou não,
# e também sua aparência.
def separador(titulo='', limite=0, tipo='-'):
    if titulo:
        titulo = ("{}{}{}".format(' ', titulo, ' '))
        titulo_original = titulo

        # Se o parâmetro "limite" não for informado, ele
        # usará o tamanho padrão armazenado
        # na variável "separador_tamanho".
        if not limite:
            i = 0
            while len(titulo) < separador_tamanho:
                titulo = ("{}{}{}".format(tipo * i, titulo_original, tipo * i))
                i += 1

            if len(titulo) == (separador_tamanho + 1):
                titulo = titulo[:-1]

        # Se não, usará o tamanho informado no parâmetro.
        else:
            i = 0
            while len(titulo) < limite:
                titulo = ("{}{}{}".format(tipo * i, titulo, tipo * i))
                i += 1

            if len(titulo) == (limite + 1):
                titulo = titulo[:-1]

        print_delay(titulo)
    else:
        if not limite:
            print_delay(tipo * separador_tamanho)
        else:
            print_delay(tipo * limite)


# Função para tornar a exibição do programa menos abrupta.
# Ele utiliza da variável "tempo_delay" para determinar a
# velocidade em que os textos serão exibidos.
def print_delay(exibir, tempo=0, breakline=True):
    if tempo:
        if not breakline:
            print(exibir, end='')
            sleep(tempo)

        else:
            print(exibir)
            sleep(tempo)
    else:
        if not breakline:
            print(exibir, end='')
            sleep(tempo_delay)

        else:
            print(exibir)
            sleep(tempo_delay)


def add_option(option, exit=False, breakline=False):
    raw_options = []

    for i in options:
        if i != "":
            raw_options.append(i)

    if exit:
        if len(raw_options) >= 1:
            options.append("")

        options.append('# ' + option)

    else:
        if option != "":
            if not breakline:
                options.append('• ' + option)
            else:
                options.append("")
                options.append('• ' + option)


def show_options(subtitulo=''):
    raw_options = []

    for i in options:
        if i != "":
            raw_options.append(i)

    if len(raw_options) > 5:
        for i in options:
            print_delay("  " + i)

        ascii(subtitulo)

    terminal_menu = TerminalMenu(options, skip_empty_entries=True, menu_cursor_style=("fg_purple", "bold"))
    resp = terminal_menu.show()

    for i in options:
        options[options.index(i)] = i[2:]

    return resp


def config(variable, value):
    replace = "{} = '{}'".format(variable, value)

    with open(r'{}'.format(config_path), 'r') as file:
        data = file.read()
        search = re.findall("{} = '{}'".format(variable, '.*?'), data)
        for match in search:
            data = data.replace(match, replace)

    with open(r'{}'.format(config_path), 'w') as file:
        file.write(data)


def settings():
    while True:
        importlib.reload(user_settings)
        global options
        options = []
        subtitulo = ascii("Opções")
        if user_settings.DEFAULT_BROWSER == '':
            add_option("Browser padrão: DEFINIR")
        else:
            add_option("Browser padrão: {}".format(user_settings.DEFAULT_BROWSER))
        add_option("Voltar", exit=True)

        resp = show_options(subtitulo)

        if (options[resp] == "Browser padrão: DEFINIR" or
           options[resp] == "Browser padrão: {}".format
           (user_settings.DEFAULT_BROWSER)):

            for i in options:
                if i != "" and i != "Voltar":
                    print_delay("  * {}".format(i))

                elif i == "Voltar":
                    print_delay("")
                    print_delay("  * Voltar")

            while True:
                options = []
                print_delay("")
                separador(Fore.GREEN + "Definir browser padrão" + Style.RESET_ALL, tipo='+')
                print_delay("")
                add_option("lynx")
                add_option("w3m")
                add_option("Voltar", exit=True)

                resp = show_options()

                if resp == options.index("lynx"):
                    config("DEFAULT_BROWSER", 'lynx')
                    break

                elif resp == options.index("w3m"):
                    config("DEFAULT_BROWSER", 'w3m')
                    break

                elif resp == options.index("Voltar"):
                    break

        elif resp == options.index("Voltar"):
            break


def twtxt():
    while True:
        global options
        options = []

        os.system("clear")
        subtitulo = ascii("Twtxt")

        add_option("Tweet")
        add_option("Exibir tweets mais recentes")
        add_option("Quem você está seguindo")
        add_option("Voltar", exit=True)

        resp = show_options(subtitulo)

        if resp == options.index("Tweet"):
            tweet = input("\nFaça seu tweet: ")
            os.system("twtxt tweet '{}'".format(tweet))
            print_delay("\nTweet realizado com sucesso!")
            sleep(3)
            continue

        elif resp == options.index("Exibir tweets mais recentes"):
            os.system("twtxt timeline | less")

        elif resp == options.index("Quem você está seguindo"):
            os.system("twtxt following | cut -d '>' -f2 | cut -d ' ' -f2 | less")

        return resp


def games():
    while True:
        global options
        options = []

        os.system("clear")
        subtitulo = ascii("Games")

        add_option("Tron")
        add_option("Wargames")
        add_option("Telehack")
        add_option("MudShell")
        add_option("Jogo da Velha (By Al4xs)")
        add_option("Cataclysm: Dark Days Ahead")
        add_option("Voltar", exit=True)

        resp = show_options(subtitulo)

        if resp == options.index("Tron"):
            os.system("clear")
            os.system("tron")

        elif resp == options.index("Wargames"):
            os.system("clear")
            os.system("wargames")

        elif resp == options.index("Telehack"):
            os.system("clear")
            os.system("telehack")

        elif resp == options.index("MudShell"):
            os.system("clear")
            os.system("mudsh")

        elif resp == options.index("Jogo da Velha (By Al4xs)"):
            os.system("jogo-da-velha.py")

        elif resp == options.index("Cataclysm: Dark Days Ahead"):
            os.system("/home/eduuG/Games/cataclysmdda-0.F/cataclysm-launcher")

        elif resp == options.index("Voltar"):
            break


def acessar_gopher():
    while True:
        global options
        options = []
        subtitulo = ascii("Acessar Gopher")
        add_option("Seu Gopher Hole")
        add_option("Gopher Holes atualizados recentemente >")
        add_option("Gopher Hole de outros usuários >")
        add_option("Voltar", exit=True)

        resp = show_options(subtitulo)

        if resp == options.index("Seu Gopher Hole"):
            os.system("clear")
            os.system("{} gopher://vaporhole.xyz/1/~{}".format(user_settings.DEFAULT_BROWSER, user))

        elif resp == options.index("Gopher Holes atualizados recentemente >"):
            while True:
                subtitulo = ascii("Gopher Holes atualizados")
                options = []
                gopher_list = last_gopher.show()
                for users in gopher_list:
                    add_option(users)
                add_option("Voltar", exit=True)

                resp = show_options(subtitulo)

                for users in options:
                    if resp == options.index(users) and resp != options.index("Voltar"):
                        os.system("{} gopher://vaporhole.xyz/1/~{}".format(user_settings.DEFAULT_BROWSER, users))

                if resp == options.index("Voltar"):
                    break

        elif resp == options.index("Gopher Hole de outros usuários >"):
            print("* Ctrl-C para voltar")

            while True:
                try:
                    search_user = input("\nNome do usuário: ")

                except KeyboardInterrupt:
                    break

                if search_user in quantidade_membros.lista():
                    os.system("{} gopher://vaporhole.xyz/1/~{}".format(user_settings.DEFAULT_BROWSER, search_user))

                else:
                    print_delay("\n- Usuário desconhecido -\n", 3)

        elif resp == options.index("Voltar"):
            break


def acessar_web():
    while True:
        global options
        options = []
        subtitulo = ascii("Acessar Web")
        add_option("Pesquisar")
        add_option("Sua página Web", breakline=True)
        add_option("Páginas Web atualizadas recentemente >")
        add_option("Página Web de outros usuários >")
        add_option("Voltar", exit=True)

        resp = show_options(subtitulo)

        if resp == options.index("Pesquisar"):
            os.system("{} duckduckgo.com".format(user_settings.DEFAULT_BROWSER))

        elif resp == options.index("Sua página Web"):
            os.system("clear")
            os.system("{} https://vaporhole.xyz/~{}".format(user_settings.DEFAULT_BROWSER, user))

        elif resp == options.index("Páginas Web atualizadas recentemente >"):
            while True:
                subtitulo = ascii("Páginas Web atualizadas")
                options = []
                web_list = last_web.show()
                for users in web_list:
                    add_option(users)
                add_option("Voltar", exit=True)

                resp = show_options(subtitulo)

                for users in options:
                    if resp == options.index(users) and resp != options.index("Voltar"):
                        os.system("{} https://vaporhole.xyz/~{}".format(user_settings.DEFAULT_BROWSER, users))

                if resp == options.index("Voltar"):
                    break

        elif resp == options.index("Página Web de outros usuários >"):
            print("* Ctrl-C para voltar")

            while True:
                try:
                    search_user = input("\nNome do usuário: ")

                except KeyboardInterrupt:
                    break

                if search_user in quantidade_membros.lista():
                    os.system("{} https://vaporhole.xyz/~{}".format(user_settings.DEFAULT_BROWSER, search_user))

                else:
                    print_delay("\n- Usuário desconhecido -\n", 3)

        elif resp == options.index("Voltar"):
            break


separador_tamanho = 60
tempo_delay = 0.03
options = []
user = getuser()
config_path = "/home/{}/Frontend/user_settings.py".format(user)

while True:
    if 'Frontend' in os.listdir("/home/{}/".format(user)):
        pass
    else:
        os.mkdir("/home/{}/Frontend".format(user))
        os.mknod("/home/{}/Frontend/user_settings.py".format(user))

        with (open('default_settings.py', 'r') as file1,
              open(config_path, 'a') as file2):

            for line in file1:
                file2.write(line)

    sys.path.insert(1, "/home/{}/Frontend".format(user))
    import user_settings
    importlib.reload(user_settings)

    curr_time = strftime("%H:%M", localtime())
    exibir_quantidade_membros = quantidade_membros.exibir()
    subtitulo = ascii("O que deseja fazer?", animation=True)
    options = []

    add_option("Chat de conversa")
    add_option("Fórum")
    add_option("E-mail")
    add_option("Twtxt >")
    add_option("Games >")
    add_option("Acessar Gopher >", breakline=True)
    add_option("Acessar Web >")
    add_option("Opções >", breakline=True)
    add_option("Sobre")
    add_option("Sair", exit=True)

    resp = show_options(subtitulo)

    if resp == options.index("Chat de conversa"):
        os.system("chat")

    elif resp == options.index("Fórum"):
        os.system("iris")

    elif resp == options.index("E-mail"):
        os.system("mutt")

    elif resp == options.index("Sobre"):
        while True:
            subtitulo = ascii("Sobre")
            sobre_path = resource_path("sobre")
            text_file = open(sobre_path, 'r')
            data = text_file.read()
            text_file.close()

            sobre = wrap(data, width=50, break_long_words=False,
                         replace_whitespace=False)
            for i in sobre:
                print(i)

            print_delay("")
            options = []
            add_option("Voltar", exit=True)

            resp = show_options(subtitulo)

            if resp == options.index("Voltar"):
                break

    elif resp == options.index("Twtxt >"):
        while True:
            resp = twtxt()

            if resp == options.index("Voltar"):
                break

    elif resp == options.index("Games >"):
        games()

    elif resp == options.index("Opções >"):
        settings()

    elif resp == options.index("Acessar Gopher >"):
        acessar_gopher()

    elif resp == options.index("Acessar Web >"):
        acessar_web()

    elif resp == options.index("Sair"):
        print_delay("\n- Até mais! -\n")
        break
