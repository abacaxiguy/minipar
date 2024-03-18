from server import Server

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
        if current_token < len(tokens) and tokens[current_token][0] == token_type:
            return True
        return False

    def parse_print():
        if match('LPAREN'):
            get_next_token()
            if match('STRING'):
                string = tokens[current_token][1]
                print(string[1:-1]) # Remover aspas
                if match('RPAREN'):
                    get_next_token()
                else:
                    raise SyntaxError("Esperado ')' após STRING")
            else:
                raise SyntaxError("Esperado STRING após '('")
        else:
            raise SyntaxError("Esperado '(' após PRINT")

    def parse_send():
        if match('LPAREN'):
            get_next_token()  # Consumir token LPAREN
            if match('IDENTIFIER'):
                operacao = tokens[current_token][1]
                get_next_token()
                if match('COMMA'):
                    get_next_token()  # Consumir token COMMA
                    if match('INTEGER') or match('FLOAT'):
                        valor1 = tokens[current_token][1]
                        get_next_token()  # Consumir token INTEGER ou FLOAT
                        if match('COMMA'):
                            get_next_token()  # Consumir token COMMA
                            if match('INTEGER') or match('FLOAT'):
                                valor2 = tokens[current_token][1]
                                get_next_token()  # Consumir token INTEGER ou FLOAT
                                if match('RPAREN'):
                                    get_next_token()  # Consumir token RPAREN

                                    # send through server
                                    
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
        print('parse_input')
        if match('LPAREN'):
            get_next_token() # Consumir token LPAREN
            if match('STRING'):
                string = tokens[current_token][1]
                value = input(string)
                print(value)
                if match('RPAREN'):
                    get_next_token() # Consumir token RPAREN
                    return value
                else:
                    raise SyntaxError("Esperado ')' após STRING")
            else:
                raise SyntaxError("Esperado STRING após '('")
        else:
            raise SyntaxError("Esperado '(' após INPUT")

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
            channel = tokens[current_token][1]
            variables[channel] = None
            get_next_token()
            if match('IDENTIFIER'):
                get_next_token()
                if match('IDENTIFIER'):
                    get_next_token()

                    global server
                    server = Server()
                else:
                    raise SyntaxError("Esperado IDENTIFIER após IDENTIFIER")
            else:
                raise SyntaxError("Esperado IDENTIFIER após IDENTIFIER")
        else:
            raise SyntaxError("Esperado IDENTIFIER após C_CHANNEL")

    def parse_assign(identifier):
        variables[identifier] = expression()

    def parse_if():
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

    # Função para expressão
    def expression():
        nonlocal current_token
        print(tokens[current_token])
        if match('SEQ'):
            get_next_token()
            expression()
        elif match('PAR'):
            get_next_token()
            expression()
        elif match('PRINT'):
            get_next_token() # Consumir token PRINT
            parse_print()
        elif match('INPUT'):
            get_next_token() # Consumir token INPUT
            parse_input()
        elif match('IF'):
            get_next_token()  # Consumir token IF
            parse_if()
        elif match('WHILE'):
            get_next_token()  # Consumir token WHILE
            parse_while()
        elif match('C_CHANNEL'):
            get_next_token()  # Consumir token C_CHANNEL
            parse_c_channel()
        elif match('IDENTIFIER'):
            identifier = tokens[current_token][1]
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
                get_next_token() # Consumir token ASSIGN
                parse_assign(identifier)
        else:
            raise SyntaxError("Comando inválido")

    # Analisar expressão
    try:
        print(len(tokens))
        while current_token < len(tokens):
            print(current_token)
            expression()
    except SyntaxError as e:
        return str(e)
