import threading
import pjsua2 as pj
import sys

class MyAccount(pj.Account):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def onRegState(self, prm):
        print(f"Account {self.config.idUri} - Registration status: ", prm.code)
        if prm.code == 200:
            print("Registrado com sucesso!")
        else:
            print("Falha no registro.")
            print(f"Código de erro: {prm.code}")
            print(f"Razão da falha: {prm.reason}")

def create_endpoint():
    ep = pj.Endpoint()
    ep_cfg = pj.EpConfig()
    log_cfg = pj.LogConfig()
    log_cfg.level = 4
    log_cfg.consoleLevel = 4
    ep_cfg.logConfig = log_cfg

    ep.libCreate()
    ep.libInit(ep_cfg)
    return ep

def manage_accounts(users, ep):
    try:
        transport_cfg = pj.TransportConfig()
        transport_cfg.port = 5060
        ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, transport_cfg)
        ep.libStart()
        print("Endpoint inicializado.")
        
        accounts = []
        for user in users:
            acc_cfg = pj.AccountConfig()
            acc_cfg.idUri = f"sip:{user['username']}@{user['domain']}"
            acc_cfg.regConfig.registrarUri = f"sip:{user['domain']}"
            acc_cfg.sipConfig.authCreds.append(pj.AuthCredInfo("digest", "*", user["username"], 0, user["password"]))

            account = MyAccount(acc_cfg)
            account.create(acc_cfg)
            accounts.append(account)
            print(f"Conta criada para {user['username']}.")

        try:
            while True:
                ep.libHandleEvents(1000)
                user_input = input("Digite 'logout' para desconectar todas as contas: ")
                if user_input.lower() == 'logout':
                    break
        except KeyboardInterrupt:
            print("Interrupção detectada. Desconectando contas...")
        finally:
            for account in accounts:
                account.shutdown()  # Use shutdown() instead of delete()
                print(f"Conta {account.config.idUri} deletada.")
    except pj.Error as e:
        print(f"Falha ao inicializar o endpoint: {e}")

if __name__ == "__main__":
    try:
        ep = create_endpoint()

        users = [
            {"username": "1000", "password": "asteriskRamalPass", "domain": "192.168.15.252"},
            {"username": "1040", "password": "asteriskRamalPass", "domain": "192.168.15.252"}
        ]

        manage_accounts(users, ep)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        if ep:
            ep.libDestroy()
            print("Endpoint destroyed.")
