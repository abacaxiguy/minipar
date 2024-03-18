
import sys

from src.lexer import lexer
from src._parser import parser

def interpreter(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            text = ''.join(lines)
            tokens = lexer(text)
            parser(tokens)

    except FileNotFoundError:
        print("Arquivo não encontrado:", filename)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        interpreter(sys.argv[1])
    else:
        print("Uso: python main.py <arquivo>")