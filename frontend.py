# Uma espécie de frontend para o servidor
# By: "eduuG"

from os import system
from time import sleep, strftime, localtime
from textwrap import wrap
from colorama import Fore, Back, Style
import quantidade_membros


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
    system("clear")
    print_delay(" {}".format(curr_time), breakline=False)
    print_delay("{} Membros: {}".format(' ' * 32, exibir_quantidade_membros))
    print_delay("")
    f = open('/home/eduuG/Scripts/vaporhole-frontend/ascii', 'r')
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
# e também sua aparência (se usará "-" ou "+").
def separador(titulo='', limite=0, tipo=0):
    if titulo:
        titulo = ("{}{}{}".format(' ', titulo, ' '))
        titulo_original = titulo

        # Se o parâmetro "limite" não for informado, ele
        # usará o tamanho padrão armazenado
        # na variável "separador_tamanho".
        if not limite:
            i = 0
            while len(titulo) < separador_tamanho:
                titulo = ("{}{}{}".format('-' * i, titulo_original, '-' * i))
                i += 1

            if len(titulo) == (separador_tamanho + 1):
                titulo = titulo[:-1]

        # Se não, usará o tamanho informado no parâmetro.
        else:
            i = 0
            while len(titulo) < limite:
                titulo = ("{}{}{}".format('-' * i, titulo, '-' * i))
                i += 1

            if len(titulo) == (limite + 1):
                titulo = titulo[:-1]

        print_delay(titulo)
    else:
        # Se o tipo não for informado, ele usará a aparência padrão de "-".
        if not tipo:
            if not limite:
                print_delay('-' * separador_tamanho)
            else:
                print_delay('-' * limite)
        elif tipo == 1:
            if not limite:
                print_delay('+' * separador_tamanho)
            else:
                print_delay('+' * limite)


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


def twtxt():
    system("clear")
    ascii("Twtxt")
    while True:
        add_option("Tweet")
        add_option("Exibir tweets mais recentes")
        add_option("Quem você está seguindo")
        add_option("Voltar", exit=True)
        show_options()

        resp = validar_resposta("\nR: ")

        if resp == 1:
            tweet = input("\nFaça seu tweet: ")
            system("twtxt tweet '{}'".format(tweet))
            print_delay("\nTweet realizado com sucesso!")
            sleep(3)
            continue

        elif resp == 2:
            system("twtxt timeline | less")

        elif resp == 3:
            system("twtxt following | cut -d '>' -f2 | cut -d ' ' -f2 | less")

        return resp


separador_tamanho = 60
tempo_delay = 0.1

while True:
    curr_time = strftime("%H:%M", localtime())
    exibir_quantidade_membros = quantidade_membros.exibir()
    sleep(tempo_delay)
    print_delay("")
    ascii("O que deseja fazer?")
    sleep(tempo_delay)
    options = []

    add_option("Chat de conversa")
    add_option("Fórum")
    add_option("E-mail")
    add_option("Browser")
    add_option("Twtxt", breakline=True)
    add_option("Sobre")
    add_option("Sair", exit=True)
    show_options()

    resp = validar_resposta("\nR: ")

    if resp == options.index("Chat de conversa"):
        system("chat")

    elif resp == options.index("Fórum"):
        system("iris")

    elif resp == options.index("E-mail"):
        system("mutt")

    elif resp == options.index("Browser"):
        while True:
            ascii("Selecione o browser")
            options = []
            add_option("lynx")
            add_option("w3m")
            add_option("Voltar", exit=True)
            show_options()
            resp = validar_resposta("\nR: ")

            if resp == 1:
                system("lynx")

            elif resp == 2:
                system("w3m duckduckgo.com")

            elif resp == 0:
                break

    elif resp == options.index("Sobre"):
        while True:
            ascii("Sobre")
            text_file = open("/home/eduuG/Scripts/vaporhole-frontend/sobre", 'r')
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

    elif resp == options.index("Twtxt"):
        while True:
            options = []
            resp = twtxt()

            if resp == 0:
                break

    elif resp == 0:
        print_delay("\n- Até mais! -\n")
        break
