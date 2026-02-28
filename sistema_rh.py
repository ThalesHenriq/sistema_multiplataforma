import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

def render():
    st.markdown("""
        <style>
        .rh-header {
            background: linear-gradient(90deg, #6C3483 0%, #8E44AD 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }
        .rh-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            border-left: 4px solid #6C3483;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="rh-header">
            <h1>👥 Sistema de RH</h1>
            <p>Gestão completa de recursos humanos</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Funcionários", "45", "+3")
    with col2:
        st.metric("Departamentos", "8", "0")
    with col3:
        st.metric("Horas Trabalhadas", "7.520", "+320")
    with col4:
        st.metric("Taxa de Absenteísmo", "3.2%", "-0.5%")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Funcionários", "📅 Ponto Eletrônico", "💰 Folha de Pagamento", "📊 Indicadores"])
    
    with tab1:
        st.subheader("Quadro de Funcionários")
        
        # Dados simulados
        funcionarios = pd.DataFrame({
            'Matrícula': ['F001', 'F002', 'F003', 'F004', 'F005'],
            'Nome': ['João Silva', 'Maria Santos', 'Carlos Oliveira', 'Ana Souza', 'Pedro Lima'],
            'Cargo': ['Analista', 'Coordenador', 'Assistente', 'Gerente', 'Analista'],
            'Departamento': ['TI', 'RH', 'Vendas', 'Financeiro', 'Marketing'],
            'Data Admissão': ['10/01/2022', '15/03/2021', '20/06/2023', '05/02/2020', '12/04/2022'],
            'Salário': ['R$ 4.500', 'R$ 6.800', 'R$ 2.800', 'R$ 9.500', 'R$ 4.200'],
            'Status': ['Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo']
        })
        
        st.dataframe(funcionarios, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Adicionar Funcionário")
            with st.form("novo_funcionario"):
                nome = st.text_input("Nome Completo")
                cargo = st.text_input("Cargo")
                departamento = st.selectbox("Departamento", ["TI", "RH", "Vendas", "Financeiro", "Marketing", "Operações"])
                salario = st.number_input("Salário", min_value=0.0, format="%.2f")
                data_admissao = st.date_input("Data de Admissão")
                
                if st.form_submit_button("➕ Adicionar"):
                    st.success(f"Funcionário {nome} adicionado com sucesso!")
        
        with col2:
            st.subheader("Departamentos")
            deptos = pd.DataFrame({
                'Departamento': ['TI', 'RH', 'Vendas', 'Financeiro', 'Marketing', 'Operações'],
                'Funcionários': [8, 5, 12, 6, 4, 10],
                'Head': ['Carlos', 'Maria', 'João', 'Ana', 'Pedro', 'Lucia']
            })
            st.dataframe(deptos, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Registro de Ponto - Hoje")
        
        # Ponto eletrônico
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        st.write(f"**Data:** {data_hoje}")
        
        # Tabela de ponto
        ponto = pd.DataFrame({
            'Funcionário': ['João Silva', 'Maria Santos', 'Carlos Oliveira', 'Ana Souza', 'Pedro Lima'],
            'Entrada': ['08:00', '08:15', '08:05', '07:55', '08:10'],
            'Saída Almoço': ['12:00', '12:15', '12:05', '12:00', '12:10'],
            'Retorno Almoço': ['13:00', '13:15', '13:05', '13:00', '13:10'],
            'Saída': ['18:00', '18:15', '18:05', '17:55', '18:10'],
            'Horas': ['9h', '9h', '9h', '9h', '9h'],
            'Status': ['Normal', 'Normal', 'Normal', 'Normal', 'Normal']
        })
        
        st.dataframe(ponto, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Registrar Ponto Manual")
            funcionario = st.selectbox("Funcionário", ponto['Funcionário'].tolist())
            tipo_registro = st.selectbox("Tipo", ["Entrada", "Saída Almoço", "Retorno Almoço", "Saída"])
            horario = st.time_input("Horário", datetime.now().time())
            
            if st.button("🕒 Registrar"):
                st.success(f"Ponto registrado para {funcionario} às {horario}")
        
        with col2:
            st.subheader("Resumo do Dia")
            st.metric("Total de Horas", "396h", "+12h")
            st.metric("Funcionários Presentes", "42", "-3")
            st.metric("Atrasos", "2", "-1")
    
    with tab3:
        st.subheader("Folha de Pagamento")
        
        # Selecionar período
        mes = st.selectbox("Mês/Ano", ["Maio/2024", "Abril/2024", "Março/2024", "Fevereiro/2024", "Janeiro/2024"])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Bruto", "R$ 187.500", "+R$ 5.200")
        with col2:
            st.metric("Total Descontos", "R$ 32.800", "+R$ 1.200")
        with col3:
            st.metric("Total Líquido", "R$ 154.700", "+R$ 4.000")
        
        # Detalhamento
        st.subheader("Detalhamento por Funcionário")
        
        detalhamento = pd.DataFrame({
            'Funcionário': ['João Silva', 'Maria Santos', 'Carlos Oliveira', 'Ana Souza', 'Pedro Lima'],
            'Salário Base': ['R$ 4.500', 'R$ 6.800', 'R$ 2.800', 'R$ 9.500', 'R$ 4.200'],
            'Horas Extras': ['R$ 450', 'R$ 0', 'R$ 280', 'R$ 0', 'R$ 210'],
            'Bonificações': ['R$ 0', 'R$ 680', 'R$ 0', 'R$ 950', 'R$ 0'],
            'INSS': ['R$ 495', 'R$ 748', 'R$ 308', 'R$ 1.045', 'R$ 462'],
            'IRRF': ['R$ 135', 'R$ 340', 'R$ 0', 'R$ 712', 'R$ 105'],
            'Líquido': ['R$ 4.320', 'R$ 6.392', 'R$ 2.772', 'R$ 8.693', 'R$ 3.843']
        })
        
        st.dataframe(detalhamento, use_container_width=True, hide_index=True)
        
        if st.button("📥 Exportar Folha", use_container_width=True):
            st.success("Folha de pagamento exportada com sucesso!")
    
    with tab4:
        st.subheader("Indicadores de RH")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por departamento
            deptos_count = pd.DataFrame({
                'Departamento': ['TI', 'RH', 'Vendas', 'Financeiro', 'Marketing', 'Operações'],
                'Quantidade': [8, 5, 12, 6, 4, 10]
            })
            
            fig_deptos = px.pie(deptos_count, values='Quantidade', names='Departamento', 
                               title='Distribuição por Departamento')
            st.plotly_chart(fig_deptos, use_container_width=True)
        
        with col2:
            # Tempo de casa
            tempo_casa = pd.DataFrame({
                'Tempo': ['< 1 ano', '1-3 anos', '3-5 anos', '5-10 anos', '> 10 anos'],
                'Quantidade': [12, 18, 8, 5, 2]
            })
            
            fig_tempo = px.bar(tempo_casa, x='Tempo', y='Quantidade', 
                              title='Tempo de Casa dos Funcionários')
            st.plotly_chart(fig_tempo, use_container_width=True)
        
        # Outros indicadores
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Turnover Mensal", "2.2%", "-0.3%")
        with col2:
            st.metric("Média Salarial", "R$ 4.850", "+R$ 150")
        with col3:
            st.metric("Satisfação", "4.2/5", "+0.2")
        
        # Aniversariantes
        st.subheader("Aniversariantes do Mês")
        aniversariantes = pd.DataFrame({
            'Funcionário': ['Ana Lima', 'Carlos Sousa', 'Mariana Silva', 'José Santos'],
            'Cargo': ['Analista', 'Coordenador', 'Assistente', 'Gerente'],
            'Data': ['15/05', '18/05', '22/05', '28/05'],
            'Departamento': ['RH', 'Vendas', 'Financeiro', 'TI']
        })
        
        st.dataframe(aniversariantes, use_container_width=True, hide_index=True)