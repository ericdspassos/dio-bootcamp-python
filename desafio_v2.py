from datetime import datetime
import textwrap
import time

AGENCIA = '0001'
QTD_LIMITE_SAQUE_DIARIO = 3
QTD_LIMITE_TRANSACOES_DIARIAS = 10
    
def atualiza_transacoes(cpf, conta, operacao, valor, transacoes_usuarios) -> list: #atualiza a lista de transações e devolve ela
      
    data_hora_atual = datetime.now()
    if operacao.lower() == 'deposito':
        transacoes_usuarios.append({'cpf': cpf, 'conta': conta, 'operacao': 'Depósito', 'valor': valor, 'data': data_hora_atual})
    elif operacao.lower() == 'saque':
        transacoes_usuarios.append({'cpf': cpf, 'conta': conta, "operacao" : "Saque", "valor" : valor * -1, 'data': data_hora_atual})
    else:
        print('ERROR: Parâmetro passado no valor "operação" inválido.')
    
    return transacoes_usuarios
   
def get_qtd_transacoes_dia(cpf, transacoes_usuarios) -> int:
    qtd_transacoes = 0
    data_atual = datetime.now()
    
    for transacao in transacoes_usuarios:
        if datetime.strftime(transacao['data'],'%d-%m-%Y') == datetime.strftime(data_atual, '%d-%m-%Y') and cpf == transacao.get('cpf') :
           qtd_transacoes += 1
           
    return qtd_transacoes 

def get_saldo(cpf, conta, transacoes_usuarios) -> float: # Retorna o saldo do usuário na conta indicada
    saldo = 0
    
    for usuario in transacoes_usuarios:
        if cpf == usuario.get('cpf') and conta == usuario.get('conta'):
            saldo += usuario.get('valor')
    
    return saldo
    
def get_qtd_saques(cpf, transacoes_usuarios) -> int: #retorna a quantidade de saques realizados pelo usuário
    qtd_saque = 0
    for usuario in transacoes_usuarios:
        if cpf == usuario.get('cpf') and usuario.get('operacao').lower == "saque":
            qtd_saque += 1
    
    return qtd_saque
  
def get_contas_usuario(cpf, lista_contas) -> list: # Retorna uma lista com todas as contas do usuário
    contas_usuario = []
    for conta in lista_contas:
        if cpf == conta[2]:
            contas_usuario.append(conta)
    
    return contas_usuario
                  
def sacar(*, valor, conta, valor_limite, cpf, transacoes_usuarios, lista_contas) -> list: #realiza o saque na conta indicada
    #limite de 3 saques por dia
    #limite máximo por saque deve ser de 500 reais
    #exibir mensagem informando impossibilidade de saque caso saldo seja inferior ao valor de saque
    #todos os saques precisam ser armazenados numa variável para exibir no extrato
    qtd_saques_realizados = get_qtd_saques(cpf, transacoes_usuarios)
    qtd_transacoes_dia = get_qtd_transacoes_dia(cpf, transacoes_usuarios)
    saldo_conta = get_saldo(cpf, conta, transacoes_usuarios)
    contas_usuario = get_contas_usuario(cpf, lista_contas)
    is_conta_usuario = False #recebe o valor False e logo abaixo testa se a conta é do usuário
    for conta_usr in contas_usuario:
        if conta_usr[1] == conta:
            is_conta_usuario = True
            break
        
    if valor <= 0:
        print("Valor precisa ser um número positivo")
    elif not is_conta_usuario:
        print('O número de conta não corresponde a nenhuma conta cadastrada para o usuário')
    elif qtd_saques_realizados >= QTD_LIMITE_SAQUE_DIARIO:
        print("Quantidade diária de saques excedida. \n Tente novamente outro dia.")
    elif qtd_transacoes_dia >= QTD_LIMITE_TRANSACOES_DIARIAS:
        print("Você excedeu o limite de transações diário.\n Tente novamente outro dia.")
    elif valor > valor_limite:
        print(f"Valor excede o limite por operação. O limite é de R$ {valor_limite:.2f}")
    elif valor > saldo_conta:
        print("O valor do saque não pode exceder o saldo em conta!") 
    else:
        transacoes_usuarios = atualiza_transacoes(cpf, conta, 'Saque', valor, transacoes_usuarios)
        print("Saque realizado com sucesso! Retire as cédulas no caixa!")
    return transacoes_usuarios
    
def depositar(cpf, conta, valor, transacoes_usuarios, lista_contas, /) -> list: # Realiza a operação de depósito
    #valores depositados precisam ser positivos
    #todos os depósitos precisam ser armazenados numa variável para exibir no extrato
    qtd_transacoes_dia = get_qtd_transacoes_dia(cpf, transacoes_usuarios)
    contas_usuario = get_contas_usuario(cpf, lista_contas)
    is_conta_usuario = False #recebe o valor False e logo abaixo testa se a conta é do usuário
    for conta_usr in contas_usuario:
        if conta_usr[1] == conta:
            is_conta_usuario = True
            break
        
    if valor <= 0:
        print('O valor para depósito não pode ser negativo!')
    elif not is_conta_usuario:
        print('O número de conta não corresponde a nenhuma conta cadastrada para o usuário!')
    elif qtd_transacoes_dia >= QTD_LIMITE_TRANSACOES_DIARIAS:
        print("Você excedeu o limite diário de transações.\n Tente novamente outro dia.")
    else:        
        transacoes_usuarios = atualiza_transacoes(cpf, conta, 'Deposito', valor, transacoes_usuarios)
        print('Depósito realizado com sucesso! \n')
    
    return transacoes_usuarios
    
def exibir_extrato(cpf, conta,/, *,transacoes_usuarios, lista_contas) -> None: #Exibe o extrato da conta informada pelo cliente.
    #listar todos os depósitos e saques realizados na conta
    #informar caso não haja movimentação
    #Exibir o saldo ao final, no formato: R$ 0,00
    saldo = get_saldo(cpf, conta, transacoes_usuarios)
    contas_usuario = get_contas_usuario(cpf, lista_contas)
    is_conta_usuario = False #recebe o valor False e logo abaixo testa se a conta é do usuário
    for conta_usr in contas_usuario:
        if conta_usr[1] == conta:
            is_conta_usuario = True
            break
        
    print('Extrato'.center(40, '_')) #para desenhar a parte superior do quadro
    
    if not transacoes_usuarios:
        print('Não há movimentações no período!'.center(40,'*'))
    elif not is_conta_usuario:
        print('A conta informada não é válida ou não pertence a você.')
    else:
        print(f'Exibindo extrato para conta {conta}'.center(40,'*'))
        #for para percorrer cada transação salva e imprimi-la na tela
        for transacao in transacoes_usuarios:
            if conta == transacao['conta']:
                data_formatada = datetime.strftime(transacao['data'], '%d/%m/%Y')
                print(f"{data_formatada} - {transacao['operacao']}: R$ {transacao['valor']:.2f} |".rjust(41))
        
    print('_' * 40) #linha de baixo do quadro
    print(f'Saldo atual: R$ {saldo:.2f}'.rjust(40))

def limpar_terminal(): # Limpa o terminal
    import os
    
    try:
        os.system("cls")
    except AttributeError:
        print('\n' * os.get_terminal_size().lines)
        
def menu_principal() -> str: # Menu quando o usuário já fez o login
    menu = """
     ________________________ PyBank ________________________
    |                                                        |
    | Bem-vindo ao menu inicial da sua conta.                |
    | Pressione o número correspondente à operação           |
    | desejada e tecle ENTER:                                |
    |                                                        |
    | (1) Saque                                              |  
    | (2) Depósito                                           |
    | (3) Extrato                                            |
    | (4) Cadastrar Nova Conta                               |
    | (5) Listar Minhas Contas (Com Saldo)                   | 
    | (0) Sair da Conta                                      |
    |________________________________________________________|
    """
    return menu

def menu_inicial() -> str: # Menu no início da aplicação, antes de ser realizado login
    menu = """
     ________________________ PyBank ________________________
    |                                                        |
    | Bem-vindo ao PyBank. Prático e seguro.                 |
    | Pressione o número correspondente à operação           |
    | desejada e tecle ENTER:                                |
    |                                                        |
    | (1) Já sou Cliente!                                    |  
    | (2) Desejo me cadastrar!                               |
    | (3) Listar todas as contas                             |
    | (0) Encerrar aplicativo.                               |
    |________________________________________________________|
    """
    return menu
    # return int(input(textwrap.dedent(menu)))

def cliente_existe(cpf, lista_clientes) -> bool: # Checa se cliente já existe
    """
    Verifica se um cliente já existe na lista de clientes.

    Parâmetros:
    cpf (str): O CPF do cliente a ser verificado.
    lista_clientes (list): A lista de clientes cadastrados.

    Retorna:
    bool: True se o cliente já existe, False caso contrário.
    """
    
    for cliente in lista_clientes:
        if cliente.get('cpf') == cpf:
            return True
    
    return False

def cadastrar_cliente(cliente: dict, lista_clientes) -> list: #Cadastra um novo cliente e retorna a lista atualizada
    nome = cliente.get("nome")
    data_nascimento = cliente.get("data_nascimento")
    cpf = cliente.get('cpf')
    endereco = cliente.get('endereco')
    
    if cliente_existe(cpf, lista_clientes):
        print('Já existe um cadastro para o CPF informado!')
        time.sleep(2)
    else:
        lista_clientes.append(cliente)
    
    return lista_clientes

def criar_conta(cpf_cliente, lista_clientes, lista_contas, agencia = "0001") -> list: # Cria uma nova conta
    #Agência sempre 0001; Contas sequenciais, incrementadas de 1 em 1
    ultima_conta = lista_contas[-1][1] if len(lista_contas) > 0 else 0
    conta_nova = [agencia, ultima_conta + 1, cpf_cliente]
    lista_contas.append(conta_nova)
    
    return lista_contas

def main():
    saldo = 0
    limite_por_saque = 500
    transacoes_usuarios = [] #armazena todas as transações de todos os usuários (saque e depósito)
    lista_clientes = [] #lista com todos os cliente cadastrados
    lista_contas = [] #[agencia, conta, cpf] lista de todas as contas cadastradas para todos os cliente
    usuario_logado = 0 # armazena o cliente logado na conta.
    
    
    while True:    
        limpar_terminal()     
        if usuario_logado == 0: #entra no menu inicial para login ou cadastro de novo usuário
            opcao_menu = int(input(textwrap.dedent(menu_inicial())))
            
            if opcao_menu == 1: #Para fazer login quando já é cliente
                limpar_terminal()
                cpf_informado = input('Informe o número de seu CPF: ')
                if cliente_existe(cpf_informado, lista_clientes):
                    usuario_logado = cpf_informado
                    continue #reiniciar uso do while
                else:
                    print('Usuário não encontrado! Realize seu cadastro.')
                    input("Tecle ENTER para retornar ao menu inicial")
                    continue                
            elif opcao_menu == 2: # Para cadastrar um novo usuário
                limpar_terminal()
                nome_novo_usuário = input('Informe seu nome: ')
                data_nascimento_novo_usuario = input('Data de nascimento: ')
                cpf_novo_usuario = input('CPF (apenas números): ')
                endereco_novo_usuario = input('Endereço: ')
                
                dict_novo_usuario = {
                    'nome': nome_novo_usuário, 
                    'data_nascimento': data_nascimento_novo_usuario,
                    'cpf': cpf_novo_usuario,
                    'endereco': endereco_novo_usuario
                    }
                
                lista_clientes = cadastrar_cliente(dict_novo_usuario, lista_clientes)
                continue 
            elif opcao_menu == 3: #listar todas as contas, só pra conferir que tá funcionando ok
                limpar_terminal()
                for conta in lista_contas:
                    cpf_todos = conta[2]
                    print(f'Cliente: {conta[2]} Agência: {conta[0]} \t Conta: {conta[1]} Saldo: R$ {get_saldo(cpf_todos, conta[1], transacoes_usuarios)}\n')
                input("Tecle ENTER para retornar ao menu principal")    
            elif opcao_menu == 0: #Para encerrar o sistema
                break   
            else:
                print("Selecione uma opção válida!")
                time.sleep(2)
                #fim do bloco que contém o menu incial para login ou cadastro de usuário      
        else: #Entra no menu da conta do usuário
            
            operacao = int(input(textwrap.dedent(menu_principal())))
            
            if operacao == 1: # Para realizar um saque
                limpar_terminal()
                valor_saque = float(input("Informe o valor do saque \nR$: "))
                conta_saque = int(input('Informe o número da conta: '))
                transacoes_usuarios = sacar(cpf=usuario_logado, valor=valor_saque, valor_limite=limite_por_saque,
                                            conta=conta_saque, transacoes_usuarios=transacoes_usuarios, lista_contas=lista_contas)
                input("Tecle ENTER para retornar ao menu principal")
            elif operacao == 2: # Para realizar um depósito
                limpar_terminal()
                valor_deposito = float(input("Informe o valor do depósito \nR$: "))
                conta_deposito = int(input('Informe o número da conta: '))
                transacoes_usuarios = depositar(usuario_logado, conta_deposito, valor_deposito, transacoes_usuarios, lista_contas)
                input("Tecle ENTER para retornar ao menu principal")
            elif operacao == 3: # Para tirar extrato
                limpar_terminal()
                conta_extrato = int(input('Informe a conta para exibir o extrato: '))
                limpar_terminal()
                exibir_extrato(usuario_logado, conta_extrato, transacoes_usuarios=transacoes_usuarios,
                               lista_contas=lista_contas)
                input("Tecle ENTER para retornar ao menu principal")
            elif operacao == 4: # Cadastrar nova conta
                while True:
                    limpar_terminal()
                    deseja_criar_conta = input('Uma nova conta será criada para você. Deseja confirmar a operação (s/n): ')
                    if deseja_criar_conta.lower() == "s":
                        criar_conta(cpf_cliente=usuario_logado, lista_clientes=lista_clientes, lista_contas=lista_contas)
                        input(f'Conta criada com sucesso! Anote a numeração:\n Ag: 0001 \n Conta: {lista_contas[-1][1]}\nPressione qualquer tecla para sair')
                        break
                    elif deseja_criar_conta == "n":
                        print('Ficaremos felizes em abrir uma nova conta quando estiver interessado.')
                        input("Tecle ENTER para retornar ao menu principal")
                        break
                    else:
                        print("Selecione uma opção válida!")
                        time.sleep(2)
            elif operacao == 5: # Listar contas existentes:
                limpar_terminal()
                print('Estas são suas contas:\n')
                contas_usuario = get_contas_usuario(usuario_logado, lista_contas)
                for conta in contas_usuario:
                    print(f'Agência: {conta[0]} \t Conta: {conta[1]} Saldo: R$ {get_saldo(usuario_logado, conta[1], transacoes_usuarios)}\n')
                input("Tecle ENTER para retornar ao menu principal")
            elif operacao == 0: # Para sair da conta
                usuario_logado = 0
                continue
            else:
                print("Selecione uma opção válida!")
                input("Tecle ENTER para retornar ao menu principal")
                limpar_terminal()
            
main() # Chamada da função principal para executar a aplicação.