def cabecalho():
    return ('\033[1m*-*-' * 6)[:-1] + '\033[0m'

def menu():
    menu_text = """
    \033[1m[1]\tDEPOSITAR\033[0m
    \033[1m[2]\tSACAR\033[0m
    \033[1m[3]\tEXTRATO\033[0m
    \033[1m[4]\tNOVA CONTA\033[0m
    \033[1m[5]\tLISTAR CONTAS\033[0m
    \033[1m[6]\tNOVO USUÁRIO\033[0m
    \033[1m[0]\tSAIR\033[0m
    \033[1mDIGITE A OPÇÃO:\033[0m """

    return input(menu_text)

def mensagem_retorno():
    return input('\033[96mDESEJA VOLTAR AO MENU?\nSIM : aperte ENTER\nNÃO : digite N pra encerrar a sessão\033[0m').upper()

def mensagem_tchau():
    print('\033[93mOBRIGADO E VOLTE SEMPRE\033[0m')

def verificar_retorno():
    opcao = mensagem_retorno()
    if opcao == 'N':
        mensagem_tchau()
        return False
    return True

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"\033[1mDepósito:\tR$ {valor:.2f}\n\033[0m"
        print("\n\033[32mDEPOSITO REALIZADO\033[0m")
    else:
        print("\n\033[91mERRO, VALOR INVALIDO\033[0m")

    return saldo, extrato

def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n\033[1;31mERRO, VOCÊ NÃO TEM SALDO DISPONIVEL\033[0m")
    elif excedeu_limite:
        print("\n\033[1;31mERRO, VALOR DO SAQUE ULTRAPASSA O LIMITE\033[0m")
    elif excedeu_saques:
        print("\n\033[1;31mERRO, LIMITE DE SAQUES EXCEDIDOS\033[0m")
    elif valor > 0:
        saldo -= valor
        extrato += f"\033[1mSaque:\t\tR$ {valor:.2f}\n\033[0m"
        numero_saques += 1
        print("\n\033[32mSAQUE REALIZADO\033[0m")
    else:
        print("\n\033[91mERRO, VALOR INVALIDO\033[0m")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n\033[1m================ EXTRATO ================\033[0m")
    if not extrato:
        print("\033[1mNÃO FORAM REALIZADAS TRANSAÇÕES\033[0m")
    else:
        print(extrato)
    print(f"\n\033[1mSALDO:\t\tR$ {saldo:.2f}\033[0m")
    print("\033[1m==========================================\033[0m")

def criar_usuario(usuarios):
    cpf = input("\033[1mINFORME O CPF (somente número): \033[0m")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n\033[91mUSUARIO COM ESSE CPF JÁ FOI CADASTRADO\033[0m")
        return

    nome = input("\033[1mNOME COMPLETO: \033[0m")
    data_nascimento = input("\033[1mDATA DE NASCIMENTO(dd-mm-aaaa): \033[0m")
    endereco = input("\033[1mENDEREÇO(rua, numero e bairro, cidade / estado): \033[0m")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\033[32mUSUARIO CRIADO\033[0m")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("\033[1mCPF DO TITULAR: \033[0m")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n\033[32mCONTA CRIADA COM SUCESSO\033[0m")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n\033[91mUSUARIO NÃO ENCONTRADO\033[0m")
    return None

def listar_contas(contas):
    for conta in contas:
        linha = f"""
        \033[1mAGÊNCIA:\t{conta['agencia']}\033[0m
        \033[1mC/C:\t\t{conta['numero_conta']}\033[0m
        \033[1mTITULAR:\t{conta['usuario']['nome']}\033[0m
        """
        print("\033[1m" + "=" * 40 + "\033[0m")
        print(linha.strip())
        print("\033[1m" + "=" * 40 + "\033[0m")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    contass = 0

    while True:
        print(cabecalho())
        print('\033[32m\tBANCO DIGITAL\033[0m')
        print(cabecalho())
        opcao = menu()

        if opcao == "1":
            valor = float(input("\033[1mVALOR DO DEPOSITO: \033[0m"))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("\033[1mVALOR DO SAQUE: \033[0m"))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                contass += 1

        elif opcao == "5":
            if contass >= 1:
                listar_contas(contas)
            else:
                print('\033[91mNENHUMA CONTA CADASTRADA\033[0m')

        elif opcao == "6":
            criar_usuario(usuarios)

        elif opcao == "0":
            mensagem_tchau()
            break

        else:
            print("\033[91mERRO, OPÇÃO INVALIDA\033[0m")

        if not verificar_retorno():
            break

if __name__ == "__main__":
    main()
