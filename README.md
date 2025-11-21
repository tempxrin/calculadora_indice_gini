# Calculadora do Coeficiente de Gini

Aplicação web interativa para cálculo e visualização do Coeficiente de Gini, desenvolvida com Streamlit.

## Descrição

Esta ferramenta permite calcular o índice de Gini, uma medida estatística de desigualdade na distribuição de renda. O coeficiente varia de 0 (igualdade perfeita) a 1 (desigualdade máxima).

## Funcionalidades

### Entrada de Dados
- **Dados de exemplo**: 1000 observações fictícias com distribuição realista de renda brasileira
- **Entrada manual**: Interface para inserir dados individualmente
- **Upload de arquivo**: Suporte para arquivos Excel (.xlsx) e CSV (.csv)

### Análises Disponíveis
- Cálculo do Coeficiente de Gini
- Estatísticas descritivas (número de observações, renda total)
- Análise por grupos (percentuais mais ricos e mais pobres)
- Razão entre grupos de renda
- Curva de Lorenz com visualização gráfica
- Exportação de resultados em Excel

## Instalação e Execução

### Requisitos
- Python 3.10 ou superior
- Git

### Passo a Passo

1. Clone o repositório:
```bash
git clone https://github.com/tempxrin/calculadora_indice_gini.git
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
streamlit run app.py
```

## Metodologia

O cálculo do Coeficiente de Gini é realizado através da fórmula:

```
Gini = ((2 * Σ(i × Yi)) / (n × ΣYi)) - ((n + 1) / n)
```

Onde:
- i = posição ordenada da observação
- Yi = valor da renda na posição i
- n = número total de observações

## Interpretação dos Resultados

### Coeficiente de Gini
- 0.0 a 0.3: Baixa desigualdade
- 0.3 a 0.5: Desigualdade moderada
- 0.5 a 0.7: Alta desigualdade
- 0.7 a 1.0: Desigualdade extrema

### Curva de Lorenz
A curva mostra a distribuição acumulada da renda. Quanto maior a área entre a curva real e a linha de igualdade perfeita, maior a desigualdade.

## Exportação

Os resultados podem ser exportados em formato Excel contendo:
- **Planilha "Dados_Calculados"**: Todos os dados processados com cálculos intermediários
- **Planilha "Resumo"**: Métricas principais e indicadores de desigualdade

## Notas Técnicas

- Valores de renda devem ser numéricos e positivos
- Valores não numéricos são automaticamente removidos durante o processamento
- Dados de exemplo são fictícios e gerados para fins educacionais