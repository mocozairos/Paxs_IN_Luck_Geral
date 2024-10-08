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

        st.session_state.mapa_router_jp = gerar_df_phoenix('vw_router', 'joao_pessoa')

        st.session_state.mapa_router_rec = gerar_df_phoenix('vw_router', 'recife')

        st.session_state.mapa_router_nat = gerar_df_phoenix('vw_router', 'natal')

        st.session_state.mapa_router_mcz = gerar_df_phoenix('vw_router', 'maceio')

        st.session_state.mapa_router_ssa = gerar_df_phoenix('vw_router', 'salvador')

        st.session_state.mapa_router_nor = gerar_df_phoenix('vw_router', 'noronha')

        st.session_state.mapa_router_ara = gerar_df_phoenix('vw_router', 'aracaju')

    st.success('Dados baixados com sucesso!')

def gerar_dfs_base(base_luck):

    if base_luck=='João Pessoa':

        df = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck'] == 'JPA') & 
                                                (st.session_state.mapa_router_geral['Servico'] != 'FAZER CONTATO - SEM TRF IN ') & 
                                                (st.session_state.mapa_router_geral['Servico'] != 'GUIA BASE NOTURNO') & 
                                                (st.session_state.mapa_router_geral['Servico'] != 'GUIA BASE DIURNO ') & 
                                                (st.session_state.mapa_router_geral['Status do Servico'] != 'CANCELADO')].reset_index(drop=True)

        return df

    elif base_luck=='Recife':

        df = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck'] == 'REC') & 
                                                (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO') & 
                                                (st.session_state.mapa_router_geral['Status do Servico']!='RASCUNHO')].reset_index(drop=True)
    
        return df

    elif base_luck=='Natal':

        df = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck'] == 'NAT') & 
                                                (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO')].reset_index(drop=True)

        return df

    elif base_luck=='Maceió':

        df = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck']=='MCZ') & 
                                                (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO')].reset_index(drop=True)
        
        df = df[~df['Observacao'].str.upper().str.contains('CLD', na=False)]

        return df

    elif base_luck=='Salvador':

        df = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck']=='SSA') & 
                                                (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO')].reset_index(drop=True)

        return df

    elif base_luck=='Aracajú':

        df = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck']=='AJU') & 
                                                (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO')].reset_index(drop=True)

        return df

    elif base_luck=='Noronha':

        df = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck']=='FEN') & 
                                                (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO')].reset_index(drop=True)

        return df

def grafico_pizza(df, coluna_valores, coluna_labels):

    borda_preto = {'linewidth': 2, 'edgecolor': 'black'}

    fig, ax = plt.subplots(figsize=(5, 8))

    plt.pie(df[coluna_valores], labels=df[coluna_labels], autopct='%1.1f%%', startangle=90, wedgeprops=borda_preto)

    ax.set_aspect('equal')

    fig.patch.set_edgecolor('black')

    fig.patch.set_linewidth(5)

    st.pyplot(fig)
    plt.close(fig)

def grafico_seis_linhas_numero(referencia, eixo_x, eixo_y_1, ref_1_label, eixo_y_2, ref_2_label, eixo_y_3, ref_3_label, eixo_y_4, 
                                 ref_4_label, eixo_y_5, ref_5_label, eixo_y_6, ref_6_label, titulo):
    
    fig, ax = plt.subplots(figsize=(15, 8))
    
    plt.plot(referencia[eixo_x], referencia[eixo_y_1], label = ref_1_label, linewidth = 0.5, color = 'red')
    ax.plot(referencia[eixo_x], referencia[eixo_y_2], label = ref_2_label, linewidth = 0.5, color = 'blue')
    ax.plot(referencia[eixo_x], referencia[eixo_y_3], label = ref_3_label, linewidth = 0.5, color = 'black')
    ax.plot(referencia[eixo_x], referencia[eixo_y_4], label = ref_4_label, linewidth = 0.5, color = 'green')
    ax.plot(referencia[eixo_x], referencia[eixo_y_5], label = ref_5_label, linewidth = 0.5, color = 'orange')
    ax.plot(referencia[eixo_x], referencia[eixo_y_6], label = ref_6_label, linewidth = 0.5, color = 'gray')
    
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_1][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_1][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_2][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_2][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_3][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_3][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_4][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_4][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_5][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_5][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_6][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_6][i], texto, ha='center', va='bottom')

    plt.title(titulo, fontsize=30)
    plt.xlabel('Ano/Mês')
    ax.legend(loc='lower right', bbox_to_anchor=(1.2, 1))
    st.pyplot(fig)
    plt.close(fig)

def grafico_cinco_linhas_numero(referencia, eixo_x, eixo_y_1, ref_1_label, eixo_y_2, ref_2_label, eixo_y_3, ref_3_label, eixo_y_4, 
                                 ref_4_label, eixo_y_5, ref_5_label, titulo):
    
    fig, ax = plt.subplots(figsize=(15, 8))
    
    plt.plot(referencia[eixo_x], referencia[eixo_y_1], label = ref_1_label, linewidth = 0.5, color = 'red')
    ax.plot(referencia[eixo_x], referencia[eixo_y_2], label = ref_2_label, linewidth = 0.5, color = 'blue')
    ax.plot(referencia[eixo_x], referencia[eixo_y_3], label = ref_3_label, linewidth = 0.5, color = 'black')
    ax.plot(referencia[eixo_x], referencia[eixo_y_4], label = ref_4_label, linewidth = 0.5, color = 'green')
    ax.plot(referencia[eixo_x], referencia[eixo_y_5], label = ref_5_label, linewidth = 0.5, color = 'orange')
    
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_1][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_1][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_2][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_2][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_3][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_3][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_4][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_4][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_5][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_5][i], texto, ha='center', va='bottom')

    plt.title(titulo, fontsize=30)
    plt.xlabel('Ano/Mês')
    ax.legend(loc='lower right', bbox_to_anchor=(1.2, 1))
    st.pyplot(fig)
    plt.close(fig)

def grafico_quatro_linhas_percentual(referencia, eixo_x, eixo_y_1, ref_1_label, eixo_y_2, ref_2_label, eixo_y_3, ref_3_label, 
                                     eixo_y_4, ref_4_label, titulo):
    
    fig, ax = plt.subplots(figsize=(15, 8))
    
    plt.plot(referencia[eixo_x], referencia[eixo_y_1], label = ref_1_label, linewidth = 0.5, color = 'red')
    ax.plot(referencia[eixo_x], referencia[eixo_y_2], label = ref_2_label, linewidth = 0.5, color = 'blue')
    ax.plot(referencia[eixo_x], referencia[eixo_y_3], label = ref_3_label, linewidth = 0.5, color = 'black')
    ax.plot(referencia[eixo_x], referencia[eixo_y_4], label = ref_4_label, linewidth = 0.5, color = 'green')
    
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_1][i]*100)) + '%'
        plt.text(referencia[eixo_x][i], referencia[eixo_y_1][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_2][i]*100)) + '%'
        plt.text(referencia[eixo_x][i], referencia[eixo_y_2][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_3][i]*100)) + '%'
        plt.text(referencia[eixo_x][i], referencia[eixo_y_3][i], texto, ha='center', va='bottom')
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_4][i]*100)) + '%'
        plt.text(referencia[eixo_x][i], referencia[eixo_y_4][i], texto, ha='center', va='bottom')

    plt.title(titulo, fontsize=30)
    plt.xlabel('Ano/Mês')
    ax.legend(loc='lower right', bbox_to_anchor=(1.2, 1))
    st.pyplot(fig)
    plt.close(fig)

def grafico_linha_numero(referencia, eixo_x, eixo_y_1, ref_1_label, titulo):
    
    fig, ax = plt.subplots(figsize=(15, 8))
    
    plt.plot(referencia[eixo_x], referencia[eixo_y_1], label = ref_1_label, linewidth = 0.5, color = 'black')
    
    for i in range(len(referencia[eixo_x])):
        texto = str(int(referencia[eixo_y_1][i]))
        plt.text(referencia[eixo_x][i], referencia[eixo_y_1][i], texto, ha='center', va='bottom')

    plt.title(titulo, fontsize=30)
    plt.xlabel('Ano/Mês')
    ax.legend(loc='lower right', bbox_to_anchor=(1.2, 1))
    st.pyplot(fig)
    plt.close(fig)

def criar_coluna_ano_mes(df_mapa_filtrado):

    df_mapa_filtrado['Data Execucao'] = pd.to_datetime(df_mapa_filtrado['Data Execucao'])

    df_mapa_filtrado['mes'] = df_mapa_filtrado['Data Execucao'].dt.month

    df_mapa_filtrado['ano'] = df_mapa_filtrado['Data Execucao'].dt.year

    df_mapa_filtrado['Ano/Mês'] = df_mapa_filtrado['mes'].astype(str) + '/' + df_mapa_filtrado['ano'].astype(str).str[-2:]

    return df_mapa_filtrado

def gerar_mapa_router_geral():

    mapa_router_jp = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck'] == 'JPA') & 
                                                        (st.session_state.mapa_router_geral['Servico'] != 'FAZER CONTATO - SEM TRF IN ') & 
                                                        (st.session_state.mapa_router_geral['Servico'] != 'GUIA BASE NOTURNO') & 
                                                        (st.session_state.mapa_router_geral['Servico'] != 'GUIA BASE DIURNO ') & 
                                                        (st.session_state.mapa_router_geral['Status do Servico'] != 'CANCELADO')].reset_index(drop=True)

    mapa_router_jp['Base Luck'] = 'JPA'

    mapa_router_rec = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck'] == 'REC') & 
                                                         (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO') & 
                                                         (st.session_state.mapa_router_geral['Status do Servico']!='RASCUNHO')].reset_index(drop=True)

    mapa_router_rec['Base Luck'] = 'REC'

    mapa_router_nat = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck'] == 'NAT') & 
                                                         (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO')].reset_index(drop=True)

    mapa_router_nat['Base Luck'] = 'NAT'

    mapa_router_mcz = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck']=='MCZ') & 
                                                         (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO')].reset_index(drop=True)
        
    mapa_router_mcz = mapa_router_mcz[~mapa_router_mcz['Observacao'].str.upper().str.contains('CLD', na=False)]

    mapa_router_mcz['Base Luck'] = 'MCZ'

    mapa_router_ssa = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck']=='SSA') & 
                                                         (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO')].reset_index(drop=True)

    mapa_router_ssa['Base Luck'] = 'SSA'

    mapa_router_nor = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck']=='FEN') & 
                                                         (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO')]\
            .reset_index(drop=True)
    
    mapa_router_nor['Base Luck'] = 'FEN'

    mapa_router_ara = st.session_state.mapa_router_geral[(st.session_state.mapa_router_geral['Base Luck']=='AJU') & 
                                                         (st.session_state.mapa_router_geral['Status do Servico']!='CANCELADO')].reset_index(drop=True)
    
    mapa_router_ara['Base Luck'] = 'AJU'

    mapa_router_geral = pd.concat([mapa_router_jp, mapa_router_rec, mapa_router_nat, mapa_router_mcz, mapa_router_ssa, mapa_router_nor, mapa_router_ara], 
                                  ignore_index=True)
    
    return mapa_router_geral

def transformar_em_varias_colunas(df_mapa_filtrado_group, coluna_ref):

    df_mapa_filtrado_group_2 = pd.DataFrame(df_mapa_filtrado_group['Ano/Mês'].unique(), columns=['Ano/Mês'])

    for base_luck in df_mapa_filtrado_group[coluna_ref].unique().tolist():

        df_ref = df_mapa_filtrado_group[df_mapa_filtrado_group[coluna_ref]==base_luck].reset_index(drop=True)

        df_ref = df_ref.rename(columns={'Paxs Totais': base_luck})

        df_mapa_filtrado_group_2 = pd.merge(df_mapa_filtrado_group_2, df_ref[['Ano/Mês', base_luck]], on=['Ano/Mês'], how='left')

    return df_mapa_filtrado_group_2

st.set_page_config(layout='wide')

if 'mapa_router_geral' not in st.session_state:

    # puxar_dfs_base_phoenix()

    st.session_state.mapa_router_geral = gerar_df_phoenix('vw_router_geral', 'joao_pessoa')

st.title('Paxs IN - Luck Geral')

st.divider()

row0 = st.columns(2)

with row0[0]:

    data_inicial = st.date_input('Data Inicial', value=None ,format='DD/MM/YYYY', key='data_inicial')

    data_final = st.date_input('Data Final', value=None ,format='DD/MM/YYYY', key='data_final')

    base_luck = st.selectbox('Base Luck', ['João Pessoa', 'Natal', 'Recife', 'Maceió', 'Salvador', 'Noronha', 'Aracajú', 'Todas'], index=None)

with row0[1]:

    container_dados = st.container()

    atualizar_dados = container_dados.button('Carregar Dados do Phoenix', use_container_width=True)

    row0_1 = st.columns(2)

    with row0_1[0]:

        tipo_analise = st.radio('Análise', ['Paxs IN', '% Serviços'], index=None)

    if tipo_analise =='% Serviços' and base_luck=='Todas':

        with row0_1[1]:

            tipo_servico = st.radio('Tipos de Serviços', ['OUT + IN', 'TOUR + TRANSFER'])

if atualizar_dados:

    # puxar_dfs_base_phoenix()

    st.session_state.mapa_router_geral = gerar_df_phoenix('vw_router_geral', 'joao_pessoa')

st.divider()

if tipo_analise=='Paxs IN':

    if data_inicial and data_final and base_luck!='Todas' and base_luck and data_inicial.month == data_final.month:

        df_mapa_ref = gerar_dfs_base(base_luck)

        df_mapa_filtrado = df_mapa_ref[(df_mapa_ref['Data Execucao'] >= data_inicial) & (df_mapa_ref['Data Execucao'] <= data_final) & 
                                    (df_mapa_ref['Tipo de Servico']=='IN')].reset_index(drop=True)
        
        df_mapa_filtrado['Paxs Totais'] = df_mapa_filtrado['Total ADT'] + df_mapa_filtrado['Total CHD']

        paxs_in = int(df_mapa_filtrado['Paxs Totais'].sum())

        st.success(f'No período selecionado existem {paxs_in} passageiros.')

        row2 = st.columns(2)

        with row2[0]:

            df_mapa_filtrado_group = df_mapa_filtrado.groupby('Servico')['Paxs Totais'].sum().reset_index()

            st.dataframe(df_mapa_filtrado_group.sort_values(by='Paxs Totais', ascending=False), hide_index=True)

        with row2[1]:

            df_mapa_filtrado_group_parceiro = df_mapa_filtrado.groupby('Parceiro')['Paxs Totais'].sum().reset_index()

            st.dataframe(df_mapa_filtrado_group_parceiro.sort_values(by='Paxs Totais', ascending=False), hide_index=True)

    elif data_inicial and data_final and base_luck!='Todas' and base_luck and data_inicial.month != data_final.month:

        df_mapa_ref = gerar_dfs_base(base_luck)

        df_mapa_filtrado = df_mapa_ref[(df_mapa_ref['Data Execucao'] >= data_inicial) & (df_mapa_ref['Data Execucao'] <= data_final) & 
                                    (df_mapa_ref['Tipo de Servico']=='IN')].reset_index(drop=True)
        
        df_mapa_filtrado['Paxs Totais'] = df_mapa_filtrado['Total ADT'] + df_mapa_filtrado['Total CHD']

        df_mapa_filtrado = criar_coluna_ano_mes(df_mapa_filtrado)

        row1 = st.columns(2)

        with row1[0]:

            df_mapa_filtrado_group = df_mapa_filtrado.groupby(['Ano/Mês'])['Paxs Totais'].sum().reset_index()

            grafico_linha_numero(df_mapa_filtrado_group, 'Ano/Mês', 'Paxs Totais', 'Paxs IN', 'Paxs IN')

        with row1[1]:

            lista_maiores_parceiros = df_mapa_filtrado.groupby(['Parceiro'])['Paxs Totais'].sum().reset_index()\
                .sort_values(by='Paxs Totais', ascending=False).reset_index(drop=True).iloc[:5]['Parceiro'].tolist()
            
            df_mapa_filtrado_group_parceiro = df_mapa_filtrado[df_mapa_filtrado['Parceiro'].isin(lista_maiores_parceiros)]\
                .groupby(['Ano/Mês', 'Parceiro'])['Paxs Totais'].sum().reset_index()
            
            df_mapa_filtrado_group_parceiro = transformar_em_varias_colunas(df_mapa_filtrado_group_parceiro, 'Parceiro')

            lista_colunas = df_mapa_filtrado_group_parceiro.columns.tolist()

            grafico_cinco_linhas_numero(df_mapa_filtrado_group_parceiro, 'Ano/Mês', lista_colunas[1], lista_colunas[1], lista_colunas[2], 
                                        lista_colunas[2], lista_colunas[3], lista_colunas[3], lista_colunas[4], lista_colunas[4], 
                                        lista_colunas[5], lista_colunas[5], 'Paxs IN - Maiores Operadoras')

    elif data_inicial and data_final and base_luck=='Todas' and data_inicial.month == data_final.month:

        mapa_router_geral = gerar_mapa_router_geral()

        mapa_router_geral_filtrado = mapa_router_geral[(mapa_router_geral['Data Execucao'] >= data_inicial) & 
                                                    (mapa_router_geral['Data Execucao'] <= data_final) & 
                                                    (mapa_router_geral['Tipo de Servico']=='IN')].reset_index(drop=True)
        
        mapa_router_geral_filtrado['Paxs Totais'] = mapa_router_geral_filtrado['Total ADT'] + mapa_router_geral_filtrado['Total CHD']

        df_mapa_filtrado_group = mapa_router_geral_filtrado.groupby('Base Luck')['Paxs Totais'].sum().reset_index()

        row1 = st.columns(2)

        with row1[0]:

            st.dataframe(df_mapa_filtrado_group.sort_values(by='Paxs Totais', ascending=False), hide_index=True)

        with row1[1]:

            grafico_pizza(df_mapa_filtrado_group, 'Paxs Totais', 'Base Luck')

    elif data_inicial and data_final and base_luck=='Todas' and data_inicial.month != data_final.month:

        mapa_router_geral = gerar_mapa_router_geral()

        mapa_router_geral_filtrado = mapa_router_geral[(mapa_router_geral['Data Execucao'] >= data_inicial) & 
                                                    (mapa_router_geral['Data Execucao'] <= data_final) & 
                                                    (mapa_router_geral['Tipo de Servico']=='IN')].reset_index(drop=True)
        
        mapa_router_geral_filtrado['Paxs Totais'] = mapa_router_geral_filtrado['Total ADT'] + mapa_router_geral_filtrado['Total CHD']

        mapa_router_geral_filtrado = criar_coluna_ano_mes(mapa_router_geral_filtrado)
        
        df_mapa_filtrado_group = mapa_router_geral_filtrado.groupby(['Ano/Mês', 'Base Luck'])['Paxs Totais'].sum().reset_index()

        df_mapa_filtrado_group_2 = transformar_em_varias_colunas(df_mapa_filtrado_group, 'Base Luck')

        df_mapa_filtrado_group_geral = mapa_router_geral_filtrado.groupby('Base Luck')['Paxs Totais'].sum().reset_index()

        row1 = st.columns(2)

        with row1[0]:

            grafico_seis_linhas_numero(df_mapa_filtrado_group_2, 'Ano/Mês', 'JPA', 'João Pessoa', 'NAT', 'Natal', 'REC', 'Recife', 'MCZ', 
                                        'Maceió', 'SSA', 'Salvador', 'NOR', 'Noronha', 'Paxs IN')
            
        with row1[1]:

            grafico_pizza(df_mapa_filtrado_group_geral, 'Paxs Totais', 'Base Luck')


if tipo_analise=='% Serviços': 
    
    if data_inicial and data_final and base_luck and base_luck!='Todas' and data_inicial.month == data_final.month:

        df_mapa_ref = gerar_dfs_base(base_luck)

        df_mapa_filtrado = df_mapa_ref[(df_mapa_ref['Data Execucao'] >= data_inicial) & (df_mapa_ref['Data Execucao'] <= data_final) & 
                                    (df_mapa_ref['Status do Servico']!='CANCELADO') & 
                                    (df_mapa_ref['Status do Servico']!='RASCUNHO')].reset_index(drop=True)
        
        df_mapa_filtrado['Paxs Totais'] = df_mapa_filtrado['Total ADT'] + df_mapa_filtrado['Total CHD']

        df_mapa_filtrado_group = df_mapa_filtrado.groupby('Tipo de Servico')['Paxs Totais'].sum().reset_index()

        row1 = st.columns(2)

        with row1[0]:

            st.dataframe(df_mapa_filtrado_group.sort_values(by='Paxs Totais', ascending=False), hide_index=True)

        with row1[1]:

            grafico_pizza(df_mapa_filtrado_group, 'Paxs Totais', 'Tipo de Servico')

    if data_inicial and data_final and base_luck and base_luck!='Todas' and data_inicial.month != data_final.month:

        df_mapa_ref = gerar_dfs_base(base_luck)

        df_mapa_filtrado = df_mapa_ref[(df_mapa_ref['Data Execucao'] >= data_inicial) & (df_mapa_ref['Data Execucao'] <= data_final) & 
                                    (df_mapa_ref['Status do Servico']!='CANCELADO') & 
                                    (df_mapa_ref['Status do Servico']!='RASCUNHO')].reset_index(drop=True)
        
        df_mapa_filtrado['Paxs Totais'] = df_mapa_filtrado['Total ADT'] + df_mapa_filtrado['Total CHD']

        df_mapa_filtrado = criar_coluna_ano_mes(df_mapa_filtrado)

        df_mapa_filtrado_group = df_mapa_filtrado.groupby(['Ano/Mês', 'Tipo de Servico'])['Paxs Totais'].sum().reset_index()

        df_mapa_filtrado_group_2 = transformar_em_varias_colunas(df_mapa_filtrado_group, 'Tipo de Servico')

        df_mapa_filtrado_group_2['Total'] = df_mapa_filtrado_group_2[['OUT', 'IN', 'TOUR', 'TRANSFER']].sum(axis=1)

        df_mapa_filtrado_group_2['% OUT'] = round(df_mapa_filtrado_group_2['OUT'] / df_mapa_filtrado_group_2['Total'], 2)

        df_mapa_filtrado_group_2['% IN'] = round(df_mapa_filtrado_group_2['IN'] / df_mapa_filtrado_group_2['Total'], 2)

        df_mapa_filtrado_group_2['% TOUR'] = round(df_mapa_filtrado_group_2['TOUR'] / df_mapa_filtrado_group_2['Total'], 2)

        df_mapa_filtrado_group_2['% TRANSFER'] = round(df_mapa_filtrado_group_2['TRANSFER'] / df_mapa_filtrado_group_2['Total'], 2)

        row1 = st.columns(1)

        with row1[0]:

            grafico_quatro_linhas_percentual(df_mapa_filtrado_group_2, 'Ano/Mês', '% IN', 'IN', '% OUT', 'OUT', '% TOUR', 'TOUR', 
                                             '% TRANSFER', 'TRANSFER', '')

