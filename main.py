QTD_LIMITE_SAQUE_DIARIO = 3
saldo_conta = 0
qtd_saques_realizados = 0
limite_por_saque = 500
movimentacoes_conta = []

#função para atualização de saldo. Em caso de saque, deve receber um valor negativo
def atualiza_saldo(valor):
    global saldo_conta
    saldo_conta += valor
    
def atualiza_movimentacoes_conta(operacao, valor):
     
    global movimentacoes_conta   
    if operacao.lower() == 'deposito':
        movimentacoes_conta.append({'operacao': 'Depósito', 'valor': valor})
    elif operacao.lower() == 'saque':
        movimentacoes_conta.append({"operacao" : "Saque", "valor" : valor * -1})
    else:
        return print('Parâmetro passado no valor operação inválido.')
    
def sacar(valor):
    #limite de 3 saques por dia
    #limite máximo por saque deve ser de 500 reais
    #exibir mensagem informando impossibilidade de saque caso saldo seja inferior ao valor de saque
    #todos os saques precisam ser armazenados numa variável para exibir no extrato
    global qtd_saques_realizados
    global movimentacoes_conta
    
    if valor <= 0:
        return print("Valor precisa ser um número positivo")
    elif qtd_saques_realizados >= QTD_LIMITE_SAQUE_DIARIO:
        return print("Quantidade diária de saques excedida. \n Tente novamente outro dia.")
    elif valor > limite_por_saque:
        return print(f"Valor excede o limite por operação. O limite é de R$ {limite_por_saque:.2f}")
    elif valor > saldo_conta:
        return print("O valor do saque não pode excer o saldo em conta!") 
    else:
        qtd_saques_realizados += 1
        atualiza_saldo(valor * -1)
        atualiza_movimentacoes_conta('Saque', valor)
        return print("Saque realizado com sucesso! Retire as cédulas no caixa!")
    
def depositar(valor):
    #valores depositados precisam ser positivos
    #todos os depósitos precisam ser armazenados numa variável para exibir no extrato
    global saldo_conta
    global movimentacoes_conta
    if valor <= 0:
        return print('O valor para depósito não pode ser negativo!')
    else:
        atualiza_saldo(valor)
        atualiza_movimentacoes_conta('Deposito', valor)
    
def exibir_extrato():
    #listar todos os depósitos e saques realizados na conta
    #informar caso não haja movimentação
    #Exibir o saldo ao final, no formato: R$ 0,00
    
    print('Extrato'.center(40, '_')) #para desenhar a parte superior do quadro
    
    if len(movimentacoes_conta) == 0:
        print('Não há movimentações no período!'.center(40,'*'))
    else:
        #for para percorrer cada transação salva e imprimi-la na tela
        for transacao in range(len(movimentacoes_conta)):
            print(f"{movimentacoes_conta[transacao]['operacao']}: R$ {movimentacoes_conta[transacao]['valor']:.2f} |".rjust(41))
        
    print('_' * 40) #linha de baixo do quadro
    print(f'Saldo atual: R$ {saldo_conta:.2f}'.rjust(40))

def limpar_terminal():
    import os
    
    try:
        os.system("cls")
    except AttributeError:
        print('\n' * os.get_terminal_size().lines)
        
menu_principal = """
 ________________________ PyBank ________________________
|                                                        |
| Bem-vindo ao menu inicial da sua conta.                |
| Pressione o número correspondente à operação           |
| desejada e tecle ENTER:                                |
|                                                        |
| (1) Saque                                              |  
| (2) Depósito                                           |
| (3) Extrato                                            |
| (0) Sair da Conta                                      |
|________________________________________________________|
"""

while True:
    operacao = int(input(menu_principal))
    
    if operacao == 1:
        limpar_terminal()
        valor_saque = int(input("Informe o valor do saque \nR$: "))
        sacar(valor_saque)
        input("Tecle ENTER para retornar ao menu principal")
        limpar_terminal()
    elif operacao == 2:
        limpar_terminal()
        valor_deposito = int(input("Informe o valor do depósito \nR$: "))
        depositar(valor_deposito)
        input("Tecle ENTER para retornar ao menu principal")
        limpar_terminal()
    elif operacao == 3:
        limpar_terminal()
        exibir_extrato()
        input("Tecle ENTER para retornar ao menu principal")
        limpar_terminal()
    elif operacao == 0:
        break
    else:
        print("Selecione uma opção válida!")
        input("Tecle ENTER para retornar ao menu principal")
        limpar_terminal()