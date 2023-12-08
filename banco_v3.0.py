import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"


class Conta:
    def __init__(self, numero, cliente, senha):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._senha = senha
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
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

    
    def verifica_senha(self, senha_digitada):
        senha = self._senha
        if senha_digitada == senha:
            return True
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, senha, limite=500, limite_saques=3):
        super().__init__(numero, cliente, senha)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    @property
    def historico(self):
        return self._historico

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
                "data": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            }
        )
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def criar_usuario(nome, data_nascimento, endereço, cpf, senha):

    usuario = PessoaFisica(nome=nome,data_nascimento= data_nascimento,cpf=cpf,endereco=endereço)
    existe = False
    for i, usuario in enumerate(usuarios):
        usuario.cpf
        if usuarios[i].cpf == cpf:
            existe == True
            break
    if existe == False:
        usuarios.append(usuario)
        criar_conta_corrente(usuario, senha)
    else:
        print(f"Usuário com cpf: {cpf} já existe!")


def criar_conta_corrente(usuario, senha):
    num = len(contas) + 1
    nova_conta = ContaCorrente(cliente=usuario,numero=num, senha=senha)
    contas.append(nova_conta)
    usuario.contas.append(nova_conta)
    usuarios.append(usuario)

    print(f'''
          Conta Criada com Sucesso:
          Agencia: {nova_conta._agencia}
          conta: {num}
          CPF: {usuario.cpf}5
    ''')
    return nova_conta

def senha_esquecida(num_conta):
    conta = get_conta(num_conta)
    if conta != None:
        cpf_digitado = int(input('Digite seu CPF (apenas números): '))
        if cpf_digitado == conta['usuario']:
            print('CPF válido!')
            print(f"Senha: {conta['senha']}")
        else:
            print('CPF inválido!')
    else:
        print('Conta não existe!')

def login(contas):
    print('Efetuar Login')
    num_digitado = int(input('Conta: '))
    senha_digitada = input('senha: ')
    conta = get_conta(num_digitado)
    if conta != None:
        nome = conta.cliente.nome
        if conta.verifica_senha(senha_digitada):
            print(f"Login Efetuado com Sucesso!")
            print(f"Bem vindo(a): {nome}")
            logado(conta)
        else:
            print('Senha inconrreta, porém conta Existe!')
            

def logado(conta):
    menu1 = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [c] Criar Nova Conta
    [q] Sair

    => """
    
    while True:
            op = input(menu1)

            if op == "d":
                valor = float(input("Informe o valor do depósito: "))
                Deposito(valor=valor).registrar(conta=conta)

            elif op == "s":
                valor = float(input("Informe o valor de Saque: "))
                Saque(valor=valor).registrar(conta=conta)
      
            elif op == "e":
               print("\nExtrato\n".center(30))
               for c, transacao in enumerate(conta.historico.transacoes):
                print((c+1), end=' ')
                for item in transacao.items():
                    print(f"{item[1]:<10}", end =" ")
                print()

            elif op == "q":
                break
            elif op == "c":
                print('-='*25)
                print(f"Caro (a) {conta.cliente.nome}")
                print('Para Criar uma nova conta, digite a:')
                print('-='*25)
                senha = str(input('Nova Senha: '))

                conta = criar_conta_corrente(senha=senha, usuario=conta.cliente)
                print('Conta criada e logada com Sucesso!')

            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")
                

def mostrar_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    if extrato != '':
        print(extrato)
    else:
        print("Não foram realizadas movimentações.")
    print('------------------------------------------')
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def get_conta(num_conta):
    for c in contas:
        if num_conta == c.numero:
            return c

def listar_contas():
    
    for conta in contas:
        print(f"conta: {conta.numero}, Agência: {conta.agencia}, CPF: {conta.cliente.cpf}, nome: {conta.cliente.nome}")


def criar_teste():
    nome = 'José teste'
    data_nascimento = '28/01/1976'
    endereço = 'R. Frade Coutinho, 132 - Morumbi - São Paulo - SP'
    cpf = 43612310033
    senha = '12345'

    criar_usuario(nome=nome, data_nascimento=data_nascimento, endereço=endereço, cpf=cpf, senha=senha)

    nome = 'Silvio'
    data_nascimento = '01/03/1976'
    endereço = 'av. Chucri Zaidan, 132 - Morumbi - São Paulo - SP'
    cpf = 43612310099
    senha = '12345'
    
    criar_usuario(nome=nome, data_nascimento=data_nascimento, endereço=endereço, cpf=cpf, senha=senha)


    
#Programa Principal

menu0 = """

[1] Realizar Login
[2] Esqueci a senha
[3] Criar Novo usuário
[4] Listar Contas
[5] Sair

=> """


usuarios = list()
contas = list()


criar_teste()

stop = 0
while True:
    op1 = input(menu0)
    if op1 == '1':
        login(contas)
    elif op1 == '2':
        senha_esquecida(int(input('Digite a conta: ')))

    elif op1 == '3':
        print('')
        nome = str(input('Nome: '))
        data_nascimento = str(input('Data de Nascinento: '))
        cpf = int(input('CPF: '))
        endereço = str(input('Endereço: '))
        senha = str(input('Senha: '))

        criar_usuario(nome, data_nascimento, cpf, senha, usuarios)
    elif op1 == '4':
        listar_contas()
    elif op1 == '5':
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
    



        


            #elif op == "s":
            #    valor = float(input("Informe o valor do saque: "))
            #    saque(saldo = saldo, valor = valor, extrato = extrato, limite = limite, numero_saques = numero_saques, LIMITE_SAQUES = LIMITE_SAQUES)

            #elif op == "e":  #FINALIZADA
            #    extrato(saldo, extrato = extrato)

            