from datetime import datetime
saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

menu = """
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Saldo
    [5] Sair

==> """
while True:
    opcao = input(menu)

    if opcao == '1':
        deposito = int(input('Digite o valor para deposito: '))
        if deposito >= 0:
            saldo += deposito
            data = datetime.today().strftime('%d/%m/%Y %H:%M:%S')
            extrato.append(f'Realizado deposito de R$ {deposito:.2f}, em {data}')
            print('Deposito realizado com sucesso!')
        else:
            print('Valor inválido!')

    elif opcao == '2':
        sac = int(input('Informe o valor que deseja sacar: '))
        if sac <= 500:
            if numero_saques < LIMITE_SAQUES:
                if sac <= saldo:
                    saldo -= sac
                    numero_saques += 1
                    data = datetime.today().strftime('%d/%m/%Y %H:%M:%S')
                    extrato.append(f'Realizado saque de R$ {sac:.2f}, em {data}')
                    print('Saque realizado com sucesso!')
                else:
                    print('Saldo insuficiente para saque.')
            else:
                print('Limite de saque atingido! Máximo 3 saques por dia!')
        else:
            print('Valor inválido, limite de saque R$ 500.00')

    elif opcao == '3':
        if len(extrato) > 0:
            for ext in extrato:
                print(ext)
            print(f'Seu saldo é de R$ {saldo:.2f}')
        else:
            print('Não foram realizadas movimentações.')

    elif opcao == '4':
        print(f'Seu saldo é de R$ {saldo:.2f}')

    elif opcao == '5':
        break

    else:
        print('Opção invalida, por favor selecione novamente a operação desejada.')


