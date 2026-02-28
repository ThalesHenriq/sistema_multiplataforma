import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def render():
    st.markdown("""
        <style>
        .agendamento-header {
            background: linear-gradient(90deg, #FF4B4B 0%, #FF6B6B 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }
        .agendamento-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            border-left: 4px solid #FF4B4B;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="agendamento-header">
            <h1>📅 Sistema de Agendamento</h1>
            <p>Gerencie seus agendamentos de forma eficiente</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Menu interno
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Novo Agendamento", "👥 Clientes", "📊 Agenda", "⚙️ Configurações"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Informações do Cliente")
            nome = st.text_input("Nome do Cliente *")
            telefone = st.text_input("Telefone *")
            email = st.text_input("E-mail")
            
            st.subheader("Detalhes do Serviço")
            servico = st.selectbox(
                "Serviço *",
                ["Corte de Cabelo", "Barba", "Corte + Barba", "Coloração", "Hidratação", "Manicure", "Pedicure"]
            )
            
            profissional = st.selectbox(
                "Profissional *",
                ["João", "Maria", "Carlos", "Ana", "Pedro"]
            )
        
        with col2:
            st.subheader("Data e Hora")
            data = st.date_input("Data *", min_value=datetime.now().date())
            
            # Gerar horários disponíveis
            horarios = []
            for hora in range(8, 19):
                for minuto in ['00', '30']:
                    horarios.append(f"{hora:02d}:{minuto}")
            
            hora = st.selectbox("Horário *", horarios)
            
            st.subheader("Observações")
            observacoes = st.text_area("Observações adicionais")
        
        if st.button("✅ Agendar", type="primary", use_container_width=True):
            if nome and telefone and servico and profissional and data and hora:
                st.success(f"Agendamento realizado para {nome} em {data} às {hora}!")
                st.balloons()
            else:
                st.error("Preencha todos os campos obrigatórios (*)")
    
    with tab2:
        st.subheader("Clientes Cadastrados")
        
        # Dados simulados
        clientes = pd.DataFrame({
            "Nome": ["João Silva", "Maria Santos", "Carlos Oliveira", "Ana Souza", "Pedro Lima"],
            "Telefone": ["(11) 99999-1111", "(11) 98888-2222", "(11) 97777-3333", "(11) 96666-4444", "(11) 95555-5555"],
            "E-mail": ["joao@email.com", "maria@email.com", "carlos@email.com", "ana@email.com", "pedro@email.com"],
            "Total Agendamentos": [15, 23, 8, 12, 5],
            "Última Visita": ["10/05/2024", "12/05/2024", "08/05/2024", "11/05/2024", "09/05/2024"]
        })
        
        st.dataframe(clientes, use_container_width=True, hide_index=True)
        
        # Buscar cliente
        busca = st.text_input("🔍 Buscar cliente")
        if busca:
            resultados = clientes[clientes['Nome'].str.contains(busca, case=False)]
            st.write(f"Encontrados {len(resultados)} clientes:")
            st.dataframe(resultados, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Agenda de Hoje")
        
        # Agenda simulada
        agenda_hoje = pd.DataFrame({
            "Horário": ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"],
            "Cliente": ["João Silva", "Maria Santos", "Carlos Oliveira", "Ana Souza", "Pedro Lima", "Lucia Ferreira"],
            "Serviço": ["Corte", "Manicure", "Barba", "Coloração", "Corte + Barba", "Pedicure"],
            "Profissional": ["João", "Maria", "Carlos", "Ana", "Pedro", "Maria"],
            "Status": ["Confirmado", "Confirmado", "Em espera", "Confirmado", "Cancelado", "Confirmado"]
        })
        
        # Colorir status
        def color_status(val):
            if val == "Confirmado":
                return 'background-color: #90EE90'
            elif val == "Cancelado":
                return 'background-color: #FFB6C1'
            elif val == "Em espera":
                return 'background-color: #FFE4B5'
            return ''
        
        styled_agenda = agenda_hoje.style.applymap(color_status, subset=['Status'])
        st.dataframe(styled_agenda, use_container_width=True, hide_index=True)
        
        # Estatísticas do dia
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Agendamentos", "8", "+2")
        with col2:
            st.metric("Confirmados", "6", "-1")
        with col3:
            st.metric("Concluídos", "3", "+1")
        with col4:
            st.metric("Faturamento", "R$ 850", "+R$ 120")
    
    with tab4:
        st.subheader("Configurações do Sistema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Horário de Funcionamento**")
            hora_inicio = st.time_input("Abertura", datetime.strptime("08:00", "%H:%M").time())
            hora_fim = st.time_input("Fechamento", datetime.strptime("19:00", "%H:%M").time())
            
            st.write("**Intervalo entre agendamentos**")
            intervalo = st.select_slider("Intervalo (minutos)", options=[15, 30, 45, 60], value=30)
        
        with col2:
            st.write("**Profissionais Ativos**")
            profissionais_ativos = st.multiselect(
                "Selecione",
                ["João", "Maria", "Carlos", "Ana", "Pedro"],
                default=["João", "Maria", "Carlos", "Ana", "Pedro"]
            )
            
            st.write("**Serviços Oferecidos**")
            servicos_ativos = st.multiselect(
                "Serviços",
                ["Corte de Cabelo", "Barba", "Corte + Barba", "Coloração", "Hidratação", "Manicure", "Pedicure"],
                default=["Corte de Cabelo", "Barba", "Manicure", "Pedicure"]
            )
        
        if st.button("💾 Salvar Configurações"):
            st.success("Configurações salvas com sucesso!")