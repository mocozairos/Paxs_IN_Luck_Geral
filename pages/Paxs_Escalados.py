import pandas as pd
import mysql.connector
import decimal
import streamlit as st
import matplotlib.pyplot as plt

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

def puxar_dfs_base_phoenix():

    with st.spinner('Aguarde enquanto os dados do phoenix estão sendo puxados...'):

        st.session_state.escalas_jp = gerar_df_phoenix('vw_payment_guide', 'joao_pessoa')

        st.session_state.escalas_rec = gerar_df_phoenix('vw_payment_guide', 'recife')

        st.session_state.escalas_nat = gerar_df_phoenix('vw_payment_guide', 'natal')

        st.session_state.escalas_mcz = gerar_df_phoenix('vw_payment_guide', 'maceio')

        st.session_state.escalas_ssa = gerar_df_phoenix('vw_payment_guide', 'salvador')

        st.session_state.escalas_nor = gerar_df_phoenix('vw_payment_guide', 'noronha')

        # st.session_state.escalas_ara = gerar_df_phoenix('vw_router', 'aracaju')

    st.success('Dados baixados com sucesso!')

def tratar_dfs_base_phoenix():

    lista_dfs_phoenix = ['escalas_jp', 'escalas_rec', 'escalas_nat', 'escalas_mcz', 'escalas_ssa', 'escalas_nor']

    for df in lista_dfs_phoenix:

        st.session_state[df] = st.session_state[df][(st.session_state[df]['Status do Servico']!='CANCELADO') & 
                                                    (~pd.isna(st.session_state[df]['Escala']))].reset_index(drop=True)

def criar_coluna_base_luck():

    lista_dfs_phoenix = ['escalas_jp', 'escalas_rec', 'escalas_nat', 'escalas_mcz', 'escalas_ssa', 'escalas_nor']

    for df in lista_dfs_phoenix:

        st.session_state[df]['Base Luck'] = st.session_state[df]['Reserva'].str[:3]

def criar_df_geral():

    df_geral = pd.concat([st.session_state.escalas_jp, st.session_state.escalas_rec, st.session_state.escalas_nat, 
                          st.session_state.escalas_mcz, st.session_state.escalas_ssa, st.session_state.escalas_nor])
    
    return df_geral

st.set_page_config(layout='wide')

if 'escalas_nor' not in st.session_state:

    puxar_dfs_base_phoenix()

    tratar_dfs_base_phoenix()

    criar_coluna_base_luck()

st.title('Paxs Escalados - Luck Geral')

st.divider()

dict_bases = {'João Pessoa': 'JPA', 'Natal': 'NAT', 'Recife': 'REC', 'Maceió': 'MCZ', 'Salvador': 'SSA', 'Noronha': 'FEN'}

row0 = st.columns(2)

with row0[0]:

    data_inicial = st.date_input('Data Inicial', value=None ,format='DD/MM/YYYY', key='data_inicial')

    data_final = st.date_input('Data Final', value=None ,format='DD/MM/YYYY', key='data_final')

    base_luck = st.selectbox('Base Luck', ['João Pessoa', 'Natal', 'Recife', 'Maceió', 'Salvador', 'Noronha', 'Todas'], index=None)

with row0[1]:

    container_dados = st.container()

    atualizar_dados = container_dados.button('Carregar Dados do Phoenix', use_container_width=True)

    row0_1 = st.columns(2)

    with row0_1[0]:

        tipo_analise = st.radio('Análise', ['Paxs Escalados'], index=None)

if atualizar_dados:

    puxar_dfs_base_phoenix()

    tratar_dfs_base_phoenix()

    criar_coluna_base_luck()

criar_coluna_base_luck()

if tipo_analise=='Paxs Escalados' and data_inicial and data_final and base_luck=='Todas':

    df_geral = criar_df_geral()

    df_geral_filtrado = df_geral[(df_geral['Data Execucao'] >= data_inicial) & (df_geral['Data Execucao'] <= data_final)]\
        .reset_index(drop=True)
    
    df_geral_filtrado['Paxs Escalados'] = df_geral_filtrado['Total ADT'] + df_geral_filtrado['Total CHD']
    
    df_escalas_base = df_geral_filtrado.groupby(['Base Luck'])['Paxs Escalados'].sum().reset_index()\
        .sort_values(by='Paxs Escalados', ascending = False)

    with row0[0]:

        container_df = st.container()

        container_df.dataframe(df_escalas_base, hide_index=True, use_container_width=True)

elif tipo_analise=='Paxs Escalados' and data_inicial and data_final and base_luck!='Todas':

    codigo_base = dict_bases[base_luck]

    df_geral = criar_df_geral()

    df_geral_filtrado = df_geral[(df_geral['Data Execucao'] >= data_inicial) & (df_geral['Data Execucao'] <= data_final) & 
                                 (df_geral['Base Luck'] == codigo_base)].reset_index(drop=True)
    
    df_geral_filtrado['Paxs Escalados'] = df_geral_filtrado['Total ADT'] + df_geral_filtrado['Total CHD']
    
    df_escalas_base = df_geral_filtrado.groupby(['Base Luck'])['Paxs Escalados'].sum().reset_index()\
        .sort_values(by='Paxs Escalados', ascending = False)

    with row0[0]:

        container_df = st.container()

        container_df.dataframe(df_escalas_base, hide_index=True, use_container_width=True)

    
