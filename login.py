import streamlit as st

# Função para verificar o login
def verificar_login(usuario, senha):
    # Aqui você pode adicionar a lógica para verificar o usuário e senha
    # Por exemplo, verificar em um banco de dados ou uma lista de usuários
    usuarios = {
        "admin": "admin123",
        "usuario": "senha123"
    }
    
    if usuario in usuarios and usuarios[usuario] == senha:
        return True
    else:
        return False

# Configuração da página
st.set_page_config(page_title="Página de Login", page_icon="🔒")

# Título da página
st.title("Página de Login")

# Inputs para o usuário e senha
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

# Botão de login
if st.button("Login"):
    if verificar_login(usuario, senha):
        st.success("Login realizado com sucesso!")
        # Aqui você pode redirecionar para outra página ou exibir conteúdo restrito
        st.write("Bem-vindo à página restrita!")
    else:
        st.error("Usuário ou senha incorretos")