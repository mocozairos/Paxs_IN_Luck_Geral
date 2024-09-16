import pandas as pd
import mysql.connector
import decimal
import streamlit as st

def gerar_df_phoenix(vw_name, base):
    # Parametros de Login AWS

    nome_base = f'test_phoenix_{base}'

    config = {
    'user': 'user_automation_jpa',
    'password': 'luck_jpa_2024',
    'host': 'comeia.cixat7j68g0n.us-east-1.rds.amazonaws.com',
    'database': nome_base
    }
    # Conexão as Views
    conexao = mysql.connector.connect(**config)
    cursor = conexao.cursor()

    request_name = f'SELECT * FROM {vw_name}'

    # Script MySql para requests
    cursor.execute(
        request_name
    )
    # Coloca o request em uma variavel
    resultado = cursor.fetchall()
    # Busca apenas o cabecalhos do Banco
    cabecalho = [desc[0] for desc in cursor.description]

    # Fecha a conexão
    cursor.close()
    conexao.close()

    # Coloca em um dataframe e muda o tipo de decimal para float
    df = pd.DataFrame(resultado, columns=cabecalho)
    df = df.applymap(lambda x: float(x) if isinstance(x, decimal.Decimal) else x)
    return df

st.set_page_config(layout='wide')

if 'mapa_router_jp' not in st.session_state:

    st.session_state.mapa_router_jp = gerar_df_phoenix('vw_router', 'joao_pessoa')

    st.session_state.mapa_router_rec = gerar_df_phoenix('vw_router', 'recife')

    st.session_state.mapa_router_nat = gerar_df_phoenix('vw_router', 'natal')

    st.session_state.mapa_router_mcz = gerar_df_phoenix('vw_router', 'maceio')

    # st.session_state.mapa_router_ssa = gerar_df_phoenix('vw_router', 'salvador')

    # st.session_state.mapa_router_nor = gerar_df_phoenix('vw_router', 'noronha')

    # st.session_state.mapa_router_ara = gerar_df_phoenix('vw_router', 'aracaju')

st.title('Paxs IN - Luck Geral')

st.divider()

row0 = st.columns(2)

with row0[0]:

    data_inicial = st.date_input('Data Inicial', value=None ,format='DD/MM/YYYY', key='data_inicial')

    data_final = st.date_input('Data Final', value=None ,format='DD/MM/YYYY', key='data_final')

    base_luck = st.radio('Base Luck', ['João Pessoa', 'Natal', 'Recife', 'Maceió', 'Todas'], index=None)

with row0[1]:

    container_dados = st.container()

    atualizar_dados = container_dados.button('Carregar Dados do Phoenix', use_container_width=True)

if atualizar_dados:

    st.session_state.mapa_router_jp = gerar_df_phoenix('vw_router', 'joao_pessoa')

    st.session_state.mapa_router_rec = gerar_df_phoenix('vw_router', 'recife')

    st.session_state.mapa_router_nat = gerar_df_phoenix('vw_router', 'natal')

    st.session_state.mapa_router_mcz = gerar_df_phoenix('vw_router', 'maceio')

    # st.session_state.mapa_router_ssa = gerar_df_phoenix('vw_router', 'salvador')

    # st.session_state.mapa_router_nor = gerar_df_phoenix('vw_router', 'noronha')

    # st.session_state.mapa_router_ara = gerar_df_phoenix('vw_router', 'aracaju')

st.divider()

if data_inicial and data_final and base_luck!='Todas' and base_luck:

    if base_luck=='João Pessoa':

        df_mapa_ref = st.session_state.mapa_router_jp

    elif base_luck=='Recife':

        df_mapa_ref = st.session_state.mapa_router_rec

    elif base_luck=='Natal':

        df_mapa_ref = st.session_state.mapa_router_nat

    elif base_luck=='Maceió':

        df_mapa_ref = st.session_state.mapa_router_mcz

    # elif base_luck=='Salvador':

    #     df_mapa_ref = st.session_state.mapa_router_ssa

    # elif base_luck=='Aracajú':

    #     df_mapa_ref = st.session_state.mapa_router_ara

    df_mapa_filtrado = df_mapa_ref[(df_mapa_ref['Data Execucao'] >= data_inicial) & (df_mapa_ref['Data Execucao'] <= data_final) & 
                                   (df_mapa_ref['Tipo de Servico']=='IN') & (df_mapa_ref['Status do Servico']!='CANCELADO') & 
                                   (df_mapa_ref['Status do Servico']!='RASCUNHO')].reset_index(drop=True)
    
    df_mapa_filtrado['Paxs Totais'] = df_mapa_filtrado['Total ADT'] + df_mapa_filtrado['Total CHD']

    adt_in = int(df_mapa_filtrado['Total ADT'].sum())

    chd_in = int(df_mapa_filtrado['Total CHD'].sum())

    chd_in_metade = int(chd_in/2)

    st.success(f'No período selecionado existem {adt_in + chd_in} passageiros.')

    df_mapa_filtrado_group = df_mapa_filtrado.groupby('Servico')['Paxs Totais'].sum().reset_index()

    st.dataframe(df_mapa_filtrado_group.sort_values(by='Paxs Totais', ascending=False), hide_index=True)



elif data_inicial and data_final and base_luck=='Todas':

    mapa_router_jp = st.session_state.mapa_router_jp

    mapa_router_jp['Base Luck'] = 'JPA'

    mapa_router_rec = st.session_state.mapa_router_rec

    mapa_router_rec['Base Luck'] = 'REC'

    mapa_router_nat = st.session_state.mapa_router_nat

    mapa_router_nat['Base Luck'] = 'NAT'

    mapa_router_mcz = st.session_state.mapa_router_mcz

    mapa_router_mcz['Base Luck'] = 'MCZ'

    mapa_router_geral = pd.concat([mapa_router_jp, mapa_router_rec, mapa_router_nat, mapa_router_mcz], ignore_index=True)

    mapa_router_geral_filtrado = mapa_router_geral[(mapa_router_geral['Data Execucao'] >= data_inicial) & 
                                                   (mapa_router_geral['Data Execucao'] <= data_final) & 
                                                   (mapa_router_geral['Tipo de Servico']=='IN') & 
                                                   (mapa_router_geral['Status do Servico']!='CANCELADO') & 
                                                   (mapa_router_geral['Status do Servico']!='RASCUNHO')].reset_index(drop=True)
    
    mapa_router_geral_filtrado['Paxs Totais'] = mapa_router_geral_filtrado['Total ADT'] + mapa_router_geral_filtrado['Total CHD']

    df_mapa_filtrado_group = mapa_router_geral_filtrado.groupby('Base Luck')['Paxs Totais'].sum().reset_index()

    st.dataframe(df_mapa_filtrado_group.sort_values(by='Paxs Totais', ascending=False), hide_index=True)





