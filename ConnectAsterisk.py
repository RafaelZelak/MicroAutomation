import asterisk.manager

# Configurações do Asterisk
host = 'IPAsterisk'
port = 5038
username = 'admin'
secret = 'senhaADM'

# Conectar ao AMI
manager = asterisk.manager.Manager()
try:
    manager.connect(host, port)
    manager.login(username, secret)

    # Executar comando para listar ramais
    response = manager.command('sip show peers')

    # Verificar e processar a resposta para extrair os ramais
    peers = []
    for message in response.response:
        lines = message.split('\n')
        for line in lines:
            line = line.strip()
            print(f"Linha de 'sip show peers': {line}")  # Depuração
            if line and line[0].isdigit():
                parts = line.split()
                if len(parts) > 0:
                    ramal = parts[0].split('/')[0]  # Extrai o ramal
                    peers.append(ramal)

    # Inicializar lista para armazenar ramais e senhas
    peer_passwords = []

    # Executar comando para cada ramal e obter a senha
    for peer in peers:
        command = f'sip show peer {peer}'
        response = manager.command(command)
        
        # Processar a resposta para extrair a senha
        for message in response.response:
            lines = message.split('\n')
            for line in lines:
                line = line.strip()
                print(f"Linha de 'sip show peer {peer}': {line}")  # Depuração
                if 'Secret' in line or 'Password' in line:
                    # Extrai a senha
                    password = line.split(':')[1].strip()
                    peer_passwords.append((peer, password))
                    break

    # Exibir a lista de ramais e senhas
    print("\nLista de ramais e senhas:\n")
    for peer, password in peer_passwords:
        print(f"Ramal: {peer}, Senha: {password}")

except asterisk.manager.ManagerSocketException as e:
    print(f"Erro ao conectar ao Asterisk Manager Interface: {e}")
except asterisk.manager.ManagerAuthException as e:
    print(f"Erro de autenticação ao conectar ao Asterisk Manager Interface: {e}")
except asterisk.manager.ManagerException as e:
    print(f"Erro ao executar comando no Asterisk Manager Interface: {e}")
finally:
    # Fechar conexão
    manager.close()
