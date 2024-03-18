
import sys
import threading

from src.lexer import lexer
from src._parser import parser


# Função principal do interpretador
def interpreter(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            text = ''.join(lines)
            tokens = lexer(text)
            parser(tokens)

    except FileNotFoundError:
        print("Arquivo não encontrado:", filename)

# Testando o interpretador
interpreter(sys.argv[1])