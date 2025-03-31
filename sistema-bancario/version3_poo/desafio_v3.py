from __future__ import annotations # Para solucionar o problema das "Forward References" dentro das classes
from abc import ABC, abstractmethod
from datetime import datetime
import textwrap
import time

class Cliente:
    def __init__(self, endereco:str):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta:Conta, transacao:Transacao) -> None:
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta:Conta) -> None:
        self.contas.append(conta)
    
class PessoaFisica(Cliente):
    def __init__(self, cpf:str, nome:str, data_nascimento:str, endereco:str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
        
    def __init__(self, cliente:Cliente, conta:int, agencia:str = '0001'):  
        self._cliente = cliente
        self._agencia = agencia
        self._conta = conta        
        self._historico = Historico()
    
    @property
    def conta(self) -> int:
        return self._conta
    
    @property
    def agencia(self) -> str:
        return self._agencia
    
    @property
    def cliente(self) -> Cliente:
        return self._cliente
    
    @property
    def historico(self) -> Historico:
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente:Cliente, conta:int, agencia:str = '0001') -> Conta:
        return cls(cliente, conta)
          
    def sacar(self, valor:float) -> bool:
        saldo = self.saldo()
        if valor > 0 and valor <= saldo:
            # self._saldo -= valor
            print('Operação realizada com sucesso!')
            return True
        elif valor <= 0:
            print('Operação não realizada. O valor deve ser positivo!')
        elif valor > saldo:
            print('Operação não realizada. Saldo Insuficiente!')
        
        return False      
    
    def depositar(self, valor: float) -> bool:
        
        if valor <= 0:
            print('Operação não realizada! O valor deve ser positivo')
        else:
            # self._saldo += valor
            print('Depósito realizado com sucesso!')
            return True
        
        return False
    
    def saldo(self) -> float:
        saldo = 0.0
        for transacao in self._historico.transacoes:
            
            if transacao.get('tipo') == 'Deposito':
                saldo += transacao.get('valor')
                
            elif transacao.get('tipo') == 'Saque':
                saldo -= transacao.get('valor')
        
        return saldo
    
    def __str__(self):
        return f'Cliente: {self._cliente.nome}, Agência: {self._agencia}, Conta: {self._conta}'
    
class ContaCorrente(Conta):

    def __init__(self, cliente:Cliente, conta:int, limite_saque:float = 500, limite_qtd_saques:int = 3):
        super().__init__(cliente, conta)
        self.limite_saque = limite_saque
        self.limite_qtd_saques = limite_qtd_saques
        
    def sacar(self, valor:float) -> bool:  
        saldo = super().saldo()
        qtd_saques = len([
            transacao for transacao in self.historico.transacoes if transacao.get('tipo') == Saque.__name__
        ])      
        if valor > self.limite_saque:
            print(f'Valor excede seu limite de saque para esta conta. (Limite: R$ {self.limite_saque})')
        elif qtd_saques >=  self.limite_qtd_saques:
            print('Você excedeu o limite diário de saques')
        elif valor <= 0:
            print('Operação não realizada. O valor deve ser positivo!')
        elif valor > self.saldo():
            print('Operação não realizada. Saldo Insuficiente!')
        else:
            super().sacar(valor)
            return True
        
        
        return False      
    
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao:Transacao):
                
        self._transacoes.append({
            'tipo' : str(transacao.__class__.__name__) ,
            'valor': transacao.valor,
            'data': datetime.now()
        })

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta:Conta):
        pass
        
class Deposito(Transacao):
    def __init__(self, valor:float):
        self.valor = valor
        
    def registrar(self, conta:Conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor
    
    def registrar(self, conta:Conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
 
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

def limpar_terminal() -> None: # Limpa o terminal
    import os
    
    try:
        os.system("cls")
    except AttributeError:
        print('\n' * os.get_terminal_size().lines)

def cliente_existe(cpf:str, lista_clientes:list) -> Cliente: # Checa se cliente já existe
    """
    Verifica se um cliente já existe na lista de clientes.

    Parâmetros:
    cpf (str): O CPF do cliente a ser verificado.
    lista_clientes (list): A lista de clientes cadastrados.

    Retorna:
    bool: True se o cliente já existe, False caso contrário.
    """
    
    for cliente in lista_clientes:
        if cliente.cpf == cpf:
            return cliente

def selecionar_conta_usuario(cliente:Cliente, numero_conta_informado:int) -> Conta: #retornar o conta, caso ela pertença ao cliente.
    for conta in cliente.contas:
        if conta._conta == numero_conta_informado:
            return conta
    
    return False
       
def exibir_extrato(conta:Conta) -> None: #Exibe o extrato da conta informada pelo cliente.
    transacoes = conta.historico.transacoes  
      
    print('Extrato'.center(40, '_')) #para desenhar a parte superior do quadro
    
    if not transacoes:
        print('Não há movimentações no período!'.center(40,'*'))
    else:
        print(f'Exibindo extrato para conta {conta.conta}'.center(40,'*'))
        #for para percorrer cada transação salva e imprimi-la na tela
        for transacao in transacoes:
            data_formatada = datetime.strftime(transacao['data'], '%d/%m/%Y')
            print(f"{data_formatada} - {transacao['tipo']}: R$ {transacao['valor']:.2f} |".rjust(41))
        
    print('_' * 40) #linha de baixo do quadro
    print(f'Saldo atual: R$ {conta.saldo():.2f}'.rjust(40))
       

def main():
    lista_clientes = [] # Armazena todos os clientes cadastrados
    lista_contas = [] # Armazena todas as contas criadas
    usuario_logado = 0 # Armazena usuário logado no sistema
      
    while True:    
        limpar_terminal()    
        if usuario_logado == 0: # entra no menu inicial para login ou cadastro de novo usuário
            opcao_menu = int(input(textwrap.dedent(menu_inicial())))
            
            if opcao_menu == 1: #Para fazer login quando já é cliente
                limpar_terminal()
                cpf_informado = input('Informe o número de seu CPF: ')
                
                cliente_informado = cliente_existe(cpf_informado, lista_clientes)
                
                if cliente_informado:
                    usuario_logado = cliente_informado
                    continue #reiniciar uso do while
                else:
                    print('Usuário não encontrado! Realize seu cadastro.')
                    input("Tecle ENTER para retornar ao menu inicial")
                    continue       
                         
            elif opcao_menu == 2: # Para cadastrar um novo usuário
                limpar_terminal()
                print('Por favor, informe o que for pedido abaixo:')
                cpf_novo_usuario = input('CPF (apenas números): ')
                nome_novo_usuário = input('Informe seu nome: ')
                data_nascimento_novo_usuario = input('Data de nascimento: ')
                endereco_novo_usuario = input('Endereço: ')
                
                if cliente_existe(cpf_novo_usuario, lista_clientes):
                    input('Já existe um cadastro para o CPF informado. Reinicie o cadastro. Pressione ENTER para retornar ao menu incial.')
                else:  
                    novo_cliente = PessoaFisica(cpf_novo_usuario, nome_novo_usuário, data_nascimento_novo_usuario, endereco_novo_usuario)                                 
                    lista_clientes.append(novo_cliente)
                
                continue 
            
            elif opcao_menu == 3: #listar todas as contas, só pra conferir que tá funcionando ok
                limpar_terminal()
                for conta in lista_contas:
                    print(conta)
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
                
                conta_informada = selecionar_conta_usuario(usuario_logado, conta_saque) # retorna a conta do usuário, se existir.
                if conta_informada: # True caso pertença a ele. Senão, None
                    usuario_logado.realizar_transacao(conta_informada, Saque(valor_saque))
                else: 
                    print('Número de conta inválido ou não é de sua titularidade.')
                
                input("Tecle ENTER para retornar ao menu principal")
                
            elif operacao == 2: # Para realizar um depósito
                limpar_terminal()
                valor_deposito = float(input("Informe o valor do depósito \nR$: "))
                conta_deposito = int(input('Informe o número da conta: '))
                conta_informada = selecionar_conta_usuario(usuario_logado, conta_deposito) # retorna a conta do usuário, se existir.
                
                if conta_informada: # True caso pertença a ele. Senão, None
                    usuario_logado.realizar_transacao(conta_informada, Deposito(valor_deposito))
                else: 
                    print('Número de conta inválido ou não é de sua titularidade.')
                
                input("Tecle ENTER para retornar ao menu principal")
                    
            elif operacao == 3: # Para tirar extrato
                limpar_terminal()
                conta_extrato = int(input('Informe a conta para exibir o extrato: '))
                limpar_terminal()
                conta_informada = selecionar_conta_usuario(usuario_logado, conta_extrato) # retorna a conta do usuário, se existir.
                if conta_informada: # True caso pertença a ele. Senão, None
                    exibir_extrato(conta_informada)
                else: 
                    print('Número de conta inválido ou não é de sua titularidade.')
                
                input("Tecle ENTER para retornar ao menu principal")
                
            elif operacao == 4: # Cadastrar nova conta
                while True:
                    limpar_terminal()
                    deseja_criar_conta = input('Uma nova conta será criada para você. Deseja confirmar a operação (s/n): ')
                    if deseja_criar_conta.lower() == "s":
                        numero_conta = len(lista_contas) + 1
                        nova_conta = ContaCorrente(usuario_logado, numero_conta)
                        usuario_logado.adicionar_conta(nova_conta)
                        lista_contas.append(nova_conta)
                        input(f'Conta criada com sucesso! Anote a numeração:\n Ag: {nova_conta.agencia} \nConta: {nova_conta.conta}\nPressione qualquer tecla para sair')
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
                contas_usuario = usuario_logado.contas
                for conta in contas_usuario:
                    print(f'Agência: {conta.agencia} \t Conta: {conta.conta} Saldo: R$ {conta.saldo()}\n')
                input("Tecle ENTER para retornar ao menu principal")
            
            elif operacao == 0: # Para sair da conta
                usuario_logado = 0
                continue
            else:
                print("Selecione uma opção válida!")
                input("Tecle ENTER para retornar ao menu principal")
                limpar_terminal()
    

main()
