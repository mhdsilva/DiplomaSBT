import json
import streamlit as st
from web3 import Web3
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="DiplomaNFT Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<p class="main-header">🎓 Plataforma de Certificados Acadêmicos Tokenizados</p>', unsafe_allow_html=True)

# Sidebar - Configurações
st.sidebar.header("⚙️ Configurações")

# Configurações da Blockchain
rpc_url = st.sidebar.text_input(
    "RPC URL",
    value="http://127.0.0.1:7545",
    help="Endereço do Ganache ou outro provider Ethereum"
)

# Configurações do Contrato
st.sidebar.subheader("📄 Contrato")
contract_address = st.sidebar.text_input(
    "Endereço do Contrato",
    value="0x01E60d7c05ac1b5E10245dD7881c0aC4fc6d99D2",
    help="Endereço do contrato deployado"
)

# Configurações da Universidade
st.sidebar.subheader("🏛️ Universidade")
private_key_universidade = st.sidebar.text_input(
    "Chave Privada",
    type="password",
    value="0x63d4d69e3e37bbc3a8ebebef47143042b75800e5e15c9c5520c41305cd99e23e",
    help="Private key da conta da universidade"
)

public_key_universidade = st.sidebar.text_input(
    "Endereço Público",
    value="0xee4b2B2680E23b2dedf7b7896B161702EDD985E2",
    help="Endereço da conta da universidade"
)

# ABI do contrato (simplificado para o dashboard)
CONTRACT_ABI_JSON = [
    {
        "inputs": [
            {"internalType": "address", "name": "student", "type": "address"},
            {"internalType": "string", "name": "tokenURI", "type": "string"}
        ],
        "name": "issueDiploma",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Inicializar conexão Web3
@st.cache_resource
def init_web3(rpc_url):
    """Inicializa conexão com a blockchain"""
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        return w3
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")
        return None

# Função para verificar conexão
def check_connection(w3):
    """Verifica se está conectado à blockchain"""
    if w3 is None:
        return False, "Não foi possível inicializar a conexão"
    try:
        if w3.is_connected():
            block_number = w3.eth.block_number
            chain_id = w3.eth.chain_id
            return True, f"Conectado! Bloco: {block_number}, Chain ID: {chain_id}"
        else:
            return False, "Não conectado à blockchain"
    except Exception as e:
        return False, f"Erro: {str(e)}"

# Função para emitir certificado
def emitir_certificado(w3, contract, endereco_aluno, url_json_gist, private_key, public_key):
    """Emite um certificado (SBT) para o aluno"""
    try:
        # Validar endereço
        if not w3.is_address(endereco_aluno):
            return False, None, "Endereço inválido"
        
        aluno_checksum = w3.to_checksum_address(endereco_aluno)
        
        # Construir transação
        nonce = w3.eth.get_transaction_count(public_key)
        
        tx = contract.functions.issueDiploma(
            aluno_checksum,
            url_json_gist
        ).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 2000000,
            'gasPrice': w3.to_wei('20', 'gwei'),
            'nonce': nonce,
            'from': public_key
        })
        
        # Assinar transação
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        
        # Enviar transação
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        # Aguardar confirmação
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            return True, receipt, None
        else:
            return False, receipt, "Transação revertida"
            
    except Exception as e:
        return False, None, str(e)

# Inicializar Web3
w3 = init_web3(rpc_url)

# Verificar conexão
is_connected, connection_msg = check_connection(w3)

# Colunas principais
col1, col2, col3 = st.columns(3)

with col1:
    if is_connected:
        st.success("🟢 Conectado")
    else:
        st.error("🔴 Desconectado")
    
    st.caption(connection_msg)

with col2:
    if is_connected and w3:
        try:
            block_number = w3.eth.block_number
            st.metric("Bloco Atual", f"#{block_number}")
        except:
            st.metric("Bloco Atual", "N/A")

with col3:
    if is_connected and w3:
        try:
            chain_id = w3.eth.chain_id
            chain_name = "Ganache Local" if chain_id == 1337 else f"Chain {chain_id}"
            st.metric("Rede", chain_name)
        except:
            st.metric("Rede", "N/A")

st.divider()

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🎓 Emitir Certificado", "📜 Consultar Certificados", "📈 Estatísticas"])

# TAB 1: Dashboard
with tab1:
    st.header("📊 Visão Geral")
    
    if not is_connected:
        st.error("⚠️ Não é possível continuar sem conexão com a blockchain.")
        st.info("Verifique se o Ganache está rodando e configure o RPC URL corretamente.")
    else:
        # Informações do contrato
        st.subheader("📄 Informações do Contrato")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Endereço do Contrato", value=contract_address, disabled=True)
        
        with col2:
            if contract_address and contract_address != "0x...":
                try:
                    contract = w3.eth.contract(
                        address=w3.to_checksum_address(contract_address),
                        abi=CONTRACT_ABI_JSON
                    )
                    st.success("✅ Contrato válido")
                except Exception as e:
                    st.error(f"❌ Erro ao carregar contrato: {e}")
                    contract = None
            else:
                st.warning("⚠️ Configure o endereço do contrato")
                contract = None
        
        # Informações da conta
        st.subheader("🏛️ Conta da Universidade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if public_key_universidade and public_key_universidade != "0x...":
                st.text_input("Endereço Público", value=public_key_universidade, disabled=True)
            else:
                st.warning("⚠️ Configure o endereço público")
        
        with col2:
            if public_key_universidade and public_key_universidade != "0x..." and w3:
                try:
                    balance = w3.eth.get_balance(public_key_universidade)
                    balance_eth = w3.from_wei(balance, 'ether')
                    st.metric("Saldo", f"{balance_eth:.4f} ETH")
                except:
                    st.metric("Saldo", "N/A")

# TAB 2: Emitir Certificado
with tab2:
    st.header("🎓 Emitir Novo Certificado")
    
    if not is_connected:
        st.error("⚠️ Conecte-se à blockchain primeiro!")
    elif not contract_address or contract_address == "0x...":
        st.error("⚠️ Configure o endereço do contrato nas configurações!")
    elif not private_key_universidade or private_key_universidade == "0x...":
        st.error("⚠️ Configure a chave privada nas configurações!")
    else:
        try:
            contract = w3.eth.contract(
                address=w3.to_checksum_address(contract_address),
                abi=CONTRACT_ABI_JSON
            )
            
            with st.form("emitir_certificado_form"):
                st.subheader("📝 Dados do Certificado")
                
                endereco_aluno = st.text_input(
                    "Endereço do Aluno (Ethereum)",
                    placeholder="0x...",
                    help="Endereço da carteira do aluno que receberá o certificado"
                )
                
                url_json_gist = st.text_input(
                    "URL dos Metadados (Gist)",
                    placeholder="https://gist.githubusercontent.com/...",
                    help="Link RAW do Gist com os dados do certificado em JSON"
                )
                
                submitted = st.form_submit_button("🚀 Emitir Certificado", use_container_width=True)
                
                if submitted:
                    if not endereco_aluno or not url_json_gist:
                        st.error("⚠️ Preencha todos os campos!")
                    else:
                        with st.spinner("Processando transação..."):
                            success, receipt, error = emitir_certificado(
                                w3,
                                contract,
                                endereco_aluno,
                                url_json_gist,
                                private_key_universidade,
                                public_key_universidade
                            )
                            
                            if success and receipt:
                                st.success("✅ Certificado emitido com sucesso!")
                                
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("Bloco", receipt.blockNumber)
                                
                                with col2:
                                    st.metric("Gas Usado", f"{receipt.gasUsed:,}")
                                
                                with col3:
                                    tx_hash_hex = w3.to_hex(receipt.transactionHash)
                                    st.text_input("Hash da Transação", value=tx_hash_hex[:20] + "...", disabled=True)
                                
                                st.balloons()
                            else:
                                st.error(f"❌ Erro ao emitir certificado: {error}")
                                
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")

# TAB 3: Consultar Certificados
with tab3:
    st.header("📜 Consultar Certificados")
    
    if not is_connected:
        st.error("⚠️ Conecte-se à blockchain primeiro!")
    elif not contract_address or contract_address == "0x...":
        st.error("⚠️ Configure o endereço do contrato nas configurações!")
    else:
        try:
            contract = w3.eth.contract(
                address=w3.to_checksum_address(contract_address),
                abi=CONTRACT_ABI_JSON
            )
            
            st.subheader("🔍 Buscar por Endereço")
            
            endereco_consulta = st.text_input(
                "Endereço do Aluno",
                placeholder="0x...",
                help="Digite o endereço para verificar os certificados"
            )
            
            if st.button("🔎 Consultar", use_container_width=True):
                if endereco_consulta and w3.is_address(endereco_consulta):
                    try:
                        endereco_checksum = w3.to_checksum_address(endereco_consulta)
                        balance = contract.functions.balanceOf(endereco_checksum).call()
                        
                        st.success(f"✅ Encontrado: {balance} certificado(s)")
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao consultar: {str(e)}")
                else:
                    st.error("⚠️ Endereço inválido!")
                    
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")

# TAB 4: Estatísticas
with tab4:
    st.header("📈 Estatísticas da Rede")
    
    if not is_connected:
        st.error("⚠️ Conecte-se à blockchain primeiro!")
    else:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            try:
                block_number = w3.eth.block_number
                st.metric("Bloco Atual", f"#{block_number:,}")
            except:
                st.metric("Bloco Atual", "N/A")
        
        with col2:
            try:
                chain_id = w3.eth.chain_id
                st.metric("Chain ID", chain_id)
            except:
                st.metric("Chain ID", "N/A")
        
        with col3:
            try:
                if public_key_universidade and public_key_universidade != "0x...":
                    balance = w3.eth.get_balance(public_key_universidade)
                    balance_eth = w3.from_wei(balance, 'ether')
                    st.metric("Saldo ETH", f"{balance_eth:.4f}")
                else:
                    st.metric("Saldo ETH", "N/A")
            except:
                st.metric("Saldo ETH", "N/A")
        
        with col4:
            try:
                gas_price = w3.eth.gas_price
                gas_price_gwei = w3.from_wei(gas_price, 'gwei')
                st.metric("Gas Price", f"{gas_price_gwei:.2f} gwei")
            except:
                st.metric("Gas Price", "N/A")
        
        st.divider()
        
        # Informações adicionais
        st.subheader("ℹ️ Informações da Rede")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.write("**RPC URL:**", rpc_url)
            st.write("**Endereço do Contrato:**", contract_address)
        
        with info_col2:
            if public_key_universidade and public_key_universidade != "0x...":
                st.write("**Conta da Universidade:**", public_key_universidade[:10] + "..." + public_key_universidade[-8:])
            else:
                st.write("**Conta da Universidade:**", "Não configurado")

# Rodapé
st.divider()
st.caption("🎓 Plataforma de Certificados Acadêmicos Tokenizados - Desenvolvido para disciplina de Criptomoedas e Blockchain")

