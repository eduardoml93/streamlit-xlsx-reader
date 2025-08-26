import streamlit as st
import pandas as pd
import base64
import plotly.express as px

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

def load_data(uploaded_file):
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    selected_sheet = st.selectbox("Selecione a aba para visualizar:", sheet_names)
    df = pd.read_excel(xls, sheet_name=selected_sheet)
    return df, selected_sheet

def page_analises(df):
    st.write("### Informações sobre os Dados:")
    st.write("**Tipos de Dados:**")
    st.write(df.dtypes)

    st.write("**Valores Nulos por Coluna:**")
    st.write(df.isnull().sum())

    # st.write("**Número de Registros Duplicados:**")
    # st.write(df.duplicated().sum())
    num_duplicados = st.session_state.df.duplicated().sum()
    st.metric(label="Número de Registros Duplicados", value=num_duplicados)

    st.write("**Número de Valores Únicos por Coluna:**")
    st.write(df.nunique())

    st.write("**Estatísticas Descritivas:**")
    st.write(df.describe())

    st.write("**Distribuição Percentual de Valores Nulos:**")
    st.write((df.isnull().sum() / len(df)) * 100)

def page_graficos(df):
    st.write("## Visualizações Gráficas 📊")
    num_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(include='object').columns

    # Histograma
    st.write("### Histograma")
    if len(num_cols) > 0:
        selected_hist = st.selectbox("Selecione a coluna numérica:", num_cols, key="hist")
        fig_hist = px.histogram(df, x=selected_hist, nbins=20, title=f"Distribuição de {selected_hist}")
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("Não há colunas numéricas para histograma.")

    # Dispersão
    st.write("### Gráfico de Dispersão")
    if len(num_cols) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            selected_x = st.selectbox("Eixo X:", num_cols, key="scatter_x")
        with col2:
            selected_y = st.selectbox("Eixo Y:", num_cols, key="scatter_y")
        fig_scatter = px.scatter(df, x=selected_x, y=selected_y, title=f"Dispersão: {selected_x} vs {selected_y}")
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Não há colunas numéricas suficientes para dispersão.")

    # Boxplot
    st.write("### Boxplot")
    if len(num_cols) > 0:
        selected_box = st.selectbox("Selecione a coluna numérica:", num_cols, key="box")
        fig_box = px.box(df, y=selected_box, title=f"Boxplot de {selected_box}")
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.info("Não há colunas numéricas para boxplot.")

    # Gráfico de contagem (categorias)
    st.write("### Gráfico de Contagem (colunas categóricas)")
    if len(cat_cols) > 0:
        selected_cat = st.selectbox("Selecione a coluna categórica:", cat_cols, key="bar")
        count_data = df[selected_cat].value_counts().reset_index()
        count_data.columns = [selected_cat, "Quantidade"]
        fig_bar = px.bar(count_data, x=selected_cat, y="Quantidade", title=f"Contagem de {selected_cat}")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Não há colunas categóricas para gráfico de contagem.")

    # Heatmap
    st.write("### Mapa de Calor (Correlação entre Variáveis Numéricas) 🌡️")
    if len(num_cols) > 1:
        corr = df[num_cols].corr()
        fig_heatmap = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu_r",
            title="Mapa de Calor das Correlações"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.info("Não há colunas numéricas suficientes para gerar o mapa de calor.")

def main():
    st.markdown('<div class="title-box">Explorador XLSX</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Faça o upload do seu arquivo XLSX", type=["xlsx"])
    
    if uploaded_file is not None:
        df, sheet_name = load_data(uploaded_file)

        # Menu lateral para páginas
        page = st.sidebar.radio("Selecione a página:", ["Análises", "Gráficos"])
        
        if page == "Análises":
            page_analises(df)
        elif page == "Gráficos":
            page_graficos(df)

if __name__ == "__main__":
    main()


