import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora do Coeficiente de Gini", layout="centered")

st.title("Calculadora do Coeficiente de Gini")
st.markdown("Calcule o índice de Gini a partir de dados de renda.")

st.header("1. Configuração dos Dados")

option = st.radio(
    "Como deseja inserir os dados?",
    ["Usar dados de exemplo", "Upload de arquivo"]
)

df = None
dados_exemplo = False

if option == "Usar dados de exemplo":
    st.info("Usando dados de exemplo com 1000 observações de renda")
    st.warning("**Atenção:** Dados fictícios gerados aleatoriamente para fins educacionais e de estudo.")
    np.random.seed(42)
    dados_exemplo = True
    
    rendas_exemplo = []
    rendas_exemplo.extend(np.random.uniform(1420, 4000, 600))
    rendas_exemplo.extend(np.random.uniform(4000, 10000, 250))
    rendas_exemplo.extend(np.random.uniform(10000, 30000, 100))
    rendas_exemplo.extend(np.random.uniform(30000, 100000, 50))
    
    np.random.shuffle(rendas_exemplo)
    
    df = pd.DataFrame({'Renda': rendas_exemplo})
        
elif option == "Upload de arquivo":
    st.subheader("Upload de Arquivo")
    
    st.info("""
    **Instruções para upload de arquivo:**
    - O arquivo deve ser Excel (.xlsx) ou CSV (.csv)
    - Deve conter uma coluna chamada **'Renda'** ou **'renda'**
    - A coluna 'Renda' deve conter valores numéricos
    - Cada linha representa uma pessoa/observação
    - Valores não numéricos serão ignorados
    """)
    
    uploaded_file = st.file_uploader("Escolha um arquivo Excel ou CSV", type=['xlsx', 'csv'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            
            coluna_renda = None
            for col in df.columns:
                if col.lower() == 'renda':
                    coluna_renda = col
                    break
            
            if coluna_renda is None:
                st.error("**Erro:** O arquivo deve conter uma coluna chamada 'Renda' ou 'renda'")
                st.info("Colunas encontradas no arquivo: " + ", ".join(df.columns.tolist()))
                df = None
            else:
                if coluna_renda != 'Renda':
                    df = df.rename(columns={coluna_renda: 'Renda'})
                
                df['Renda'] = pd.to_numeric(df['Renda'], errors='coerce')
                df = df.dropna(subset=['Renda'])
                
                if len(df) == 0:
                    st.error("**Erro:** Nenhum valor numérico válido encontrado na coluna 'Renda'")
                    df = None
                else:
                    st.success(f"Arquivo carregado com sucesso! {len(df)} registros válidos encontrados.")
                    
        except Exception as e:
            st.error(f"**Erro ao ler o arquivo:** {str(e)}")
            df = None

if df is not None:
    st.header("2. Dados e Resultados")
    
    st.subheader("Dados de Renda")
    df_ordenado = df.sort_values('Renda').reset_index(drop=True)
    st.dataframe(df_ordenado.head(10))
    if dados_exemplo:
        st.caption(f"Total de registros: {len(df)} | Dados ordenados do menor para o maior")
    else:
        st.caption(f"Total de registros: {len(df)} | Dados ordenados do menor para o maior")
    
    df_calc = df_ordenado.copy()
    df_calc['ID'] = range(1, len(df_calc) + 1)
    df_calc['Renda Acumulada'] = df_calc.Renda.cumsum()
    df_calc['População Acumulada'] = (df_calc.index + 1) / len(df_calc)
    df_calc['Renda Acumulada Proporcional'] = df_calc.Renda.cumsum() / df_calc.Renda.sum()
    df_calc['Posição'] = range(1, len(df_calc) + 1)
    df_calc['Soma Ponderada pela Posição'] = df_calc['Renda'] * df_calc['Posição']
    
    soma_ponderada = df_calc['Soma Ponderada pela Posição'].sum()
    soma_renda = df_calc['Renda'].sum()
    n = len(df_calc)
    
    gini = ((2 * soma_ponderada / soma_renda) - (n + 1)) / n
    gini = round(gini, 4)
    
    st.subheader("Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Coeficiente de Gini", f"{gini:.4f}")
    
    with col2:
        st.metric("Número de Observações", n)
    
    with col3:
        st.metric("Renda Total", f"R$ {soma_renda:,.0f}")
    
    st.subheader("Análise por Grupos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        percentual_ricos = st.slider("Percentual mais rico (%)", 1, 50, 20)
        n_ricos = int(n * percentual_ricos / 100)
        if n_ricos > 0:
            renda_ricos = df_calc.tail(n_ricos)['Renda'].sum()
            participacao_ricos = renda_ricos / soma_renda
        else:
            participacao_ricos = 0
        
        st.metric(
            f"Renda dos {percentual_ricos}% mais ricos", 
            f"{participacao_ricos:.1%}"
        )
    
    with col2:
        percentual_pobres = st.slider("Percentual mais pobre (%)", 1, 50, 20)
        n_pobres = int(n * percentual_pobres / 100)
        if n_pobres > 0:
            renda_pobres = df_calc.head(n_pobres)['Renda'].sum()
            participacao_pobres = renda_pobres / soma_renda
        else:
            participacao_pobres = 0
        
        st.metric(
            f"Renda dos {percentual_pobres}% mais pobres", 
            f"{participacao_pobres:.1%}"
        )
    
    if participacao_pobres > 0:
        razao = participacao_ricos / participacao_pobres
        st.metric(
            f"Razão {percentual_ricos}% mais ricos / {percentual_pobres}% mais pobres",
            f"{razao:.2f}"
        )
    
    st.subheader("Curva de Lorenz")
    
    populacao_acumulada = [0] + df_calc['População Acumulada'].tolist()
    renda_acumulada = [0] + df_calc['Renda Acumulada Proporcional'].tolist()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.plot(populacao_acumulada, renda_acumulada, 'b-', linewidth=2, label='Curva de Lorenz')
    
    ax.plot([0, 1], [0, 1], 'r--', linewidth=2, label='Igualdade Perfeita')
    
    ax.fill_between(populacao_acumulada, renda_acumulada, populacao_acumulada, alpha=0.3, color='gray')
    
    ax.set_xlabel('Proporção Acumulada da População', fontsize=12)
    ax.set_ylabel('Proporção Acumulada da Renda', fontsize=12)
    ax.set_title('Curva de Lorenz', fontsize=14, fontweight='bold')
    
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    for i in range(0, 101, 10):
        ax.axhline(i/100, alpha=0.1, color='black', linestyle='-')
        ax.axvline(i/100, alpha=0.1, color='black', linestyle='-')
    
    ax.legend()
    
    ax.text(0.02, 0.95, f'Coeficiente de Gini: {gini}', transform=ax.transAxes, 
            fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    st.pyplot(fig)
    
    st.markdown("""
    **Interpretação da Curva de Lorenz:**
    - **Linha vermelha tracejada**: Igualdade perfeita (se todos tivessem a mesma renda)
    - **Curva azul**: Distribuição real da renda
    - **Área cinza**: Representa a desigualdade (quanto maior a área, maior a desigualdade)
    """)
    
    st.subheader("Exportar Resultados")
        
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_calc.to_excel(writer, sheet_name='Dados_Calculados', index=False)
        
        resumo = pd.DataFrame({
            'Métrica': ['Coeficiente de Gini', 'Número de Observações', 'Renda Total', 
                       f'Participação dos {percentual_ricos}% mais ricos',
                       f'Participação dos {percentual_pobres}% mais pobres',
                       f'Razão entre grupos'],
            'Valor': [gini, n, f"R$ {soma_renda:,.2f}", 
                     f"{participacao_ricos:.1%}", 
                     f"{participacao_pobres:.1%}",
                     f"{razao:.2f}" if participacao_pobres > 0 else "N/A"]
        })
        resumo.to_excel(writer, sheet_name='Resumo', index=False)
    
    excel_data = output.getvalue()
    
    st.download_button(
        label="Baixar dados calculados (Excel)",
        data=excel_data,
        file_name="dados_gini_calculados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("Configure os dados acima para calcular o coeficiente de Gini")

st.markdown("---")
st.caption("Calculadora do Coeficiente de Gini - Desenvolvida por João Daniel Temporin para análise de desigualdade de renda")
