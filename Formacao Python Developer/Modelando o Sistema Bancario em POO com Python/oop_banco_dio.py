from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime


# Usuario

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


# Banco
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, conta, numero):
        return cls(conta, numero)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("\nOperacao falhou! Voce nao tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\n===== Saque realizado com sucesso! =====")
            return True

        else:
            print("Operacao falhou! valor informado e invalido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n===== Depósito realizado com sucesso! =====")
            return True
        else:
            print("Operacao falhou! valor informado e invalido.")

        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        if valor > self._limite:
            print("\nOperacao falhou! Valor excedeu o limite do saque diario.")

        elif numero_saques == self._limite_saques:
            print("\nOperacao falhou! Voce excedeu o numero de saques diarios.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            }
        )


# Funcionalidade Banco classes
class Transacao(ABC):

    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao_efetuada = conta.sacar(self.valor)

        if transacao_efetuada:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao_efetuada = conta.depositar(self.valor)

        if transacao_efetuada:
            conta.historico.adicionar_transacao(self)


# Funcionalidade Banco Funcoes
def verifica_cliente(cpf, clientes):
    cliente_verificado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_verificado[0] if cliente_verificado else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente nao possui conta")
        return

    return cliente.contas[0]


def operacao(clientes, operacao):
    cpf = input("Informe o CPF: ")
    cliente = verifica_cliente(cpf, clientes)

    if not cliente:
        print("Cliente nao encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = operacao(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = verifica_cliente(cpf, clientes)

    if not cliente:
        print("===============================")
        print("\n Cliente não encontrado! ")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n=========== Extrato ===========")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Nao forma realizadas movimentacoes na conta"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\t R$ {transacao['valor']:.2f}"

    print(extrato)
    print("===============================")
    print(f"\nSaldo: R$ {conta.saldo:.2f}\n")
    print("===============================")


def criar_cliente(clientes):
    cpf = input("Informe seu CPF: ")
    cliente = verifica_cliente(cpf, clientes)

    if cliente:
        print("===============================")
        print("\nUsuario ja possui cadastrado!")
        return

    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe seu endereco (rua - numero - bairro/estado): ")

    usuario = PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco)

    clientes.append(usuario)

    print("===============================")
    print("\nCliente criado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe seu cpf: ")
    cliente = verifica_cliente(cpf, clientes)

    if not cliente:
        print("===============================")
        print("\nCliente nao possui cadastrado!")
        return

    conta = ContaCorrente(numero=numero_conta, cliente=cliente)
    contas.append(conta)
    cliente.contas.append(conta)

    print("===============================")
    print("\nConta criada com sucesso!")


def lista_clientes(contas):
    print("======== Clientes Banco =======")
    for conta in contas:
        print(str(conta))
        print("===============================")


# ATM
def main():
    clientes = []
    contas = []

    menu = """
    =========== Banco Dio ===========
        [nc] Novo Cliente
        [cc] Criar Conta
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [lc] Listar Clientes
        [q] Sair
    ==> """

    while True:
        opcao = input(menu)

        if opcao == "nc":
            criar_cliente(clientes)
        
        elif opcao == "cc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "d":
            operacao(clientes, Deposito)

        elif opcao == "s":
            operacao(clientes, Saque)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "lc":
            lista_clientes(contas)

        elif opcao == "q":
            print("\nFinalizando...")
            break

        else:
            print("\nOperacao Invalida, por favor selecione novamente a operacao desejada.")


main()
