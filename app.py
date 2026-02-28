import streamlit as st
from auth import GerenciadorUsuarios
import importlib
import time

# Configuração da página
st.set_page_config(
    page_title="Portal Multiplataforma",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado global
st.markdown("""
    <style>
    /* Estilos globais */
    .stApp {
        background: #f8f9fa;
    }
    
    /* Cards do dashboard */
    .dashboard-card {
        background: white;
        border-radius: 20px;
        padding: 30px 20px;
        margin: 10px 0;
        text-align: center;
        border: 2px solid rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        border-color: transparent;
    }
    
    .dashboard-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .dashboard-card:hover::before {
        transform: scaleX(1);
    }
    
    .card-icon {
        font-size: 4em;
        margin-bottom: 20px;
    }
    
    .card-title {
        color: #333;
        margin-bottom: 10px;
        font-size: 1.5em;
        font-weight: 600;
    }
    
    .card-description {
        color: #666;
        margin-bottom: 20px;
        font-size: 0.9em;
    }
    
    /* Header do portal */
    .portal-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        text-align: center;
    }
    
    /* Botões personalizados */
    .stButton > button {
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Métricas */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Tabs personalizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        background-color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização
if 'gerenciador_usuarios' not in st.session_state:
    st.session_state.gerenciador_usuarios = GerenciadorUsuarios()

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if 'pagina' not in st.session_state:
    st.session_state.pagina = "login"

if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = None

if 'plataforma_atual' not in st.session_state:
    st.session_state.plataforma_atual = None

# Definição das plataformas
PLATAFORMAS = [
    {
        "id": "agendamento",
        "nome": "Sistema de Agendamento",
        "icone": "📅",
        "cor": "#FF4B4B",
        "cor_gradiente": "linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%)",
        "descricao": "Gerencie agendamentos, clientes e serviços",
        "modulo": "sistema_agendamento",
        "stats": "45 agendamentos hoje"
    },
    {
        "id": "vendas",
        "nome": "Sistema de Vendas",
        "icone": "💰",
        "cor": "#00CC96",
        "cor_gradiente": "linear-gradient(135deg, #00CC96 0%, #00E6A8 100%)",
        "descricao": "Controle de vendas, produtos e clientes",
        "modulo": "sistema_vendas",
        "stats": "R$ 2.450 em vendas hoje"
    },
    {
        "id": "financeiro",
        "nome": "Sistema Financeiro",
        "icone": "📊",
        "cor": "#FFA500",
        "cor_gradiente": "linear-gradient(135deg, #FFA500 0%, #FFB52E 100%)",
        "descricao": "Fluxo de caixa, contas e relatórios",
        "modulo": "sistema_financeiro",
        "stats": "Saldo: R$ 15.780"
    },
    {
        "id": "rh",
        "nome": "Sistema de RH",
        "icone": "👥",
        "cor": "#6C3483",
        "cor_gradiente": "linear-gradient(135deg, #6C3483 0%, #8E44AD 100%)",
        "descricao": "Gestão de funcionários e folha",
        "modulo": "sistema_rh",
        "stats": "45 funcionários ativos"
    },
    {
        "id": "estoque",
        "nome": "Sistema de Estoque",
        "icone": "📦",
        "cor": "#3498DB",
        "cor_gradiente": "linear-gradient(135deg, #3498DB 0%, #5DADE2 100%)",
        "descricao": "Controle de estoque e fornecedores",
        "modulo": "sistema_estoque",
        "stats": "1.456 itens em estoque"
    },
    {
        "id": "relatorios",
        "nome": "Sistema de Relatórios",
        "icone": "📈",
        "cor": "#E74C3C",
        "cor_gradiente": "linear-gradient(135deg, #E74C3C 0%, #EC7063 100%)",
        "descricao": "Relatórios gerenciais e KPIs",
        "modulo": "sistema_relatorios",
        "stats": "12 relatórios disponíveis"
    }
]

def tela_login():
    """Tela de login do sistema"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 40px; background: white; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);'>
                <h1 style='color: #333; font-size: 2.5em; margin-bottom: 10px;'>🚀 Portal Multiplataforma</h1>
                <p style='color: #666; margin-bottom: 30px;'>Acesse todas as plataformas em um só lugar</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("📧 E-mail", placeholder="seu@email.com")
            senha = st.text_input("🔒 Senha", type="password", placeholder="••••••••")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("🔑 Entrar", type="primary", use_container_width=True)
            with col2:
                if st.form_submit_button("📝 Cadastrar", use_container_width=True):
                    st.session_state.pagina = "cadastro"
                    st.rerun()
            
            if submit:
                if email and senha:
                    usuario = st.session_state.gerenciador_usuarios.autenticar(email, senha)
                    if usuario:
                        st.session_state.usuario_logado = usuario
                        st.session_state.autenticado = True
                        st.success("✅ Login realizado com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ E-mail ou senha inválidos!")
                else:
                    st.warning("⚠️ Preencha todos os campos!")

def tela_cadastro():
    """Tela de cadastro de usuário"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 30px; background: white; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);'>
                <h1 style='color: #333;'>📝 Criar Conta</h1>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("cadastro_form"):
            nome = st.text_input("👤 Nome completo")
            email = st.text_input("📧 E-mail")
            senha = st.text_input("🔒 Senha", type="password")
            confirmar_senha = st.text_input("🔒 Confirmar senha", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✅ Cadastrar", type="primary", use_container_width=True):
                    if senha != confirmar_senha:
                        st.error("❌ As senhas não conferem!")
                    elif nome and email and senha:
                        sucesso, mensagem = st.session_state.gerenciador_usuarios.criar_usuario(
                            nome=nome,
                            email=email,
                            senha=senha
                        )
                        if sucesso:
                            st.success(mensagem)
                            time.sleep(2)
                            st.session_state.pagina = "login"
                            st.rerun()
                        else:
                            st.error(mensagem)
                    else:
                        st.warning("⚠️ Preencha todos os campos!")
            
            with col2:
                if st.form_submit_button("↩️ Voltar", use_container_width=True):
                    st.session_state.pagina = "login"
                    st.rerun()

def dashboard_principal():
    """Dashboard principal com cards das plataformas"""
    
    # Header
    st.markdown(f"""
        <div class='portal-header'>
            <h1>🚀 Bem-vindo, {st.session_state.usuario_logado.nome}!</h1>
            <p>Selecione uma plataforma para começar a trabalhar</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Informações do usuário
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col2:
        st.markdown(f"📅 {time.strftime('%d/%m/%Y')}")
    with col3:
        if st.button("🚪 Sair", type="secondary", use_container_width=True):
            st.session_state.autenticado = False
            st.session_state.usuario_logado = None
            st.session_state.pagina = "login"
            st.rerun()
    
    st.markdown("---")
    
    # Grid de cards (3x2)
    for i in range(0, len(PLATAFORMAS), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(PLATAFORMAS):
                plataforma = PLATAFORMAS[i + j]
                with cols[j]:
                    # Card com efeito hover
                    st.markdown(f"""
                        <div class='dashboard-card' id='card-{plataforma["id"]}' 
                             style='border-left: 4px solid {plataforma["cor"]};'>
                            <div class='card-icon'>{plataforma["icone"]}</div>
                            <h3 class='card-title' style='color: {plataforma["cor"]};'>{plataforma["nome"]}</h3>
                            <p class='card-description'>{plataforma["descricao"]}</p>
                            <p style='color: #999; font-size: 0.8em;'>{plataforma["stats"]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Botão de acesso
                    if st.button(f"🔓 Acessar {plataforma['nome']}", key=f"btn_{plataforma['id']}", use_container_width=True):
                        st.session_state.plataforma_atual = plataforma["id"]
                        st.session_state.pagina = "plataforma"
                        st.rerun()
    
    # Últimos acessos
    st.markdown("---")
    st.subheader("📋 Últimos Acessos")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📅 Sistema de Agendamento - 10:30")
    with col2:
        st.info("💰 Sistema de Vendas - 09:15")
    with col3:
        st.info("📊 Sistema Financeiro - 08:45")

def pagina_plataforma():
    """Página da plataforma selecionada"""
    
    # Encontrar plataforma atual
    plataforma_atual = next((p for p in PLATAFORMAS if p["id"] == st.session_state.plataforma_atual), None)
    
    if not plataforma_atual:
        st.error("Plataforma não encontrada!")
        return
    
    # Barra de navegação
    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col1:
        if st.button("← Voltar", type="secondary", use_container_width=True):
            st.session_state.pagina = "dashboard"
            st.session_state.plataforma_atual = None
            st.rerun()
    
    with col2:
        st.markdown(f"<h1 style='text-align: center; color: {plataforma_atual['cor']};'>{plataforma_atual['icone']} {plataforma_atual['nome']}</h1>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<p style='text-align: right;'>👤 {st.session_state.usuario_logado.nome}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Importar e renderizar o módulo da plataforma
    try:
        modulo = importlib.import_module(plataforma_atual["modulo"])
        modulo.render()
    except Exception as e:
        st.error(f"Erro ao carregar plataforma: {e}")
        st.info("Verifique se o arquivo do módulo existe e está funcionando corretamente.")

def main():
    """Função principal"""
    
    # Roteamento
    if not st.session_state.autenticado:
        if st.session_state.pagina == "cadastro":
            tela_cadastro()
        else:
            tela_login()
    else:
        if st.session_state.pagina == "plataforma":
            pagina_plataforma()
        else:
            dashboard_principal()

if __name__ == "__main__":
    main()