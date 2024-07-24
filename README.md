# MicroAutomation

### Repositódio destinado a todas as Micro Automações criadas, por mim, para a Setup Tecnologia

## `SittaxAutoGit.py`

Este script Python busca e baixa automaticamente a versão mais recente de um arquivo `.exe` de um repositório do GitHub.

### Funcionalidade

O script realiza as seguintes ações:

1. **Busca a Última Versão:** Consulta a API do GitHub para obter a lista de lançamentos do repositório especificado.
2. **Seleciona o Arquivo `.exe`:** Identifica o arquivo `.exe` mais recente disponível no lançamento mais recente.
3. **Baixa o Arquivo:** Usa `wget` para fazer o download do arquivo `.exe` encontrado.

### Requisitos

- Python 3.x
- Bibliotecas Python:
  - `requests` (para fazer requisições HTTP)
  - `subprocess` (para executar comandos do sistema)
- `wget` (para baixar o arquivo .exe)

### Uso

1. **Configuração:**
Substitua os parâmetros `repo_owner` e `repo_name` na função `get_latest_release_exe_link` com o proprietário e o nome do repositório GitHub desejado.

```python
get_latest_release_exe_link('OWNER', 'REPOSITORY')
````

2. **Execução:**

Execute o script Python:
  
````bash
python script.py
````
O script imprimirá a versão mais recente, a data do lançamento e o link de download do arquivo .exe. O download será iniciado automaticamente.

### Exemplo
Para o repositório DevEderNO/nf-monitor, o comando para buscar e baixar a última versão seria:

````python
get_latest_release_exe_link('DevEderNO', 'nf-monitor')
````

### Observações
O script assume que há apenas um arquivo .exe em cada lançamento. Se houver vários arquivos ou arquivos .blockmap, o script pode não funcionar conforme o esperado.
Certifique-se de que wget está instalado e disponível no seu PATH.
