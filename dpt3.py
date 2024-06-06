from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    def realizar_transicao (self,conta,transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Pessoa_Fisica(Cliente):
    def __init__(self,nome,data_nasc,cpf,endereco):
        super(). __init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nasc = data_nasc


class Contas:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    @classmethod
    def nova_conta(cls,cliente,numero):
        return  cls( numero, cliente)

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
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("A operação falhou!...Sem saldo")

        elif valor > 0:
            self._saldo -= valor
            print("Saque Realizado!...")
            return True
        else:
            print(" Operação falhou! O valor informado é inválido.")

        return False


    def depositar(self,valor):
       if valor > 0:
           self._saldo += valor
           print("Deposito Realizado!...")
       else:
           print("Operação falhou... Deposito não realizado")
           return False

       return True


class Contas_Correntes(Contas):
    def __init__(self,numero,cliente,limite = 500, num_saque = 3):
        super().__init__(numero,cliente)
        self.limite = limite
        self.num_saque = num_saque


    def sacar(self,valor):
        numero_saque = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saque > self.num_saque

        if excedeu_limite:
            print("A operação falhou!... o valor de saque chegou ao limite")

        elif excedeu_saques:
            print("A operação falhou!... o valor de saque chegou ao seu máximo")

        else:
           return super().sacar(valor)
        return False
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacoes(self,transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
        })



class Transacao(ABC):
    @property
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(cls, conta):
        pass


class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.historico.adicionar_transacao(self)



def menu():
    menu = """\n
    ~~~~~~~~~~ MENU ~~~~~~~~~~
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuario(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuario(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuario(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_usuario(cpf, clientes)

    if cliente:
        print("Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço : ")

    cliente = Pessoa_Fisica(nome=nome, data_nascimentoata=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print(" Cliente criado com sucesso! ")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuario(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado, fluxo de criação de conta encerrado!")
        return

    conta = Contas_Correntes.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()

