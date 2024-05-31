def sacar(*, saldo, extrato):
    LIMITE_SAQUES = 3

    numero_saques = 0
    limite = 500.00

    valor = float(input("Informe o valor do saque: "))

    if valor > saldo:
        print("\nOperacao falhou! Voce nao tem saldo suficiente.")

    elif valor > limite:
        print("\nOperacao falhou! Valor excedeu o limite do saque diario.")

    elif numero_saques == LIMITE_SAQUES:
        print("\nOperacao falhou! Voce excedeu o numero de saques diarios.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n===== Saque realizado com sucesso! =====")

    else:
        print("Operacao falhou! valor informado e invalido.")

    return saldo, extrato


def depositar(saldo, extrato, /):
    valor = float(input("informe o valor do deposito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Deposito:\tR$ {valor:.2f}\n"
        print("\n===== Depósito realizado com sucesso! =====")
    else:
        print("Operacao falhou! valor informado e invalido.")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n=========== Extrato ===========")
    print("Nao foram realizadas movimentacoes." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}\n")
    print("===============================")


def verifica_cliente(cpf, clientes):
    cliente_verificado = [cliente for cliente in clientes if cliente["cpf"] == cpf]
    return cliente_verificado[0] if cliente_verificado else None


def verifica_conta(cpf, contas):
    conta_verificada = [conta for conta in contas if conta["cliente"]["cpf"] == cpf]
    return conta_verificada[0] if conta_verificada else None


def criar_cliente(clientes):
    cpf = input("informe seu cpf com apenas numero: ")
    cliente = verifica_cliente(cpf, clientes)

    if cliente:
        print("\n===== Já existe usuário com esse CPF! =====")
        return

    nome = input("informe seu nome completo: ")
    data_nascimento = input("informe a sua data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    clientes.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\n===== cliente cadastrado com sucesso =====")


def criar_conta(contas, clientes):
    AGENCIA = "0001"
    numero_conta = len(contas)+1

    cpf = input("informe seu cpf apenas numero: ")
    cliente = verifica_cliente(cpf, clientes)
    conta = verifica_conta(cpf, contas)

    if cliente and conta == None:
        print("\n===== Conta criada com sucesso! =====")
        contas.append({"agencia": AGENCIA, "numero_conta": numero_conta, "cliente": cliente})
        return

    print("\n===== Cliente ja possui uma conta! =====")


def listar_clientes(contas):
    for conta in contas:
        linha = f"""
        Agência: {conta['agencia']}
        C/C: {conta['numero_conta']}
        Titular: {conta['cliente']['nome']}
        """
        print("===============================")
        print(linha)


def main():
    menu = """
    =========== Banco Dio ===========
        [nc] novo cliente
        [cc] criar conta
        [lc] listar clientes
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair
    ==> """

    saldo = 0.0
    extrato = ""
    clientes = []
    contas = []

    while True:
        opcao = input(menu)

        if opcao == "d":
            print("Deposito")
            saldo, extrato = depositar(saldo, extrato)

        elif opcao == "s":
            saldo, extrato = sacar(
                saldo=saldo,
                extrato=extrato
            )
            
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nc":
            criar_cliente(clientes)

        elif opcao == "cc":
            criar_conta(contas=contas, clientes=clientes)

        elif opcao == "lc":
            listar_clientes(contas=contas)

        elif opcao == "q":
            print("\nFinalizando...")
            break

        else:
            print("\nOperacao Invalida, por favor selecione novamente a operacao desejada.")


main()
