import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def render():
    st.markdown("""
        <style>
        .relatorios-header {
            background: linear-gradient(90deg, #E74C3C 0%, #EC7063 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }
        .relatorios-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            border-left: 4px solid #E74C3C;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="relatorios-header">
            <h1>📈 Sistema de Relatórios</h1>
            <p>Relatórios gerenciais e indicadores de desempenho</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs por tipo de relatório
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Relatórios Gerenciais", "📋 Relatórios Operacionais", "📈 Indicadores", "📁 Exportar Dados"])
    
    with tab1:
        st.subheader("Relatórios Gerenciais")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            tipo_rel = st.selectbox(
                "Tipo de Relatório",
                ["Vendas por Período", "Desempenho Financeiro", "Produtividade RH", "Giro de Estoque", "Satisfação Clientes"]
            )
            
            periodo = st.selectbox(
                "Período",
                ["Hoje", "Esta Semana", "Este Mês", "Este Trimestre", "Este Ano", "Personalizado"]
            )
            
            if periodo == "Personalizado":
                data_ini = st.date_input("Data Inicial")
                data_fim = st.date_input("Data Final")
            
            formato = st.radio("Formato", ["Visualizar", "PDF", "Excel"])
        
        with col2:
            st.markdown("### Pré-visualização do Relatório")
            
            if tipo_rel == "Vendas por Período":
                # Gráfico de vendas
                datas = [(datetime.now() - timedelta(days=i)).strftime('%d/%m') for i in range(30, 0, -1)]
                vendas = [random.randint(1000, 5000) for _ in range(30)]
                
                fig = px.line(x=datas, y=vendas, title='Vendas Diárias - Últimos 30 Dias')
                fig.update_layout(xaxis_title='Data', yaxis_title='Valor (R$)')
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabela resumo
                dados_vendas = pd.DataFrame({
                    'Métrica': ['Total Vendas', 'Média Diária', 'Maior Venda', 'Menor Venda'],
                    'Valor': [f'R$ {sum(vendas):,.2f}', f'R$ {sum(vendas)/30:,.2f}', 
                             f'R$ {max(vendas):,.2f}', f'R$ {min(vendas):,.2f}']
                })
                st.dataframe(dados_vendas, use_container_width=True, hide_index=True)
            
            elif tipo_rel == "Desempenho Financeiro":
                # Gráfico de DRE
                categorias = ['Receita', 'Custos', 'Despesas', 'Lucro Bruto', 'Lucro Líquido']
                valores = [100000, 35000, 25000, 40000, 25000]
                
                fig = go.Figure(data=[
                    go.Bar(name='Valores', x=categorias, y=valores, marker_color=['green', 'red', 'red', 'blue', 'purple'])
                ])
                fig.update_layout(title='Demonstrativo de Resultados')
                st.plotly_chart(fig, use_container_width=True)
            
            elif tipo_rel == "Produtividade RH":
                # Gráfico de funcionários
                meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai']
                contratacoes = [3, 5, 2, 4, 3]
                desligamentos = [1, 2, 3, 1, 2]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=meses, y=contratacoes, mode='lines+markers', name='Contratações'))
                fig.add_trace(go.Scatter(x=meses, y=desligamentos, mode='lines+markers', name='Desligamentos'))
                fig.update_layout(title='Movimentação de Pessoal')
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Relatórios Operacionais")
        
        tipo_op = st.selectbox(
            "Selecione o Relatório Operacional",
            ["Agendamentos do Dia", "Vendas do Dia", "Estoque Crítico", "Ponto Eletrônico", "Contas a Pagar/Receber"]
        )
        
        if tipo_op == "Agendamentos do Dia":
            st.write("**Agendamentos para hoje**")
            agendamentos_dia = pd.DataFrame({
                'Horário': ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00'],
                'Cliente': ['João', 'Maria', 'Carlos', 'Ana', 'Pedro', 'Lucia'],
                'Serviço': ['Corte', 'Manicure', 'Barba', 'Coloração', 'Corte', 'Pedicure'],
                'Profissional': ['Carlos', 'Ana', 'João', 'Maria', 'Pedro', 'Ana'],
                'Status': ['Confirmado', 'Confirmado', 'Em espera', 'Confirmado', 'Confirmado', 'Confirmado']
            })
            st.dataframe(agendamentos_dia, use_container_width=True, hide_index=True)
        
        elif tipo_op == "Vendas do Dia":
            vendas_dia = pd.DataFrame({
                'Hora': ['09:30', '10:15', '11:45', '14:20', '15:30', '16:45'],
                'Cliente': ['Cliente A', 'Cliente B', 'Cliente C', 'Cliente D', 'Cliente E', 'Cliente F'],
                'Produto': ['Produto X', 'Serviço Y', 'Produto Z', 'Serviço W', 'Produto K', 'Serviço L'],
                'Valor': ['R$ 150,00', 'R$ 200,00', 'R$ 89,90', 'R$ 350,00', 'R$ 75,50', 'R$ 180,00'],
                'Pagamento': ['Cartão', 'PIX', 'Dinheiro', 'Cartão', 'PIX', 'Cartão']
            })
            st.dataframe(vendas_dia, use_container_width=True, hide_index=True)
            
            total_dia = 150 + 200 + 89.9 + 350 + 75.5 + 180
            st.metric("Total do Dia", f"R$ {total_dia:.2f}")
        
        elif tipo_op == "Estoque Crítico":
            estoque_critico = pd.DataFrame({
                'Produto': ['Item A', 'Item B', 'Item C', 'Item D', 'Item E'],
                'Categoria': ['Eletrônicos', 'Móveis', 'Papelaria', 'Vestuário', 'Alimentos'],
                'Atual': [5, 3, 2, 4, 1],
                'Mínimo': [10, 5, 5, 8, 5],
                'Status': ['Crítico', 'Crítico', 'Crítico', 'Atenção', 'Crítico']
            })
            st.dataframe(estoque_critico, use_container_width=True, hide_index=True)
            
            st.warning("⚠️ 5 produtos precisam de reposição urgente!")
    
    with tab3:
        st.subheader("Indicadores de Desempenho (KPIs)")
        
        # KPIs gerais
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Faturamento Mensal", "R$ 78.450", "+12%")
            st.metric("Ticket Médio", "R$ 94,50", "+R$ 5,20")
            st.metric("Conversão", "68%", "+3%")
        
        with col2:
            st.metric("Satisfação Clientes", "4.5/5", "+0.3")
            st.metric("Produtividade", "92%", "+2%")
            st.metric("Giro de Estoque", "6.2x", "+0.5x")
        
        with col3:
            st.metric("Absenteísmo", "3.2%", "-0.4%")
            st.metric("ROI", "18.5%", "+2.1%")
            st.metric("Margem Líquida", "22.3%", "+1.2%")
        
        # Gráfico de performance
        st.subheader("Evolução dos Indicadores")
        
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
        indicadores = pd.DataFrame({
            'Mês': meses,
            'Faturamento': [65000, 68000, 72000, 75000, 78450, 82000],
            'Clientes': [580, 620, 680, 720, 780, 820],
            'Satisfação': [4.1, 4.2, 4.3, 4.4, 4.5, 4.6]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=indicadores['Faturamento'], mode='lines+markers', name='Faturamento (R$)', yaxis='y'))
        fig.add_trace(go.Scatter(x=meses, y=indicadores['Clientes'], mode='lines+markers', name='Clientes', yaxis='y2'))
        
        fig.update_layout(
            title='Evolução de Indicadores',
            yaxis=dict(title='Faturamento (R$)', side='left'),
            yaxis2=dict(title='Clientes', overlaying='y', side='right')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela comparativa
        st.subheader("Comparativo Mensal")
        comparativo = pd.DataFrame({
            'Indicador': ['Faturamento', 'Clientes Atendidos', 'Ticket Médio', 'Satisfação', 'Produtividade'],
            'Mês Atual': ['R$ 78.450', '780', 'R$ 94,50', '4.5', '92%'],
            'Mês Anterior': ['R$ 72.000', '720', 'R$ 89,20', '4.3', '90%'],
            'Variação': ['+9%', '+8.3%', '+5.9%', '+4.7%', '+2.2%']
        })
        st.dataframe(comparativo, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("Exportar Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Selecione os dados para exportar**")
            
            modulo = st.selectbox(
                "Módulo",
                ["Todos", "Agendamento", "Vendas", "Financeiro", "RH", "Estoque"]
            )
            
            periodo_export = st.selectbox(
                "Período",
                ["Hoje", "Esta Semana", "Este Mês", "Este Trimestre", "Este Ano", "Todo Histórico"]
            )
            
            formato_export = st.selectbox(
                "Formato",
                ["CSV", "Excel", "JSON", "PDF"]
            )
            
            incluir_graficos = st.checkbox("Incluir gráficos", value=True)
            incluir_resumo = st.checkbox("Incluir resumo estatístico", value=True)
        
        with col2:
            st.write("**Resumo da exportação**")
            st.info(f"""
            **Módulo:** {modulo}
            **Período:** {periodo_export}
            **Formato:** {formato_export}
            **Registros estimados:** {random.randint(100, 1000)}
            **Tamanho estimado:** {random.randint(1, 10)} MB
            """)
            
            if st.button("📥 Gerar e Exportar", type="primary", use_container_width=True):
                with st.spinner("Gerando relatório..."):
                    # Simular processamento
                    import time
                    time.sleep(3)
                    
                    st.success("Relatório gerado com sucesso!")
                    
                    # Botão de download simulado
                    st.download_button(
                        label="📥 Clique para baixar",
                        data="Dados simulados".encode(),
                        file_name=f"relatorio_{modulo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{formato_export.lower()}",
                        mime="text/plain"
                    )
            
            # Exportações recentes
            st.write("**Exportações recentes**")
            export_recentes = pd.DataFrame({
                'Data': ['10/05 14:30', '10/05 10:15', '09/05 16:45', '09/05 11:20'],
                'Módulo': ['Vendas', 'RH', 'Estoque', 'Financeiro'],
                'Formato': ['Excel', 'PDF', 'CSV', 'Excel'],
                'Status': ['✅ Concluído', '✅ Concluído', '✅ Concluído', '✅ Concluído']
            })
            st.dataframe(export_recentes, use_container_width=True, hide_index=True)