# Plataforma de Certificados Acadêmicos Tokenizados (Soulbound NFTs)

Projeto desenvolvido para a disciplina de Criptomoedas e Blockchain. Implementa um sistema de emissão de diplomas digitais utilizando Smart Contracts na rede Ethereum.

## 📋 Sobre o Projeto

Uma aplicação que permite a universidades emitirem diplomas como **Soulbound Tokens (SBTs)**. Diferente de NFTs comuns, estes tokens são **intransferíveis**, garantindo que o aluno não possa "vender" ou transferir seu diploma para outra carteira, mantendo a integridade da identidade acadêmica.

## 🛠 Tecnologias

- **Blockchain:** Ethereum (EVM)
- **Linguagem:** Solidity (Smart Contract)
- **Backend:** Python (Web3.py)
- **Padrão:** ERC-721 (modificado para SBT)

## 📝 Justificativas (Requisitos do Projeto)

### Por que Blockchain?

A blockchain garante **autenticidade imutável** e **verificação pública**.

- **Ganho:** Elimina fraudes de diplomas e reduz o tempo de verificação por empregadores de dias para milissegundos.
- **Perda:** Custo de taxa de rede (Gas), mitigado pelo uso de redes Layer-2.

### Por que Ethereum?

Escolhida pela **universalidade**. Um diploma precisa ser verificável por qualquer entidade no mundo (público), e não apenas por membros de uma rede fechada (como no Hyperledger Fabric). O padrão ERC-721 fornece a estrutura ideal para identidade única.

### Soluções de Mercado

1. **Blockcerts (MIT):** Padrão aberto para credenciais.
2. **Acreditta:** Emissão de badges digitais na América Latina.
3. **POAP:** Protocolo de prova de presença.

## 📊 Dados da Implementação

- **Linhas de Código (Solidity):** ~35 linhas
- **Linhas de Código (Python):** ~90 linhas
- **Desempenho:**
  - Emissão Local (Ganache): < 100ms
  - Custo de Gas estimado: ~150.000 gwei por diploma

## 🚀 Como Rodar

### Pré-requisitos

- Python 3.11.5 (gerenciado via pyenv)
- Ganache rodando em `http://127.0.0.1:7545`
- Contrato deployado no Ganache

### Instalação

1. **Ative o ambiente virtual:**
   ```bash
   source venv/bin/activate
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
   Ou instale diretamente:
   ```bash
   pip install web3
   ```

### Execução

**IMPORTANTE:** Sempre ative o ambiente virtual antes de executar o script:

#### Opção 1: Script Python (CLI)
```bash
source venv/bin/activate
python3 app.py
```

#### Opção 2: Dashboard Web (Streamlit) - Recomendado
```bash
source venv/bin/activate
streamlit run dashboard.py
```

O dashboard abrirá automaticamente no navegador em `http://localhost:8501`

**Funcionalidades do Dashboard:**
- 📊 Visão geral da conexão com a blockchain
- 🎓 Interface visual para emitir certificados
- 📜 Consulta de certificados por endereço
- 📈 Estatísticas da rede em tempo real
- ⚙️ Configurações acessíveis via sidebar

## Por que usar ambiente virtual?

O ambiente virtual (`venv`) isola as dependências do projeto, garantindo que:
- As bibliotecas instaladas não conflitem com outros projetos
- O projeto funcione mesmo se você tiver múltiplas versões do Python
- Outras pessoas possam replicar o ambiente exatamente

## 🔧 Solução de Problemas

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
