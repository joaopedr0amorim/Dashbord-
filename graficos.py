import plotly.express as px
from utilis import df_rec_estado, df_rec_mensal,df_rec_cat,df_ven

gmapa = px.scatter_geo(
    df_rec_estado,
    lat='lat',  # Correção para 'lat' com letra minúscula
    lon='lon',  # Correção para 'lon' com letra minúscula
    scope='south america',
    size='Preço',
    template='seaborn',
    hover_name='Local da compra',
    hover_data={'lat': False, 'lon': False},  # Correção de 'lom' para 'lon'
    title='Receita por Estado',
    width=500,  # Largura do gráfico
    height=500   # Altura do gráfico
)

#mapa quantidade

gmapa2=px.line(
    df_rec_mensal,
    x='Mes',
    y='Preço',
    markers=True,
    range_y=(0,df_rec_mensal.max()),
    color='Ano',
    line_dash='Ano',
    title='Receita Mensssal'
)

gmapa2.update_layout(yaxis_title='Receita')

gbarra= px.bar(
    df_rec_estado.head(10),
    x='Local da compra',
    y='Preço',
    text_auto=True,
    title='TOP Receitas por Estado'
)

#head=aos maiores
#taill=aos menores

gbar= px.bar(
    df_rec_cat.head(7),
    text_auto=True,
    title='Receita por categoria'
)
#grafico de vendedores
gven = px.bar(
    df_ven[['sum']].sort_values('sum', ascending=False).head(7),
    x = 'sum',
    y = df_ven[['sum']].sort_values('sum', ascending=False).head(7).index,
    text_auto = True,
    title = 'Top 7 Vendedores por Receita'
)

#grafico de vendedores
grafico_vendas=px.bar(
    df_ven[['count']].sort_values('count',ascending=False).head(7),
    x ='count',
    y = df_ven[['count']].sort_values('count',ascending=False).head(7).index,
    text_auto=True,
    title='Top Vendas dos 7 Vendedores'
)

