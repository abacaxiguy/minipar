import socket

# Definindo exceção para erros de sintaxe
class SyntaxError(Exception):
    pass

# Tokens
tokens = [
    'PRINT',
    'DOT',
    'SEND',
    'RECEIVE',
    'OPERATOR',
    'FLOAT',
    'INTEGER',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'STRING',
    'ASSIGN',
    'EQUALS',
    'DIFFERENT',
    'GREATER',
    'LESS',
    'GREATEREQUAL',
    'LESSEQUAL',
    'AND',
    'OR',
    'NOT',
    'IF',
    'ELSE',
    'WHILE',
    'FUNCTION',
    'RETURN',
    'INPUT',
    'IDENTIFIER'
]


# Função para análise sintática
def parser(tokens):
    # Índice do token atual
    current_token = 0
    variables = {}

    # Função para obter o próximo token
    def get_next_token():
        nonlocal current_token
        current_token += 1
        if current_token < len(tokens):
            return tokens[current_token]
        return None

    # Função para verificação de tokens
    def match(token_type):
        nonlocal current_token
        print(token_type, tokens[current_token][0])
        if current_token < len(tokens) and tokens[current_token][0] == token_type:
            return True
        return False

    def parse_print():
        if match('LPAREN'):
            get_next_token()
            if match('STRING'):
                string = get_next_token()[1]
                if match('RPAREN'):
                    get_next_token()
                else:
                    raise SyntaxError("Esperado ')' após STRING")
            else:
                raise SyntaxError("Esperado STRING após '('")
        else:
            raise SyntaxError("Esperado '(' após PRINT")

        print(string)

    def parse_send():
        if match('LPAREN'):
            get_next_token()  # Consumir token LPAREN
            if match('IDENTIFIER'):
                get_next_token()  # Consumir token IDENTIFIER
                if match('COMMA'):
                    get_next_token()  # Consumir token COMMA
                    if match('INTEGER') or match('FLOAT'):
                        get_next_token()  # Consumir token INTEGER ou FLOAT
                        if match('COMMA'):
                            get_next_token()  # Consumir token COMMA
                            if match('INTEGER') or match('FLOAT'):
                                get_next_token()  # Consumir token INTEGER ou FLOAT
                                if match('RPAREN'):
                                    get_next_token()  # Consumir token RPAREN
                                else:
                                    raise SyntaxError("Esperado ')' após valor")
                            else:
                                raise SyntaxError("Esperado INTEGER ou FLOAT após COMMA")
                        else:
                            raise SyntaxError("Esperado COMMA após valor")
                    else:
                        raise SyntaxError("Esperado INTEGER ou FLOAT após COMMA")
                else:
                    raise SyntaxError("Esperado COMMA após IDENTIFIER")
            else:
                raise SyntaxError("Esperado IDENTIFIER após '('")
        else:
            raise SyntaxError("Esperado '(' após SEND")

    def parse_receive():
        if match('LPAREN'):
            get_next_token() # Consumir token LPAREN
            if match('IDENTIFIER'):
                get_next_token() # Consumir token IDENTIFIER
                if match('RPAREN'):
                    get_next_token() # Consumir token RPAREN
                else:
                    raise SyntaxError("Esperado ')' após IDENTIFIER")
            else:
                raise SyntaxError("Esperado IDENTIFIER após '('")
        else:
            raise SyntaxError("Esperado '(' após RECEIVE")

    def parse_input():
        if match('LPAREN'):
            get_next_token() # Consumir token LPAREN
            if match('STRING'):
                string = get_next_token()[1]
                if match('RPAREN'):
                    get_next_token() # Consumir token RPAREN
                else:
                    raise SyntaxError("Esperado ')' após STRING")
            else:
                raise SyntaxError("Esperado STRING após '('")
        else:
            raise SyntaxError("Esperado '(' após INPUT")

        value = input(string)
        print(value)
        return value

    def parse_while():
        if match('LPAREN'):
            get_next_token()  # Consumir token LPAREN
            # Expressão dentro do parêntese do WHILE
            expression()
            if match('RPAREN'):
                get_next_token()  # Consumir token RPAREN
                # Corpo do WHILE
                expression()
            else:
                raise SyntaxError("Esperado ')' após expressão do WHILE")
        else:
            raise SyntaxError("Esperado '(' após WHILE")

    def parse_c_channel():
        if match('IDENTIFIER'):
            channel = get_next_token()[1]
            variables[channel] = None
            get_next_token()
            if match('IDENTIFIER'):
                pc_1 = get_next_token()[1]
                get_next_token()
                if match('IDENTIFIER'):
                    pc_2 = get_next_token()[1]
                    get_next_token()

        # criar socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # conectar ao servidor
        s.connect(('localhost', 12335))

        print(f'Conectado ao servidor {variables[channel]} na porta 12345')

    # Função para expressão
    def expression():
        nonlocal current_token
        if match('SEQ'):
            get_next_token()
            while current_token < len(tokens) and not match('PAR'):
                expression()
        elif match('PAR'):
            get_next_token()
            while current_token < len(tokens) and not match('SEQ'):
                expression()
        elif match('PRINT'):
            get_next_token() # Consumir token PRINT
            parse_print()
        elif match('INPUT'):
            get_next_token() # Consumir token INPUT
            parse_input()
        elif match('IF'):
            get_next_token()  # Consumir token IF
            if match('LPAREN'):
                get_next_token()  # Consumir token LPAREN
                # Expressão dentro do parêntese do IF
                expression()
                if match('RPAREN'):
                    get_next_token()  # Consumir token RPAREN
                    # Corpo do IF
                    expression()
                    if match('ELSE'):
                        get_next_token()  # Consumir token ELSE
                        # Corpo do ELSE
                        expression()
                else:
                    raise SyntaxError("Esperado ')' após expressão do IF")
            else:
                raise SyntaxError("Esperado '(' após IF")
        elif match('WHILE'):
            get_next_token()  # Consumir token WHILE
            parse_while()
        elif match('C_CHANNEL'):
            get_next_token()  # Consumir token C_CHANNEL
            parse_c_channel()
        elif match('IDENTIFIER'):
            get_next_token()  # Consumir token IDENTIFIER
            if match('DOT'):
                get_next_token()
                if match('SEND'):
                    get_next_token() # Consumir token SEND
                    parse_send()
                elif match('RECEIVE'):
                    get_next_token() # Consumir token RECEIVE
                    parse_receive()
            if match('ASSIGN'):
                get_next_token()  # Consumir token ASSIGN
                expression()  # Expressão do lado direito da atribuição
        else:
            raise SyntaxError("Comando inválido")

    # Analisar expressão
    try:
        expression()
        if current_token < len(tokens):
            raise SyntaxError("Tokens extras após o comando válido")
    except SyntaxError as e:
        return str(e)

    return "Análise sintática bem-sucedida."

