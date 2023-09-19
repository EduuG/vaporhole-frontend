# Uma espécie de frontend para o servidor
# Sou aprendiz em programação, não liguem pra qualidade do código :P
# By: "eduuG"

from os import system
from time import sleep, strftime, localtime
from textwrap import wrap
from colorama import Fore, Back, Style
import quantidade_membros


def validar_resposta(pergunta, opcoes):
    while True:
        try:
            resp = int(input(pergunta))

            if resp < 0 or resp > opcoes:
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
    print_delay("                               Membros: {}".format(exibir_quantidade_membros))
    print_delay("")
    f = open('/home/eduuG/Scripts/vaporhole_frontend/ascii', 'r')
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


def twtxt():
    system("clear")
    ascii("Twtxt")
    while True:
        print_delay("[1] Tweet")
        print_delay("[2] Exibir tweets mais recentes")
        print_delay("[3] Quem você está seguindo")

        print_delay("\n[0] Voltar")

        resp = validar_resposta("\nR: ", 3)

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
    print_delay(("[1] Chat de conversa"))
    print_delay("[2] Fórum")
    print_delay("[3] E-mail")
    print_delay("[4] Browser")
    print_delay("[5] Twtxt")
    print_delay("\n[6] Sobre")
    print_delay("\n[0] Sair")

    resp = validar_resposta("\nR: ", 6)

    if resp == 1:
        system("chat")

    elif resp == 2:
        system("iris")

    elif resp == 3:
        system("mutt")

    elif resp == 4:
        while True:
            ascii("Selecione o browser")
            print_delay("[1] lynx")
            print_delay("[2] w3m")
            print_delay("\n[0] Voltar")
            resp = validar_resposta("\nR: ", 2)

            if resp == 1:
                system("lynx")

            elif resp == 2:
                system("w3m duckduckgo.com")

            elif resp == 0:
                break

    elif resp == 6:
        while True:
            ascii("Sobre")
            text_file = open("/home/eduuG/Scripts/vaporhole_frontend/sobre", 'r')
            data = text_file.read()
            text_file.close()

            sobre = wrap(data, width=50, break_long_words=False,replace_whitespace=False)
            for i in sobre:
                print(i)

            print_delay("\n[0] Voltar")
    
            resp = validar_resposta("\nR: ", 0)

            if resp == 0:
                break

    elif resp == 5:
        while True:
            resp = twtxt()
            
            if resp == 0:
                break

    elif resp == 0:
        print_delay("\n- Até mais! -\n")
        break

