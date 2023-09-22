def criar_usuario(nome, data_nascimento, endereço, cpf, senha):
    usuario = dict()
    dados = dict()

    dados['Nome'] = nome
    dados['Data de Nascimento'] = data_nascimento
    dados['CPF'] = cpf
    dados['endereço'] = endereço
    

    if usuarios.count(cpf) == 0:
        usuario = {cpf : dados}   
        usuarios.append(usuario)
        criar_conta_corrente(cpf, senha)
    else:
        print(f"Usuário com cpf: {cpf} já existe!")


def criar_conta_corrente(cpf, senha, agencia = '0001'):
    nova_conta = dict()
    # Criar Dados
    
    num_conta = len(contas) + 1
    nova_conta['agencia'] = agencia
    nova_conta['senha'] = senha

    # Criar dados relacionados a Dinheiro
    nova_conta['saldo'] = 0
    nova_conta['limite'] = 500
    nova_conta['extrato'] = ''
    nova_conta['numero_saques'] = 0
    nova_conta['LIMITE_SAQUES'] = 3
    nova_conta['usuario'] = cpf

    conta_criada = {num_conta : nova_conta}  
    contas.append(conta_criada)

    print(f'''
          Conta Criada com Sucesso:
          Agencia: {nova_conta['agencia']}
          conta: {num_conta}
          CPF: {cpf}
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
    conta_digitada = int(input('Conta: '))
    senha_digitada = input('senha: ')
    dados_conta = get_conta(conta_digitada)
    if dados_conta != None:
        dados_user = get_usuario(cpf=dados_conta.get('usuario'))
        nome = dados_user["Nome"]
        if dados_conta['senha'] == senha_digitada:
            print(f"Login Efetuado com Sucesso!")
            print(f"Bem vindo(a): {nome}")
            logado(conta_digitada)
        else:
            print('Senha inconrreta, porém conta Existe!')
            

def logado(num_conta):
    posição = num_conta - 1
    conta = contas[posição][num_conta]

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
                saldo, extrato = deposito(conta.get("saldo"), valor, conta.get('extrato'))
                conta['saldo'] = saldo
                conta['extrato'] = extrato
                # update_conta(conta)

            elif op == "s":
                valor = float(input("Informe o valor de Saque: "))
                
                saldo, extrato, numero_saques = saque(saldo = conta.get("saldo"),
                    valor = valor,
                    extrato = conta.get("extrato"),
                    limite = conta.get("limite"),
                    numero_saques = conta.get("numero_saques"),
                    LIMITE_SAQUES = conta.get("LIMITE_SAQUES"))
                
                conta['saldo'] = saldo
                conta['extrato'] = extrato
                conta['numero_saques'] = numero_saques

                           
            elif op == "e":
               mostrar_extrato(conta.get('saldo'), conta.get('extrato')) 

            elif op == "q":
                break
            elif op == "c":
                cpf = conta.get('usuario')
                usuario = get_usuario(cpf)
                print('-='*25)
                print(f"Caro (a) {usuario['Nome']}")
                print('Para Criar uma nova conta, digite a:')
                print('-='*25)
                senha = str(input('Nova Senha: '))

                conta = criar_conta_corrente(senha=senha, cpf=cpf)
                print('Conta criada e logada com Sucesso!')

            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")
                

def deposito(saldo, valor, extrato):
    # positional only

    if valor > 0:
        saldo += valor
        extrato += "Depósito: R$ {:.2f}\n".format(valor)
        print("Depositado o valor de: R$ {:.2f}".format(valor))
        print('Saldo: {:.2f}'.format(saldo))
        return saldo, extrato       
    
        
def saque(saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    # Keyword Only
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES
    
    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente. (Saldo: {:.2f})".format(saldo))
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite. (Saldo: {:.2f})".format(saldo))

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += "Saque: R$ {:.2f}\n".format(valor)
        numero_saques += 1
        print('Valor sacado: {:.2f}'.format(valor))
        print('Saldo: {:.2f}'.format(saldo))

    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques


def mostrar_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    if extrato != '':
        print(extrato)
    else:
        print("Não foram realizadas movimentações.")
    print('------------------------------------------')
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def get_usuario(cpf):
        teste = dict()
        for usuario in usuarios:
            for k,v in usuario.items():
                if k == cpf:
                    return v

def get_conta(num_conta):
    for c in contas:
        for k, v in c.items():
            if num_conta == k:
                return v

def listar_contas():
    
    for conta in contas:
        for k, v in conta.items():
            cpf = v.get('usuario')
            agencia = v.get('agencia')
            dados_user = get_usuario(cpf)
            nome = dados_user['Nome']
            print(f"conta: {k}, Agência: {agencia}, CPF: {cpf}, nome: {nome}")



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

            
