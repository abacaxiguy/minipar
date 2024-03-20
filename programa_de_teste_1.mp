# Programa cliente servidor de uma calculadora aritmética simples

c_channel calculadora computador_1 computador_2

SEQ
    # depois do SEQ todas as seguintes instruções identadas serão executadas de forma
    # seqüencial

    print("As operações da calculadora são: +, -, *, /")
    operacao = input("Digite a operação desejada: ")
    valor1 = input("Digite o primeiro valor: ")
    valor2 = input("Digite o segundo valor: ")
    calculadora.send(operacao,valor1,valor2)

    # Imprime o resultado via print

    resultado = calculadora.receive()
    print("O resultado da operação é: ")
    print(resultado)