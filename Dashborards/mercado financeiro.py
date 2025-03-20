import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid

def build_sidebar():
    st.image(r"C:\Users\joaop\OneDrive\Documentos\teste vs\Dashborards\imagens\images.png")
    ticker_list=pd.read_csv(r'C:\Users\joaop\OneDrive\Documentos\teste vs\tickers_ibra.csv', index_col=0)
    tickers= st.multiselect(label='Selecione as Empresas', options=ticker_list, placeholder='Códigos')
    tickers = [t+".SA" for t in tickers]
    start_date= st.date_input('De', format='DD/MM/YYYY', value=datetime(2023,1,2))
    end_date= st.date_input('Até', format='DD/MM/YYYY', value="today")

    if tickers:
        prices= yf.download(tickers,start=start_date, end=end_date)["Close"]
        prices.columns = prices.columns.str.rstrip(".SA")
        prices['IBOV'] = yf.download("^BVSP", start=start_date, end=end_date)["Close"]
        return tickers, prices
    return None, None

def build_main(tickers, prices):
    # Calcula os pesos, normalização, retornos e volatilidade
    weights = np.ones(len(tickers)) / len(tickers)
    prices['portfolio'] = prices.drop("IBOV", axis=1) @ weights
    norm_prices = 100 * prices / prices.iloc[0]
    returns = prices.pct_change()[1:]
    vols = returns.std() * np.sqrt(252)
    rets = (norm_prices.iloc[-1] - 100) / 100

    # Define o grid para o layout
    mygrid = grid(4, 4, 4, 4)  # Espaçamento entre os ativos

    for t in prices.columns:
        # Cria container para cada ativo
        c = mygrid.container(border=False)
        c.subheader(t, divider="red")  # Título do ativo
        
        # Layout de colunas para os dados e imagem
        colA, colB, colC = c.columns([1, 2, 2])  # Coluna A menor para imagens
        
        # Define a imagem com base no ativo ou portfólio
        if t == "portfolio":
            colA.image(r"C:\Users\joaop\OneDrive\Documentos\teste vs\Dashborards\imagens\images.png", width=60)
        elif t == "IBOV":
            colA.image(r"C:\Users\joaop\OneDrive\Documentos\teste vs\Dashborards\imagens\b3-on-nm--600.png")
        else:
            colA.image(f'https://raw.githubusercontent.com/thefintz/icones-b3/main/icones/{t}.png', width=60)
        
        # Exibe as métricas de retorno e volatilidade
        #colB.metric(label="retorno", value=f"{rets[t] * 100:.0f}%")  # Sem casas decimais
        colB.metric(label="retorno", value=f"{rets[t] * 100:.0f}%")  # Uma casa decimal
        colC.metric(label="volatilidade", value=f"{vols[t] * 100:.0f}%")  # Sem casas decimais

    # Estiliza os cartões para se assemelhar à imagem 2
    style_metric_cards(
        background_color="rgba(255,255,255,0)",  # Fundo transparente
        border_color="rgba(200, 200, 200, 0.5)",  # Bordas sutis
    )

    col1,col2=st.columns(2,gap='large')
    with col1:
        st.subheader('Desempenho Relativo')
        st.line_chart(norm_prices, height=600)
    with col2: 
        st.subheader('Risco-Retorno')
        fig = px.scatter(
            x=vols,
            y=rets,
            text=vols.index,
            color=rets/vols,
            color_continuous_scale=px.colors.sequential.Bluered_r
        )
        fig.update_traces(
            textfont_color='white', 
            marker=dict(size=45),
            textfont_size=10,                  
        )
        fig.layout.yaxis.title = 'Retorno Total'
        fig.layout.xaxis.title = 'Volatilidade (anualizada)'
        fig.layout.height = 600
        fig.layout.xaxis.tickformat = ".0%"
        fig.layout.yaxis.tickformat = ".0%"        
        fig.layout.coloraxis.colorbar.title = 'Sharpe'
        st.plotly_chart(fig, use_container_width=True)

st.set_page_config(layout='wide')

with st. sidebar:
    tickers, prices = build_sidebar()

st.title('PYthon para Investidores')
if tickers:
    build_main(tickers, prices)
    