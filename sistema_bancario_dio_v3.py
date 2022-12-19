from datetime import datetime
import textwrap
from abc import ABC, abstractclassmethod, abstractproperty


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao, tipo):
        transacao.registrar(conta, tipo)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

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
        
        if valor <= saldo:
            if valor > 0:
                self._saldo -= valor
                print('Saque realizado com sucesso!')
                return True
                # numero_saques += 1
                # data = datetime.today().strftime('%d/%m/%Y %H:%M:%S')
                # extrato.append(f'Realizado saque de R$ {valor:.2f}, em {data}')
            else:
                print("Operação falhou! O valor informado é inválido.")
                return False
        else:
            print('Saldo insuficiente para saque.')
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Deposito realizado com sucesso!')
            return True
            # data = datetime.today().strftime('%d/%m/%Y %H:%M:%S')
            # extrato.append(f'Realizado deposito de R$ {deposito:.2f}, em {data}')
        else:
            print('Valor inválido!')
            return False
        

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques


    def sacar(self, valor, tipo):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == tipo]
        )

        if valor <= self._limite:
            if numero_saques < self._limite_saques:
                return super().sacar(valor)
            else:
                print('Limite de saque atingido! Máximo 3 saques por dia!')
                return False
        else:
            print('Valor inválido, limite de saque R$ 500.00')
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

    def adicionar_transacao(self, transacao, tipo):
        self._transacoes.append(
            {
                "tipo": tipo,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta, tipo):
        pass


class SaqueDeposito(Transacao):
    def __init__(self, valor, tipo):
        self._valor = valor
        self.tipo = tipo

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta, tipo):
        if tipo == 'saque':
            sucesso_transacao = conta.sacar(self.valor, 'saque')
            if sucesso_transacao:
                conta.historico.adicionar_transacao(self, 'saque')
        else:
            sucesso_transacao = conta.depositar(self.valor)
            if sucesso_transacao:
                conta.historico.adicionar_transacao(self, 'deposito')


def menu():
    menu = """
    Bem vindo ao seu sistema bancário!

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Saldo
    [5] Novo Cliente
    [6] Listar Clientes
    [7] Nova Conta
    [8] Listar Contas
    [9] Sair

==> """

    return input(menu)


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente não possui conta!')
        return

    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        valor = float(input("Informe o valor do depósito: "))
        transacao = SaqueDeposito(valor, 'deposito')

        conta = recuperar_conta_cliente(cliente)
        if conta:
            cliente.realizar_transacao(conta, transacao, 'deposito')
        else:
            return
    else:
        print('\n Cliente não encontrado!')
        return


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        valor = float(input("Informe o valor do saque: "))
        transacao = SaqueDeposito(valor, 'saque')

        conta = recuperar_conta_cliente(cliente)
        if conta:
            cliente.realizar_transacao(conta, transacao, 'saque')
        else:
            return
    else:
        print("\n Cliente não encontrado!")
        return


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado!")
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
            extrato += f"Realizado {transacao['tipo']} de\n\t R$ {transacao['valor']:.2f}, em {datetime.today().strftime('%d/%m/%Y %H:%M:%S')}\n"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
        clientes.append(cliente)

        print("\n Cliente criado com sucesso!")
    else:
        print("\n Já existe cliente com esse CPF!")
        return


def criar_conta(clientes, contas):
    numero_conta = len(contas) + 1
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)
        print("\n Conta criada com sucesso!")
    else:
        print("\n Cliente não encontrado, fluxo de criação de conta encerrado!")
        return


def listar_conta(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
    # if len(contas) > 0:
    #     for conta in contas:
    #         list_conta = f"""\
    #             Agência:\t{conta.get('agencia')}
    #             C/C:\t\t{conta.get('numero_conta')}
    #             Titulas:\t{conta.get('cliente').get('nome')}
    #         """
    #         print('=' * 100)
    #         print(textwrap.dedent(list_conta))
    # else:
    #     print('Nenhum cliente cadastrado!')


def listar_cliente(clientes):
    if len(clientes) > 0:
        for cli in clientes:
            list_cli = f"""\
                Nome:\t\t{cli.nome}
                CPF:\t\t{cli.cpf}
                Nascimento:\t{cli.data_nascimento}
                Endereço:\t{cli.endereco}
            """
            print('=' * 100)
            print(textwrap.dedent(list_cli))
    else:
        print('Nenhum cliente cadastrado!')


def saldo(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        conta = recuperar_conta_cliente(cliente)
        if conta:
            print(f'Seu saldo é de R$ {conta.saldo:.2f}')
        else:
            print('\n Cliente não possui conta!')
    else:
        print("\n Cliente não encontrado!")
        return

    
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == '1':
            depositar(clientes)

        elif opcao == '2':
            sacar(clientes)

        elif opcao == '3':
            exibir_extrato(clientes)

        elif opcao == '4':
            saldo(clientes)

        elif opcao == '5':
            criar_cliente(clientes)

        elif opcao == '6':
            listar_cliente(clientes)

        elif opcao == '7':
            criar_conta(clientes, contas)

        elif opcao == '8':
            listar_conta(contas)

        elif opcao == '9':
            break

        else:
            print('Opção invalida, por favor selecione novamente a operação desejada.')


main()






