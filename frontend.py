# Uma espécie de frontend para o servidor
# By: "eduuG"

import os
from getpass import getuser
from time import sleep, strftime, localtime
from textwrap import wrap
from colorama import Fore, Back, Style
import quantidade_membros
import last_gopher
import sys
import re
import importlib


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


def ascii(subtitulo):
    os.system("clear")
    print_delay(" {}".format(curr_time), breakline=False)
    print_delay("{} Membros: {}".format(' ' * 32, exibir_quantidade_membros))
    print_delay("")
    f = open('ascii', 'r')
    content = f.read()
    print_delay(Fore.GREEN + content + Style.RESET_ALL)
    f.close()

    separador(Fore.BLUE + subtitulo + Style.RESET_ALL)
    print_delay("")


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
            print(exibir, end=' ')
            sleep(tempo)

        else:
            print(exibir)
            sleep(tempo)
    else:
        if not breakline:
            print(exibir, end=' ')
            sleep(tempo_delay)

        else:
            print(exibir)
            sleep(tempo_delay)


def add_option(option, exit=False, breakline=False):
    if exit:
        options.insert(0, option)

    else:
        if breakline:
            options.append("{}\n".format(option))
        else:
            options.append(option)


def show_options():
    for i in options:
        if i != "Sair" and i != "Voltar":
            print_delay("[{}] {}".format(options.index(i), i))
        if "\n" in i:
            options[options.index(i)] = i[:-1]
    print_delay("\n[{}] {}".format('0', options[0]))


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
        ascii("Opções")
        if user_settings.DEFAULT_BROWSER == '':
            add_option("Browser padrão: DEFINIR")
        else:
            add_option("Browser padrão: {}".format(user_settings.DEFAULT_BROWSER))
        add_option("Voltar", exit=True)
        show_options()

        resp = validar_resposta("\nR: ")

        if (options[resp] == "Browser padrão: DEFINIR" or
           options[resp] == "Browser padrão: {}".format
           (user_settings.DEFAULT_BROWSER)):

            while True:
                options = []
                print_delay("")
                separador(Fore.GREEN + "Definir browser padrão" + Style.RESET_ALL, tipo='+')
                print_delay("")
                add_option("lynx")
                add_option("w3m")
                add_option("Voltar", exit=True)
                show_options()

                resp = validar_resposta("\nR: ")

                if resp == options.index("lynx"):
                    config("DEFAULT_BROWSER", 'lynx')
                    break

                elif resp == options.index("w3m"):
                    config("DEFAULT_BROWSER", 'w3m')
                    break

                elif resp == 0:
                    break

        elif resp == 0:
            break


def twtxt():
    while True:
        os.system("clear")
        ascii("Twtxt")

        global options
        options = []
        add_option("Tweet")
        add_option("Exibir tweets mais recentes")
        add_option("Quem você está seguindo")
        add_option("Voltar", exit=True)
        show_options()

        resp = validar_resposta("\nR: ")

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


def acessar_gopher():
    while True:
        global options
        options = []
        ascii("Acessar Gopher")
        add_option("Seu Gopher Hole")
        add_option("Gopher Holes atualizados recentemente >")
        add_option("Gopher Holes de outros usuários >")
        add_option("Voltar", exit=True)
        show_options()

        resp = validar_resposta("\nR: ")

        if resp == options.index("Seu Gopher Hole"):
            os.system("clear")

            if user_settings.DEFAULT_BROWSER == 'lynx':
                os.system("lynx gopher://vaporhole.xyz/1/~{}".format(user))

            elif user_settings.DEFAULT_BROWSER == 'w3m':
                os.system("w3m gopher://vaporhole.xyz/1/~{}".format(user))

        elif resp == options.index("Gopher Holes atualizados recentemente >"):
            while True:
                ascii("Gopher Holes atualizados")
                options = []
                gopher_list = last_gopher.show()
                for users in gopher_list:
                    add_option(users)
                add_option("Voltar", exit=True)
                show_options()

                resp = validar_resposta("\nR: ")

                for users in options:
                    if resp == options.index(users) and resp != 0:
                        os.system("{} gopher://vaporhole.xyz/1/~{}".format(user_settings.DEFAULT_BROWSER, users))

                if resp == 0:
                    break

        elif resp == 0:
            break


separador_tamanho = 60
tempo_delay = 0.05
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
    print_delay("")
    ascii("O que deseja fazer?")
    options = []

    add_option("Chat de conversa")
    add_option("Fórum")
    add_option("E-mail")
    add_option("Browser >")
    add_option("Twtxt >")
    add_option("Games >", breakline=True)
    add_option("Acessar Gopher >")
    add_option("Acessar Web >", breakline=True)
    add_option("Opções >")
    add_option("Sobre")
    add_option("Sair", exit=True)
    show_options()

    resp = validar_resposta("\nR: ")

    if resp == options.index("Chat de conversa"):
        os.system("chat")

    elif resp == options.index("Fórum"):
        os.system("iris")

    elif resp == options.index("E-mail"):
        os.system("mutt")

    elif resp == options.index("Browser >"):
        while True:
            ascii("Selecione o browser")
            options = []
            add_option("lynx")
            add_option("w3m")
            add_option("Voltar", exit=True)
            show_options()
            resp = validar_resposta("\nR: ")

            if resp == 1:
                os.system("lynx")

            elif resp == 2:
                os.system("w3m duckduckgo.com")

            elif resp == 0:
                break

    elif resp == options.index("Sobre"):
        while True:
            ascii("Sobre")
            text_file = open("sobre", 'r')
            data = text_file.read()
            text_file.close()

            sobre = wrap(data, width=50, break_long_words=False,
                         replace_whitespace=False)
            for i in sobre:
                print(i)

            options = []
            add_option("Voltar")
            show_options()

            resp = validar_resposta("\nR: ")

            if resp == 0:
                break

    elif resp == options.index("Twtxt >"):
        while True:
            resp = twtxt()

            if resp == 0:
                break

    elif resp == options.index("Games >"):
        while True:
            ascii("Games")
            options = []
            add_option("Tron")
            add_option("Wargames")
            add_option("Telehack")
            add_option("MudShell")
            add_option("Voltar", exit=True)
            show_options()

            resp = validar_resposta("\nR: ")

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

            elif resp == 0:
                break

    elif resp == options.index("Opções >"):
        settings()

    elif resp == options.index("Acessar Gopher >"):
        acessar_gopher()

    elif resp == 0:
        print_delay("\n- Até mais! -\n")
        break
