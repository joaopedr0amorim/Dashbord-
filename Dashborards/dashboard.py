import json
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as nygit
#importa dados
file= open(r'C:\Users\joaop\OneDrive\Documentos\teste vs\dados\vendas.json')
data= json.load(file)

#transforma json em dataframe
df= pd.DataFrame.from_dict(data)
#print(df)
df['Data da Compra']=pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')
file.close()
#layout
st.set_page_config(layout='wide')
st.title('Dashbord de Vendas :shopping_trolley:')
#criar filtros laterais
#with st.sidebar:
    #st.sidebar.write('teste')
# Título da sidebar
st.sidebar.title('Filtro de Valores')

# Filtro por 'Vendedor'
filtro = st.sidebar.multiselect(
    'Vendedor',
    df['Vendedor'].unique()
)
if filtro:
    df = df[df['Vendedor'].isin(filtro)]

# Filtro por 'Categoria do Produto'
filtro2 = st.sidebar.multiselect(
    'Categoria do Produto',
    df['Categoria do Produto'].unique()
)
if filtro2:
    df = df[df['Categoria do Produto'].isin(filtro2)]

# Filtro por 'Local da compra'
filtro3 = st.sidebar.multiselect(
    'Local da compra',
    df['Local da compra'].unique()
)
if filtro3:
    df = df[df['Local da compra'].isin(filtro3)]

with st.sidebar.expander('Preço do Produto'):
    preco = st.slider(
        'Selecione o Preço',
        min_value=int(df['Preço'].min()),
        max_value=int(df['Preço'].max()),
        value=(int(df['Preço'].min()), int(df['Preço'].max()))
    )
df = df[(df['Preço'] >= preco[0]) & (df['Preço'] <= preco[1])]

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
        
        # Agrupando receita por estado
        df_rec_estado = df.groupby('Local da compra')[['Preço']].sum()
        df_rec_estado = df.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(
            df_rec_estado, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)
        
        # Criando o segundo gráfico (gbarra) para o Top 10
        df_rec_estado['Preço_milhoes'] = df_rec_estado['Preço'] / 1_000_000  # Convertendo valores para milhões

        gbarra = px.bar(
            df_rec_estado.head(10),
            x='Local da compra',
            y='Preço',
            text=df_rec_estado.head(10)['Preço_milhoes'].apply(lambda x: f'{x:.2f}M'),  # Formata os textos corretamente
            text_auto=True,
            title='TOP Receitas por Estado',
            color='Preço',  # Mapeia a cor com base no valor para destacar os mais altos
            color_continuous_scale='Blues',  # Escolhe uma escala de cor apropriada
         )
        gbarra.update_traces(
            #texttemplate='%{text:.2s}',  # Formato dos rótulos, exibindo em milhões com um "M" como sufixo
            textposition='outside'  # Posiciona os rótulos fora das barras para maior clareza
        )
        gbarra.update_layout(
            xaxis_title='Local da compra',
            yaxis_title='Preço (Milhões)',
            title_x=0.4,  # Centraliza o título
            uniformtext_minsize=8,  # Ajusta o tamanho do texto
            uniformtext_mode='hide',  # Oculta o texto de rótulo que não cabe nas barras
            coloraxis_showscale=False,  # Remove a escala de cor para barras
            template='plotly_dark'  # Usa um tema escuro para combinar com o fundo
        )
        
        # Exibindo o gráfico de mapa
        st.plotly_chart(gbarra, use_container_width=True)
        
        # Criando o primeiro gráfico (gmapa)
        gmapa = px.scatter_geo(
            df_rec_estado,
            lat='lat',  # Latitude
            lon='lon',  # Longitude
            scope='south america',  # Define o escopo como América do Sul
            size='Preço',  # Tamanho das bolhas baseado na receita
            color='Preço',  # Cor das bolhas com base na receita
            color_continuous_scale=[(0, '#00cbeb'), (0.5, '#6497b1'), (1, '#000099')],  # Escala de cor personalizada em tons de azul,  # Escala de cor em tons de azul
            hover_name='Local da compra',  # Exibe o nome do local ao passar o cursor
            hover_data={'lat': False, 'lon': False, 'Preço': ':.2f'},  # Formata 'Preço' para duas casas decimais
            title='Receita por Estado',
)

# Melhorias no layout
        gmapa.update_geos(
            showland=True,
            center={'lat': -14.2350, 'lon': -51.9253},  # Centro aproximado do Brasil
            fitbounds="locations",  # Exibe a terra para contraste
            landcolor='lightgrey',  # Cor do fundo da terra
            showcountries=True,  # Exibe as fronteiras dos países
            countrycolor='black'  # Cor das bordas dos países
)

# Configurações adicionais de layout
        gmapa.update_layout(
            title_x=0.5,  # Centraliza o título
            template='plotly_dark',  # Tema claro para contraste
            coloraxis_showscale=True,  # Mostra a barra de escala de cor para receita
            coloraxis_colorbar=dict(
            title='Receita (R$)',  # Título da barra de cores
            #ticksuffix='M',  # Sufixo para milhões, se aplicável
            ),
            width=800,  # Largura do gráfico
            height=600  # Altura do gráfico
)

        # Exibindo o gráfico de barras
        st.plotly_chart(gmapa, use_container_width=True)
    with coluna2:
        quantidade_vendas = df.shape[0] / 1_000
        st.metric('Quantidade de Vendas', f'{quantidade_vendas:.2f}K')
        #arrumando os dados
        df_rec_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
        df_rec_mensal['Ano']=df_rec_mensal['Data da Compra'].dt.year
        df_rec_mensal['Mes']=df_rec_mensal['Data da Compra'].dt.month_name()
    #criando o mapa
        gmapa2 = px.line(
            df_rec_mensal,
            x='Mes',
            y='Preço',
            markers=True,
            range_y=(0, df_rec_mensal['Preço'].max()),  # Corrigido para pegar o máximo da coluna 'Preço'
            color='Ano',
            line_dash='Ano',
            title='Receita Mensal',
)
        gmapa2.update_traces(
            mode='lines+markers',  # Mostra tanto a linha quanto os marcadores
            marker=dict(size=6, symbol='circle'),  # Define o tamanho e o tipo de marcador
            line=dict(width=2)  # Define uma espessura de linha para maior visibilidade
)

# Personalização do layout
        gmapa2.update_layout(
            title_text='Receita Mensal por Ano',  # Título mais descritivo
            title_x=0.4,  # Centraliza o título
            xaxis_title='Mês',  # Rótulo do eixo X
            yaxis_title='Receita (R$)',  # Rótulo do eixo Y
            xaxis=dict(
            tickmode='array',  # Exibe os meses corretamente, sem repetir
            tickvals=df_rec_mensal['Mes'].unique(),  # Coloca todos os meses do DataFrame no eixo X
            ),
            legend_title='Ano',  # Título da legenda
            template='plotly_white'  # Define um tema claro para melhor contraste
)
        media_receita = df_rec_mensal['Preço'].mean()
        gmapa2.add_hline(y=media_receita, line_dash="dot", line_color="red", 
                 annotation_text="Média da Receita", annotation_position="top left")

#colocando no streamlit
        st.plotly_chart(gmapa2,use_container_width=True)
    
        df_rec_cat=df.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço',ascending=False)

        gpie = px.pie(
            df_rec_cat.head(7).reset_index(),  # Usando .reset_index() para transformar o índice em coluna
            names='Categoria do Produto',  # Nome da coluna para os rótulos das fatias
            values='Preço',  # Nome da coluna para os valores das fatias
            title='Receita por Categoria',
            color_discrete_sequence=px.colors.sequential.Blues_r   # Escolhe uma paleta de cores
)

# Ajustes de layout e rótulos
        gpie.update_traces(
            textinfo='percent+label',  # Exibe rótulos com o nome da categoria e o percentual
            pull=[0.1 if i == 0 else 0 for i in range(7)],  # Destaca a fatia com maior valor, opcional
            marker=dict(line=dict(color='black', width=0.5))  # Adiciona bordas às fatias
)

# Ajuste do layout
        gpie.update_layout(
            title_text='Receita por Categoria',  # Título do gráfico
            title_x=0.4,  # Centraliza o título
            template='plotly_white'  # Usa um tema claro
)

        st.plotly_chart(gpie,use_container_width=True)
with aba3:
    coluna1,coluna2=st.columns(2)
    with coluna1:
        df_ven = pd.DataFrame(df.groupby('Vendedor')['Preço'].agg(['sum', 'count']))
        
        gven = px.bar(
            df_ven[['sum']].sort_values('sum', ascending=False).head(7).reset_index(),
            x='sum',  # Receita total como eixo X
            y='Vendedor',  # Nome do vendedor como eixo Y
            orientation='h',  # Orientação horizontal
            text='sum',  # Exibe o valor da receita nas barras
            title='Top 7 Vendedores por Receita',
            color='sum',  # Colore as barras com base na receita
            color_continuous_scale='Blues'  # Escala de cores em tons de azul
)

# Melhorias de layout e estilo
        gven.update_traces(
            texttemplate='%{text:.2s}',  # Formata o texto para valores mais curtos (ex: 200k)
            textposition='outside',  # Posiciona os valores de receita fora das barras
            marker=dict(line=dict(color='black', width=0.5))  # Adiciona uma borda preta fina para melhor definição das barras
)

# Ajuste do layout
        gven.update_layout(
            title_x=0.5,  # Centraliza o título
            xaxis_title='Receita (R$)',  # Rótulo do eixo X
            yaxis_title='Vendedor',  # Rótulo do eixo Y
            yaxis=dict(categoryorder='total ascending'),  # Ordena os vendedores de cima para baixo
            template='plotly_white',  # Usa um tema claro
            coloraxis_showscale=False  # Remove a barra de cores para simplificar
)
        
        st.plotly_chart(gven, use_container_width=True)
    with coluna2:
        grafico_vendas = px.pie(
        df_ven[['count']].sort_values('count', ascending=False).head(7).reset_index(),
            names='Vendedor',  # Coluna para os rótulos das fatias
            values='count',  # Coluna para os valores das fatias
            title='Top 7 Vendedores por Número de Vendas',
            hole=0.4,  # Define o "furo" no centro para transformar em gráfico de rosca
            color_discrete_sequence=px.colors.sequential.Blues  # Define a paleta de cores em tons de azul
)

# Melhorias de layout e estilo
        grafico_vendas.update_traces(
            textinfo='percent+label',  # Exibe o percentual e o nome do vendedor
            marker=dict(line=dict(color='black', width=0.5))  # Adiciona bordas nas fatias
)

# Ajustes adicionais no layout
        grafico_vendas.update_layout(
            title_x=0.2,  # Centraliza o título
            template='plotly_white',  # Usa um tema claro
)

        st.plotly_chart(grafico_vendas)

