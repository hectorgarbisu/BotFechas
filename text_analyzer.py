# Detects spanish date-like strings
# -*- coding: utf-8 -*-
import sys

week_day = u"lunes martes miercoles miércoles jueves viernes sabado sábado domingo".split()
cardinal = [str(x+1) for x in range(31)]
ordinal = u"primero segundo tercero cuarto quinto sexto séptimo septimo octavo noveno décimo decimo undécimo decimoprimero decimoprimer duodécimo decimosegundo".split()
mes = "enero febrero marzo abril mayo junio julio agosto septiembre setiembre octubre noviembre diciembre".split()

#TODO: a pretty state machine 

class text_analyzer():
    # NOT IMPLEMENTED
    def __init__(self):
            print("soy una clase")

def get_date(msg):
    # NOT IMPLEMENTED
    tokens = msg.split()
    if len(tokens) < 2: 
        return None
    return 2

if __name__ == "__main__":
    from colorama import init, Fore, Back, Style
    init(convert=True)
    mensajes_fechados = \
                    [u"MENSAJES CON FECHA: dos de abril:",
                    u" el cinco de mayo tengo clase de canto ",
                    u" mañana tendré hambre",
                    u" el 04/01 del año que viene milagritos++",
                    u" el lunes te cuento el chiste",
                    u" el 3 de marzo ",
                    u" el domingo fiesta",
                    u" pasado mañana almuerzo con mis padres",
                    u" el jueves primero de enero ",
                    u" el 20 de junio de 1990 no estuvo nada mal",
                    u" el 20/06/1990 no estuvo nada mal"
                    ]

    mensajes_no_fechados = \
                    [u"MENSAJES SIN FECHA",
                    u" hola buenas  ",
                    u" el cuarto número es el 3",
                    u" el 4º número es el 4 segun matlab",
                    u" matlab está loco ",
                    u" tres veces te engañé ",
                    u" mensaje_demasiado_corto",
                    u" en octubre te fuiste",
                    u" 1994 fué, por verdad usuluta, el mejor año de la historia",
                    u" aunque junio de 1990 no estuvo nada mal "
                    ]

    for ii in mensajes_fechados:
        date = get_date(ii)
        color = Fore.GREEN if date else Fore.RED
        print( color + ii + Style.RESET_ALL)

    for ii in mensajes_no_fechados:
        date = get_date(ii)
        color = Fore.RED if date else Fore.GREEN
        print( color + ii + Style.RESET_ALL)

