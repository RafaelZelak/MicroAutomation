import paramiko
import re
import warnings

# Função para suprimir mensagens de aviso específicas
def suppress_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

# Configurações do servidor
hostname = '192.168.15.252'
port = 22
username = 'root'
password = 'Dydf%hhffjk5s588ik2u@ud7aDF'

def get_ramal_password(ramal):
    suppress_warnings()
    senha_ramal = None
    
    try:
        # Cria uma instância SSHClient
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username, password)
        
        # Executa o comando para ler o arquivo de configuração
        stdin, stdout, stderr = client.exec_command('cat /etc/asterisk/sip_additional.conf')
        output = stdout.read().decode()
        
        # Procura a senha do ramal
        pattern = rf'\[{ramal}\]\s+.*?secret=(\S+)'
        match = re.search(pattern, output, re.DOTALL)
        
        if match:
            senha_ramal = match.group(1)
    
    finally:
        client.close()
    
    return senha_ramal

# Exemplo de uso
ramal = '1100'  # Substitua pelo ramal desejado
senha_ramal = get_ramal_password(ramal)

if senha_ramal:
    print(f'{senha_ramal}')
else:
    print(f'Ramal {ramal} não encontrado ou senha não definida.')
