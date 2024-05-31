menu = """

=========== Banco Dio ===========
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

==> """

saldo = 0.0
limite = 500.00
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "d":
        print("Deposito")
        valor = float(input("informe o valor do deposito: "))
        if valor > 0:
            saldo += valor
            extrato += f"Deposito: R$ {valor:.2f}\n"
        else:
            print("Operacao falhou! valor informado e invalido.")

    elif opcao == "s":
        print("Sacar")
        valor = float(input("Informe o valor do saque: "))

        if valor > saldo:
            print("\nOperacao falhou! Voce nao tem saldo suficiente.")

        elif valor > limite:
            print("\nOperacao falhou! Valor excedeu o limite do saque diario.")

        elif numero_saques >= LIMITE_SAQUES:
            print("\nOperacao falhou! Voce excedeu o numero de saques diarios.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operacao falhou! valor informado e invalido.")

    elif opcao == "e":
        print("=========== Extrato ===========")
        print("Nao foram realizadas movimentacoes." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}\n")
        print("===============================")

    elif opcao == "q":
        print("\nFinalizando...")
        break

    else:
        print("\nOperacao Invalida, por favor selecione novamente a operacao desejada.")