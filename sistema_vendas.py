import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

def render():
    st.markdown("""
        <style>
        .vendas-header {
            background: linear-gradient(90deg, #00CC96 0%, #00E6A8 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }
        .vendas-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            border-left: 4px solid #00CC96;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="vendas-header">
            <h1>💰 Sistema de Vendas</h1>
            <p>Controle completo de vendas e faturamento</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Vendas Hoje",
            value=f"R$ {random.randint(1500, 3000):,.2f}",
            delta=f"+{random.randint(5, 15)}%"
        )
    with col2:
        st.metric(
            label="Vendas Mês",
            value=f"R$ {random.randint(45000, 60000):,.2f}",
            delta=f"+{random.randint(8, 12)}%"
        )
    with col3:
        st.metric(
            label="Ticket Médio",
            value=f"R$ {random.randint(80, 120):,.2f}",
            delta=f"+R$ {random.randint(5, 15)}"
        )
    with col4:
        st.metric(
            label="Meta Mensal",
            value="78%",
            delta="+5%"
        )
    
    # Tabs para diferentes funcionalidades
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🛒 Nova Venda", "📦 Produtos", "📈 Relatórios"])
    
    with tab1:
        st.subheader("Visão Geral de Vendas")
        
        # Gráfico de vendas
        dias = list(range(1, 31))
        vendas_diarias = [random.randint(800, 2500) for _ in range(30)]
        
        df_vendas = pd.DataFrame({
            'Dia': dias,
            'Vendas': vendas_diarias
        })
        
        fig = px.line(df_vendas, x='Dia', y='Vendas', title='Vendas Diárias - Últimos 30 Dias')
        st.plotly_chart(fig, use_container_width=True)
        
        # Top produtos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Produtos Mais Vendidos")
            produtos = pd.DataFrame({
                'Produto': ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E'],
                'Quantidade': [145, 132, 98, 87, 65],
                'Faturamento': ['R$ 7.250', 'R$ 6.600', 'R$ 4.900', 'R$ 4.350', 'R$ 3.250']
            })
            st.dataframe(produtos, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("Vendas por Categoria")
            categorias = pd.DataFrame({
                'Categoria': ['Eletrônicos', 'Vestuário', 'Alimentos', 'Serviços', 'Outros'],
                'Percentual': [35, 25, 20, 12, 8]
            })
            
            fig_pie = px.pie(categorias, values='Percentual', names='Categoria', title='Distribuição por Categoria')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with tab2:
        st.subheader("Registrar Nova Venda")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cliente = st.text_input("Nome do Cliente")
            produto = st.selectbox(
                "Produto/Serviço",
                ["Produto A - R$ 50,00", "Produto B - R$ 75,00", "Produto C - R$ 120,00", 
                 "Serviço X - R$ 200,00", "Serviço Y - R$ 150,00"]
            )
            quantidade = st.number_input("Quantidade", min_value=1, value=1)
        
        with col2:
            forma_pagamento = st.selectbox(
                "Forma de Pagamento",
                ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX", "Boleto"]
            )
            
            parcelas = 1
            if forma_pagamento == "Cartão de Crédito":
                parcelas = st.selectbox("Parcelas", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
            
            observacoes = st.text_area("Observações")
        
        # Calcular valor
        precos = [50, 75, 120, 200, 150]
        idx = ["Produto A - R$ 50,00", "Produto B - R$ 75,00", "Produto C - R$ 120,00", 
               "Serviço X - R$ 200,00", "Serviço Y - R$ 150,00"].index(produto)
        valor_total = precos[idx] * quantidade
        
        st.info(f"**Valor Total: R$ {valor_total:.2f}**")
        
        if st.button("✅ Finalizar Venda", type="primary", use_container_width=True):
            st.success(f"Venda finalizada com sucesso! Total: R$ {valor_total:.2f}")
            st.balloons()
    
    with tab3:
        st.subheader("Catálogo de Produtos")
        
        # Tabela de produtos
        produtos_catalogo = pd.DataFrame({
            'Código': ['P001', 'P002', 'P003', 'P004', 'P005'],
            'Produto': ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E'],
            'Categoria': ['Eletrônicos', 'Vestuário', 'Eletrônicos', 'Alimentos', 'Serviços'],
            'Preço': ['R$ 50,00', 'R$ 75,00', 'R$ 120,00', 'R$ 25,00', 'R$ 200,00'],
            'Estoque': [45, 32, 18, 67, 999]
        })
        
        st.dataframe(produtos_catalogo, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Adicionar Novo Produto")
            novo_produto = st.text_input("Nome do Produto")
            preco = st.number_input("Preço", min_value=0.0, format="%.2f")
            categoria = st.selectbox("Categoria", ["Eletrônicos", "Vestuário", "Alimentos", "Serviços", "Outros"])
            estoque_inicial = st.number_input("Estoque Inicial", min_value=0)
            
            if st.button("➕ Adicionar Produto"):
                st.success(f"Produto {novo_produto} adicionado com sucesso!")
        
        with col2:
            st.subheader("Ajustar Estoque")
            produto_ajuste = st.selectbox("Selecione o Produto", produtos_catalogo['Produto'].tolist())
            tipo_ajuste = st.radio("Tipo de Ajuste", ["Entrada", "Saída"])
            quantidade_ajuste = st.number_input("Quantidade", min_value=1)
            
            if st.button("📦 Aplicar Ajuste"):
                st.success(f"Estoque ajustado para {produto_ajuste}!")
    
    with tab4:
        st.subheader("Relatórios de Vendas")
        
        periodo = st.selectbox(
            "Período",
            ["Hoje", "Esta Semana", "Este Mês", "Este Trimestre", "Este Ano", "Personalizado"]
        )
        
        if periodo == "Personalizado":
            col1, col2 = st.columns(2)
            with col1:
                data_inicio = st.date_input("Data Início")
            with col2:
                data_fim = st.date_input("Data Fim")
        
        tipo_relatorio = st.selectbox(
            "Tipo de Relatório",
            ["Vendas por Período", "Vendas por Produto", "Vendas por Cliente", "Comissões", "Impostos"]
        )
        
        if st.button("📊 Gerar Relatório", use_container_width=True):
            st.info("Gerando relatório...")
            
            # Relatório simulado
            st.subheader("Resultado do Relatório")
            
            dados_relatorio = pd.DataFrame({
                'Data': [(datetime.now() - timedelta(days=i)).strftime('%d/%m/%Y') for i in range(10)],
                'Vendas': [random.randint(1000, 3000) for _ in range(10)],
                'Clientes': [random.randint(8, 20) for _ in range(10)],
                'Ticket Médio': [random.randint(80, 150) for _ in range(10)]
            })
            
            st.dataframe(dados_relatorio, use_container_width=True, hide_index=True)
            
            # Botão para exportar
            csv = dados_relatorio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"relatorio_vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )