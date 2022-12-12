from datetime import datetime
import textwrap


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
    
def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == '1':
            deposito = float(input('Digite o valor para deposito: '))

            saldo, extrato = depositar(saldo, deposito, extrato)

        elif opcao == '2':
            valor = float(input('Informe o valor que deseja sacar: '))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite_saques=LIMITE_SAQUES,
                numero_saques=numero_saques,
                limite=limite
            )

        elif opcao == '3':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == '4':
            saldo(saldo)

        elif opcao == '5':
            novo_cliente(clientes)

        elif opcao == '6':
            listar_cliente(clientes)

        elif opcao == '7':
            numero_conta = len(contas) + 1
            conta = nova_conta(AGENCIA, numero_conta, clientes)

            if conta:
                contas.append(conta)

        elif opcao == '8':
            listar_conta(contas)

        elif opcao == '9':
            break

        else:
            print('Opção invalida, por favor selecione novamente a operação desejada.')


def depositar(saldo, deposito, extrato, /):
    if deposito >= 0:
        saldo += deposito
        data = datetime.today().strftime('%d/%m/%Y %H:%M:%S')
        extrato.append(f'Realizado deposito de R$ {deposito:.2f}, em {data}')
        print('Deposito realizado com sucesso!')
    else:
        print('Valor inválido!')

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    if len(extrato) > 0:
        for ext in extrato:
            print(ext)
        print(f'Seu saldo é de R$ {saldo:.2f}')
    else:
        print('Não foram realizadas movimentações.')


def saldo(saldo, /):
    return f'Seu saldo é de R$ {saldo:.2f}'


def sacar(*, saldo, valor, extrato, limite_saques, numero_saques, limite):
    if valor <= limite:
        if numero_saques < limite_saques:
            if valor <= saldo:
                saldo -= valor
                numero_saques += 1
                data = datetime.today().strftime('%d/%m/%Y %H:%M:%S')
                extrato.append(f'Realizado saque de R$ {valor:.2f}, em {data}')
                print('Saque realizado com sucesso!')
            else:
                print('Saldo insuficiente para saque.')
        else:
            print('Limite de saque atingido! Máximo 3 saques por dia!')
    else:
        print('Valor inválido, limite de saque R$ 500.00')

    return saldo, extrato


def filtrar_cliente(cpf, clientes):
    clientes_filtrado = [cliente for cliente in clientes if cliente['cpf'] == cpf]
    return clientes_filtrado[0] if clientes_filtrado else None

def novo_cliente(clientes):
    while True:
        cpf = input('Informe o CPF, apenas números: ')

        if cpf.isnumeric():
            if len(cpf) == 11:
                break
            else:
                print('Informe um número válido!')
        else:
            print('Informe um número válido!')

    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('Cliente já cadastrado com o CPF informado!')
        return

    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento no formato "dia/mês/ano": ')
    endereco = input('Informe o endereço completo, ex: lagradouro, numero - bairro - cidade/sigla estado: ')

    clientes.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})

    print('Cliente cadastrado com sucesso!')


def listar_cliente(clientes):
    if len(clientes) > 0:
        for cli in clientes:
            list_cli = f"""\
                Nome:\t\t{cli.get('nome')}
                CPF:\t\t{cli.get('cpf')}
                Nascimento:\t{cli.get('data_nascimento')}
                Endereço:\t{cli.get('endereco')}
            """
            print('=' * 100)
            print(textwrap.dedent(list_cli))
    else:
        print('Nenhum cliente cadastrado!')


def nova_conta(agencia, numero_conta, clientes):
    while True:
        cpf = input('Informe o CPF, apenas números: ')

        if cpf.isnumeric():
            if len(cpf) == 11:
                break
            else:
                print('Informe um número válido!')
        else:
            print('Informe um número válido!')

    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('Conta criada com sucesso!')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'cliente': cliente}
    else:
        print('Cliente não encontrado!')


def listar_conta(contas):
    if len(contas) > 0:
        for conta in contas:
            list_conta = f"""\
                Agência:\t{conta.get('agencia')}
                C/C:\t\t{conta.get('numero_conta')}
                Titulas:\t{conta.get('cliente').get('nome')}
            """
            print('=' * 100)
            print(textwrap.dedent(list_conta))
    else:
        print('Nenhum cliente cadastrado!')


main()






