import streamlit as st
import pandas as pd
import base64

# Função para carregar a imagem e convertê-la para base64
def get_base64_of_image(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Definir o background com a imagem convertida em base64
def set_background(image_file):
    base64_str = get_base64_of_image(image_file)
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{base64_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .title-box {{
        background: rgba(0, 0, 0, 0.6);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: bold;
        width: 60%;
        margin: auto;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Aplicando o background
set_background("bg.jpeg")

def main():
    st.markdown('<div class="title-box">XLSX Reader APP</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Faça o upload do seu arquivo XLSX", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            xls = pd.ExcelFile(uploaded_file)
            sheet_names = xls.sheet_names
            
            selected_sheet = st.selectbox("Selecione a aba para visualizar:", sheet_names)
            
            df = pd.read_excel(xls, sheet_name=selected_sheet)
            
            st.write(f"### Visualização dos Dados ({selected_sheet}):")
            st.dataframe(df)
            
            st.write("### Informações sobre os Dados:")
            st.write("**Tipos de Dados:**")
            st.write(df.dtypes)
            
            st.write("**Valores Nulos por Coluna:**")
            st.write(df.isnull().sum())
            
            st.write("**Número de Registros Duplicados:**")
            st.write(df.duplicated().sum())

            st.write("**Número de Valores Únicos por Coluna:**")
            st.write(df.nunique())

            st.write("**Estatísticas Descritivas:**")
            st.write(df.describe())

            st.write("**Distribuição Percentual de Valores Nulos:**")
            st.write((df.isnull().sum() / len(df)) * 100)
        
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")

if __name__ == "__main__":
    main()
