import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def render():
    st.markdown("""
        <style>
        .financeiro-header {
            background: linear-gradient(90deg, #FFA500 0%, #FFB52E 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }
        .financeiro-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            border-left: 4px solid #FFA500;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="financeiro-header">
            <h1>📊 Sistema Financeiro</h1>
            <p>Gestão completa do fluxo de caixa</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Saldo atual em destaque
    saldo_atual = 15780.50
    st.markdown(f"""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 30px;'>
            <h2 style='color: white; margin: 0;'>Saldo Atual</h2>
            <h1 style='color: white; font-size: 3em; margin: 10px 0;'>R$ {saldo_atual:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Entradas (Mês)", f"R$ {random.randint(25000, 35000):,.2f}", f"+{random.randint(5, 10)}%")
    with col2:
        st.metric("Saídas (Mês)", f"R$ {random.randint(18000, 25000):,.2f}", f"+{random.randint(3, 7)}%")
    with col3:
        st.metric("Lucro Líquido", f"R$ {random.randint(7000, 10000):,.2f}", f"+{random.randint(8, 15)}%")
    with col4:
        st.metric("Margem", f"{random.randint(25, 35)}%", f"+{random.randint(1, 3)}%")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Fluxo de Caixa", "💰 Contas a Pagar", "💳 Contas a Receber", "📑 Relatórios"])
    
    with tab1:
        st.subheader("Fluxo de Caixa - Últimos 30 Dias")
        
        # Dados simulados
        datas = [(datetime.now() - timedelta(days=i)).strftime('%d/%m') for i in range(30, 0, -1)]
        entradas = [random.randint(800, 2000) for _ in range(30)]
        saidas = [random.randint(600, 1500) for _ in range(30)]
        saldo = [entradas[i] - saidas[i] for i in range(30)]
        
        df_fluxo = pd.DataFrame({
            'Data': datas,
            'Entradas': entradas,
            'Saídas': saidas,
            'Saldo': saldo
        })
        
        # Gráfico de linha
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=datas, y=entradas, mode='lines+markers', name='Entradas', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=datas, y=saidas, mode='lines+markers', name='Saídas', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=datas, y=saldo, mode='lines+markers', name='Saldo', line=dict(color='blue')))
        
        fig.update_layout(title='Evolução do Fluxo de Caixa', xaxis_title='Data', yaxis_title='Valor (R$)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de movimentações
        st.subheader("Últimas Movimentações")
        
        movimentacoes = pd.DataFrame({
            'Data': [(datetime.now() - timedelta(days=i)).strftime('%d/%m/%Y') for i in range(10)],
            'Descrição': [f'Movimentação {i+1}' for i in range(10)],
            'Categoria': ['Venda', 'Compra', 'Pagamento', 'Recebimento', 'Despesa', 'Venda', 'Compra', 'Pagamento', 'Recebimento', 'Despesa'][:10],
            'Tipo': ['Entrada', 'Saída', 'Saída', 'Entrada', 'Saída', 'Entrada', 'Saída', 'Saída', 'Entrada', 'Saída'][:10],
            'Valor': [random.randint(100, 2000) for _ in range(10)]
        })
        
        # Colorir tipo
        def color_tipo(val):
            if val == 'Entrada':
                return 'background-color: #90EE90'
            elif val == 'Saída':
                return 'background-color: #FFB6C1'
            return ''
        
        styled_mov = movimentacoes.style.applymap(color_tipo, subset=['Tipo'])
        st.dataframe(styled_mov, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Contas a Pagar")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Lista de contas a pagar
            contas_pagar = pd.DataFrame({
                'Vencimento': ['15/05/2024', '18/05/2024', '20/05/2024', '22/05/2024', '25/05/2024'],
                'Fornecedor': ['Fornecedor A', 'Fornecedor B', 'Fornecedor C', 'Fornecedor D', 'Fornecedor E'],
                'Descrição': ['Compra de Material', 'Serviço de Manutenção', 'Aluguel', 'Energia Elétrica', 'Água'],
                'Valor': ['R$ 1.500,00', 'R$ 850,00', 'R$ 3.000,00', 'R$ 450,00', 'R$ 320,00'],
                'Status': ['A vencer', 'A vencer', 'Vencido', 'A vencer', 'A vencer']
            })
            
            # Colorir status
            def color_status(val):
                if val == 'Vencido':
                    return 'background-color: #FFB6C1'
                elif val == 'A vencer':
                    return 'background-color: #90EE90'
                return ''
            
            styled_contas = contas_pagar.style.applymap(color_status, subset=['Status'])
            st.dataframe(styled_contas, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("Total a Pagar")
            total_pagar = 6120.00
            st.markdown(f"""
                <div style='background-color: #FFB6C1; padding: 20px; border-radius: 10px; text-align: center;'>
                    <h2 style='margin: 0;'>R$ {total_pagar:,.2f}</h2>
                    <p>Vencidos: R$ 450,00</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Registrar Nova Conta")
            with st.form("nova_conta_pagar"):
                fornecedor = st.text_input("Fornecedor")
                descricao = st.text_input("Descrição")
                valor = st.number_input("Valor", min_value=0.01, format="%.2f")
                vencimento = st.date_input("Vencimento")
                
                if st.form_submit_button("Adicionar Conta"):
                    st.success("Conta registrada com sucesso!")
    
    with tab3:
        st.subheader("Contas a Receber")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            contas_receber = pd.DataFrame({
                'Vencimento': ['15/05/2024', '18/05/2024', '20/05/2024', '22/05/2024', '25/05/2024'],
                'Cliente': ['Cliente A', 'Cliente B', 'Cliente C', 'Cliente D', 'Cliente E'],
                'Descrição': ['Venda de Produtos', 'Serviço Prestado', 'Consultoria', 'Mensalidade', 'Comissão'],
                'Valor': ['R$ 2.500,00', 'R$ 1.200,00', 'R$ 3.500,00', 'R$ 800,00', 'R$ 450,00'],
                'Status': ['A receber', 'A receber', 'Recebido', 'A receber', 'Atrasado']
            })
            
            def color_status_rec(val):
                if val == 'Atrasado':
                    return 'background-color: #FFB6C1'
                elif val == 'Recebido':
                    return 'background-color: #90EE90'
                elif val == 'A receber':
                    return 'background-color: #FFE4B5'
                return ''
            
            styled_rec = contas_receber.style.applymap(color_status_rec, subset=['Status'])
            st.dataframe(styled_rec, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("Total a Receber")
            total_receber = 8450.00
            st.markdown(f"""
                <div style='background-color: #90EE90; padding: 20px; border-radius: 10px; text-align: center;'>
                    <h2 style='margin: 0;'>R$ {total_receber:,.2f}</h2>
                    <p>Atrasados: R$ 450,00</p>
                </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.subheader("Relatórios Financeiros")
        
        tipo_rel = st.selectbox(
            "Tipo de Relatório",
            ["Demonstrativo de Resultados", "Fluxo de Caixa", "DRE", "Balanço Patrimonial", "Indicadores"]
        )
        
        periodo_rel = st.selectbox(
            "Período",
            ["Mês Atual", "Mês Anterior", "Trimestre", "Semestre", "Ano", "Personalizado"]
        )
        
        if periodo_rel == "Personalizado":
            col1, col2 = st.columns(2)
            with col1:
                data_ini = st.date_input("Data Inicial")
            with col2:
                data_fim = st.date_input("Data Final")
        
        if st.button("📊 Gerar Relatório", use_container_width=True):
            st.success("Relatório gerado com sucesso!")
            
            # Exemplo de DRE
            if tipo_rel == "Demonstrativo de Resultados":
                dados_dre = pd.DataFrame({
                    'Descrição': ['Receita Bruta', '(-) Impostos', 'Receita Líquida', '(-) Custos', 'Lucro Bruto', 
                                 '(-) Despesas', 'Lucro Operacional', '(-) IR/CSLL', 'Lucro Líquido'],
                    'Valor (R$)': ['100.000,00', '(15.000,00)', '85.000,00', '(35.000,00)', '50.000,00',
                                 '(20.000,00)', '30.000,00', '(7.500,00)', '22.500,00'],
                    '%': ['100%', '15%', '85%', '35%', '50%', '20%', '30%', '7,5%', '22,5%']
                })
                
                st.dataframe(dados_dre, use_container_width=True, hide_index=True)