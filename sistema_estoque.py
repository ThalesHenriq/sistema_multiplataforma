import streamlit as st
import pandas as pd
import plotly.express as px
import random

def render():
    st.markdown("""
        <style>
        .estoque-header {
            background: linear-gradient(90deg, #3498DB 0%, #5DADE2 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }
        .estoque-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            border-left: 4px solid #3498DB;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="estoque-header">
            <h1>📦 Sistema de Estoque</h1>
            <p>Controle completo de estoque e fornecedores</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Itens", "1.456", "+45")
    with col2:
        st.metric("Valor em Estoque", "R$ 87.234", "+R$ 5.321")
    with col3:
        st.metric("Categorias", "23", "+2")
    with col4:
        st.metric("Fornecedores", "15", "+1")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Inventário", "⬇️ Entradas", "⬆️ Saídas", "🏭 Fornecedores"])
    
    with tab1:
        st.subheader("Inventário Atual")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            categoria_filtro = st.selectbox("Filtrar por Categoria", ["Todas", "Eletrônicos", "Vestuário", "Alimentos", "Móveis", "Papelaria"])
        with col2:
            estoque_filtro = st.selectbox("Status do Estoque", ["Todos", "Estoque Normal", "Estoque Baixo", "Em Falta"])
        
        # Dados simulados
        inventario = pd.DataFrame({
            'Código': ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008'],
            'Produto': ['Notebook', 'Mouse', 'Teclado', 'Monitor', 'Cadeira', 'Mesa', 'Caneta', 'Papel'],
            'Categoria': ['Eletrônicos', 'Eletrônicos', 'Eletrônicos', 'Eletrônicos', 'Móveis', 'Móveis', 'Papelaria', 'Papelaria'],
            'Quantidade': [15, 42, 28, 12, 8, 5, 150, 80],
            'Mínimo': [10, 30, 20, 10, 10, 5, 100, 100],
            'Máximo': [30, 100, 50, 25, 20, 15, 500, 300],
            'Valor Unit.': ['R$ 3.500', 'R$ 80', 'R$ 150', 'R$ 1.200', 'R$ 450', 'R$ 350', 'R$ 2', 'R$ 25'],
            'Valor Total': ['R$ 52.500', 'R$ 3.360', 'R$ 4.200', 'R$ 14.400', 'R$ 3.600', 'R$ 1.750', 'R$ 300', 'R$ 2.000']
        })
        
        # Aplicar filtros
        if categoria_filtro != "Todas":
            inventario = inventario[inventario['Categoria'] == categoria_filtro]
        
        # Destacar estoque baixo
        def highlight_estoque_baixo(row):
            qtd = int(row['Quantidade'])
            minimo = int(row['Mínimo'])
            if qtd <= minimo:
                return ['background-color: #FFB6C1'] * len(row)
            elif qtd <= minimo * 1.5:
                return ['background-color: #FFE4B5'] * len(row)
            return [''] * len(row)
        
        styled_inventario = inventario.style.apply(highlight_estoque_baixo, axis=1)
        st.dataframe(styled_inventario, use_container_width=True, hide_index=True)
        
        # Alertas de estoque
        estoque_baixo = inventario[inventario['Quantidade'].astype(int) <= inventario['Mínimo'].astype(int)]
        if not estoque_baixo.empty:
            st.warning(f"⚠️ {len(estoque_baixo)} produtos com estoque baixo!")
            st.dataframe(estoque_baixo[['Produto', 'Quantidade', 'Mínimo']], use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Registrar Entrada de Estoque")
        
        col1, col2 = st.columns(2)
        
        with col1:
            produto = st.selectbox("Produto", inventario['Produto'].tolist())
            quantidade = st.number_input("Quantidade", min_value=1, value=10)
            fornecedor = st.selectbox("Fornecedor", ["Fornecedor A", "Fornecedor B", "Fornecedor C", "Fornecedor D"])
            nota_fiscal = st.text_input("Número da Nota Fiscal")
        
        with col2:
            data_entrada = st.date_input("Data da Entrada")
            valor_unitario = st.number_input("Valor Unitário (R$)", min_value=0.01, format="%.2f")
            observacoes = st.text_area("Observações")
        
        if st.button("📥 Registrar Entrada", type="primary", use_container_width=True):
            st.success(f"Entrada de {quantidade} unidades de {produto} registrada com sucesso!")
        
        # Histórico de entradas
        st.subheader("Últimas Entradas")
        historico_entradas = pd.DataFrame({
            'Data': ['10/05/2024', '09/05/2024', '08/05/2024', '07/05/2024', '06/05/2024'],
            'Produto': ['Notebook', 'Mouse', 'Cadeira', 'Papel', 'Monitor'],
            'Quantidade': [10, 50, 5, 100, 8],
            'Fornecedor': ['Fornecedor A', 'Fornecedor B', 'Fornecedor C', 'Fornecedor A', 'Fornecedor D'],
            'NF': ['NF001', 'NF002', 'NF003', 'NF004', 'NF005'],
            'Valor Total': ['R$ 35.000', 'R$ 4.000', 'R$ 2.250', 'R$ 250', 'R$ 9.600']
        })
        
        st.dataframe(historico_entradas, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Registrar Saída de Estoque")
        
        col1, col2 = st.columns(2)
        
        with col1:
            produto_saida = st.selectbox("Produto (Saída)", inventario['Produto'].tolist(), key='saida')
            quantidade_saida = st.number_input("Quantidade (Saída)", min_value=1, value=1)
            destino = st.selectbox("Destino", ["Venda", "Uso Interno", "Devolução", "Perda"])
            cliente = st.text_input("Cliente (se venda)")
        
        with col2:
            data_saida = st.date_input("Data da Saída")
            responsavel = st.selectbox("Responsável", ["João", "Maria", "Carlos", "Ana"])
            observacoes_saida = st.text_area("Observações (Saída)")
        
        if st.button("📤 Registrar Saída", type="primary", use_container_width=True):
            st.success(f"Saída de {quantidade_saida} unidades de {produto_saida} registrada com sucesso!")
        
        # Histórico de saídas
        st.subheader("Últimas Saídas")
        historico_saidas = pd.DataFrame({
            'Data': ['10/05/2024', '09/05/2024', '08/05/2024', '07/05/2024', '06/05/2024'],
            'Produto': ['Mouse', 'Teclado', 'Papel', 'Caneta', 'Cadeira'],
            'Quantidade': [5, 3, 20, 30, 2],
            'Destino': ['Venda', 'Venda', 'Uso Interno', 'Venda', 'Venda'],
            'Cliente': ['Cliente A', 'Cliente B', 'Interno', 'Cliente C', 'Cliente D'],
            'Responsável': ['João', 'Maria', 'Carlos', 'Ana', 'João']
        })
        
        st.dataframe(historico_saidas, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("Fornecedores Cadastrados")
        
        fornecedores = pd.DataFrame({
            'Código': ['F001', 'F002', 'F003', 'F004', 'F005'],
            'Nome': ['Fornecedor A', 'Fornecedor B', 'Fornecedor C', 'Fornecedor D', 'Fornecedor E'],
            'CNPJ': ['12.345.678/0001-90', '23.456.789/0001-01', '34.567.890/0001-12', '45.678.901/0001-23', '56.789.012/0001-34'],
            'Telefone': ['(11) 3333-4444', '(11) 4444-5555', '(11) 5555-6666', '(11) 6666-7777', '(11) 7777-8888'],
            'Email': ['contato@fora.com', 'vendas@forb.com', 'comercial@forc.com', 'atendimento@ford.com', 'suporte@fore.com'],
            'Categoria': ['Eletrônicos', 'Móveis', 'Papelaria', 'Eletrônicos', 'Diversos']
        })
        
        st.dataframe(fornecedores, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Adicionar Fornecedor")
            with st.form("novo_fornecedor"):
                nome_forn = st.text_input("Nome do Fornecedor")
                cnpj = st.text_input("CNPJ")
                telefone = st.text_input("Telefone")
                email = st.text_input("E-mail")
                categoria_forn = st.selectbox("Categoria", ["Eletrônicos", "Móveis", "Papelaria", "Alimentos", "Diversos"])
                
                if st.form_submit_button("➕ Adicionar"):
                    st.success(f"Fornecedor {nome_forn} cadastrado com sucesso!")
        
        with col2:
            st.subheader("Avaliação de Fornecedores")
            avaliacoes = pd.DataFrame({
                'Fornecedor': ['Fornecedor A', 'Fornecedor B', 'Fornecedor C', 'Fornecedor D'],
                'Prazo Entrega': [4.5, 4.0, 3.5, 5.0],
                'Qualidade': [4.0, 4.5, 4.0, 4.5],
                'Preço': [3.5, 4.0, 4.5, 3.0],
                'Média': [4.0, 4.2, 4.0, 4.2]
            })
            
            st.dataframe(avaliacoes, use_container_width=True, hide_index=True)