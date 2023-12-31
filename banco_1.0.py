#Operações sacar, depositar, visualizar extrato
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=>"""

saldo = 0
limite = 500.00
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "d":
        print("Deposito")
        deposito = float(input("Quanto gostaria de depositar? "))

        if deposito > 0:
            saldo += deposito
            print("\nSeu saldo é de R$ {:.2f}".format(saldo))
            extrato += f"Deposito: \tR$ {deposito:.2f}\n"
        else:
            print(f"\nNão é possível depositar o valor R$ {deposito:.2f}")

    if opcao == "s":
        if saldo == 0:
            print("Você não possui Saldo!")
        
        elif numero_saques < LIMITE_SAQUES:
            print("Saldo: R$ {:.2f}".format(saldo))
            saque = float(input("Valor de Saque: R$"))

            if saque <= saldo:
                numero_saques += 1
                saldo -= saque
                print("\nValor de R$ {:.2f} sacado com SUCESSO!".format(saque))
                extrato += f"Saque: \t\tR$ {saque:.2f}\n"
            
            else:
                print("\nNão é possível sacar R$ {:.2f}, pois seu saldo é menor!".format(saque))
        
        
        else:
            print("\nLimite de Saques diarios, já atingido!")
    
    if opcao == "e":
        if extrato != "":
            print("-=" * 15)
            print("EXTRATO".center(30))
            print("-=" * 15 +"\n")
            print(extrato)
            print("-=" * 15)
            print("Saldo Atual: \tR$ {:.2f}".format(saldo))
            print("-=" * 15)
        
        else:
            print("\nNão foram realizadas movimentações.")

    elif opcao == "q":
        break