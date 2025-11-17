# DiplomaNFT - Sistema de Emissão de Certificados na Blockchain

Projeto Python para emissão de certificados (NFTs) na blockchain usando Web3.

## Pré-requisitos

- Python 3.11.5 (gerenciado via pyenv)
- Ganache rodando em `http://127.0.0.1:7545`
- Contrato deployado no Ganache

## Instalação

1. **Ative o ambiente virtual:**
   ```bash
   source venv/bin/activate
   ```

2. **Instale as dependências (se necessário):**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

**IMPORTANTE:** Sempre ative o ambiente virtual antes de executar o script:

```bash
source venv/bin/activate
python3 app.py
```

## Por que usar ambiente virtual?

O ambiente virtual (`venv`) isola as dependências do projeto, garantindo que:
- As bibliotecas instaladas não conflitem com outros projetos
- O projeto funcione mesmo se você tiver múltiplas versões do Python
- Outras pessoas possam replicar o ambiente exatamente

## Solução de Problemas

Se você receber `ModuleNotFoundError: No module named 'web3'`:

1. Certifique-se de que o ambiente virtual está ativado:
   ```bash
   source venv/bin/activate
   ```

2. Verifique se o web3 está instalado:
   ```bash
   pip list | grep web3
   ```

3. Se não estiver instalado:
   ```bash
   pip install -r requirements.txt
   ```

