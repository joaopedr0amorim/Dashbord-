import streamlit as st
import plotly.express as px
from impor_dt import df
from graficos import gmapa, gmapa2,gbarra,gbar,gven,grafico_vendas

st.set_page_config(layout='wide')
st.title('Dashbord de Vendas :shopping_trolley:')
#criar filtros laterais
#with st.sidebar:
    #st.sidebar.write('teste')
st.sidebar.title('Filtro de Valores')

filtro=st.sidebar.multiselect(
    'Vendedor',
    df['Vendedor'].unique()
)
if filtro:
    df=df[df['Vendedor'].isin(filtro)]

filtro2=st.sidebar.multiselect(
    'Categoria do Produto',
    df['Categoria do Produto'].unique()
)
if filtro2:
    df=df[df['Categoria do Produto'].isin(filtro2)]

filtro3=st.sidebar.multiselect(
    'Local da compra',
    df['Local da compra'].unique()
)
if filtro3:
    df=df[df['Local da compra'].isin(filtro3)]
def format_nmber(value,prefix=''):
    for unit in ['','mil']:
        if value < 1000:
            return f'{prefix} {value:.2f} {unit}'
        value /=1000
        return f'{prefix} {value:.2f} milhões'
#fazer mapa
#arrumar os dados 

#criar varias abas
aba1,aba2,aba3 = st.tabs(['Dataset','Receita','Vendedores'])
#colocar coisas na aba 1
with aba1:
    st.dataframe(df)

#metrica aba2
#metrica= a pequenas caixa de texto
with aba2:
    coluna1,coluna2=st.columns(2)
    with coluna1:
        receita_milhoes = df['Preço'].sum() / 1_000_000
        st.metric('Receita Total (Milhões)', f'{receita_milhoes:.2f}M')
        #st.metric('Receita Total', df['Preço'].sum())
        #colocar o mapa
        st.plotly_chart(gmapa, use_container_width=True)
        st.plotly_chart(gbarra, use_container_width=True)
    with coluna2:
        quantidade_vendas_milhares = df.shape[0] / 1_000
        st.metric('Quantidade de Vendas', f'{quantidade_vendas_milhares:.2f}K')
        #st.metric('Quantidade de vendas', df.shape[0])
        st.plotly_chart(gmapa2,use_container_width=True)
        st.plotly_chart(gbar,use_container_width=True)
with aba3:
    coluna1,coluna2=st.columns(2)
    with coluna1:
        st.plotly_chart(gven, use_container_width=True)
    with coluna2:
        st.plotly_chart(grafico_vendas)
