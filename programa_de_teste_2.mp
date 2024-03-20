c_channel calculadora computador_1 computador_2

SEQ
    calculo = calculadora.receive()
    resultado = calculadora.calculate(calculo)
    calculadora.send(resultado)