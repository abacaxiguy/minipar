import re

# Definindo os tokens da linguagem
tokens = [
    (r'[ \t\n]+', None),         # Espaços em branco (ignorados)
    (r'#[^\n]*', None),           # Comentários (ignorados)
    (r'print', 'PRINT'),          # Palavra-chave PRINT
    (r'\.', 'DOT'),               # Ponto
    (r'SEQ', 'SEQ'),              # Palavra-chave SEQ
    (r'PAR', 'PAR'),              # Palavra-chave PAR
    (r'c_channel', 'C_CHANNEL'),  # Palavra-chave C_CHANNEL
    (r'send', 'SEND'),            # Palavra-chave SEND
    (r'receive', 'RECEIVE'),      # Palavra-chave RECEIVE
    (r'calculate', 'CALCULATE'),  # Palavra-chave CALCULATE
    (r'[\+\-\*/]', 'OPERATOR'),   # Operadores aritméticos
    (r'\d+\.\d+', 'FLOAT'),       # Números decimais
    (r'\d+', 'INTEGER'),          # Números inteiros
    (r'\(', 'LPAREN'),            # Parêntese esquerdo
    (r'\)', 'RPAREN'),            # Parêntese direito
    (r',', 'COMMA'),              # Vírgula
    (r'\".*?\"', 'STRING'),       # Strings
    (r'=', 'ASSIGN'),             # Atribuição
    (r'==', 'EQUALS'),            # Igualdade
    (r'!=', 'DIFFERENT'),         # Diferença
    (r'>', 'GREATER'),            # Maior que
    (r'<', 'LESS'),               # Menor que
    (r'>=', 'GREATEREQUAL'),      # Maior ou igual
    (r'<=', 'LESSEQUAL'),         # Menor ou igual
    (r'and', 'AND'),              # Operador lógico AND
    (r'or', 'OR'),                # Operador lógico OR
    (r'not', 'NOT'),              # Operador lógico NOT
    (r'if', 'IF'),                # Palavra-chave IF
    (r'else', 'ELSE'),            # Palavra-chave ELSE
    (r'while', 'WHILE'),          # Palavra-chave WHILE
    (r'function', 'FUNCTION'),    # Palavra-chave FUNCTION
    (r'return', 'RETURN'),        # Palavra-chave RETURN
    (r'input', 'INPUT'),          # Palavra-chave INPUT
    (r'\w+', 'IDENTIFIER'),       # Identificadores (palavras)
]

# Função para analisar o texto de entrada
def lexer(text):
    tokens_list = []
    pos = 0

    while pos < len(text):
        match = None
        for token_regex, token_type in tokens:
            pattern = re.compile(token_regex)
            match = pattern.match(text, pos)
            if match:
                value = match.group(0)
                if token_type:
                    tokens_list.append((token_type, value))
                break
        if not match:
            raise SyntaxError(f"Token desconhecido: '{text[pos]}'")
        else:
            pos = match.end(0)
    
    return tokens_list


