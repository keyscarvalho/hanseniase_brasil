#%%

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# importando dataset
df = pd.read_csv('../data/ano_uf_hanseniase.csv', encoding='latin1', sep=';', skiprows=3, skipfooter=18)

# renomeando coluna para facilitar análise
df.rename(columns={'Ano Diagnóstico' : 'ano_diagnostico'}, inplace = True)

# filtrando os dados
df = (
    df[df['ano_diagnostico'] != '<1975']
      .drop(columns=['IG', 'Total'])
      .replace('-', 0)
)

# transformar as colunas UF em uma única coluna
df_long = df.melt(id_vars='ano_diagnostico', 
                  var_name='UF', 
                  value_name='casos')

# converter os casos para tipo numérico
df_long['casos'] = pd.to_numeric(df_long['casos'], errors='coerce')

# agrupar por UF e somar casos
df_total = df.groupby('UF')['casos'].sum().reset_index()

# ordenar do maior para o menor
df_total.sort_values(by='casos', ascending=False)

# visualização de casos por uf ao longo dos anos
plt.figure(figsize=(14,6))
sns.barplot(data=df_total, x='UF', y='casos', color='royalblue')

plt.title('Total de Casos por UF de 1975 à 2025', pad=10)
plt.xlabel('UF', labelpad=10)
plt.ylabel('Número total de casos', labelpad=10)

#%%

# agrupar por ano e somar casos
df_total = df.groupby('ano_diagnostico')['casos'].sum().reset_index()

# ordenar do maior para o menor
df_total.sort_values(by='ano_diagnostico', ascending=True)

# convertendo números para inteiro
df_total['ano_diagnostico'] = df_total['ano_diagnostico'].astype(int)

# visualização de casos por ano
plt.figure(figsize=(14, 6))
sns.lineplot(data=df_total, x='ano_diagnostico', y='casos', color='royalblue')

plt.title('Total de Casos de Hanseníase por Ano (1975-2025)', pad=10)
plt.xlabel('Ano', labelpad=10)
plt.ylabel('Número total de casos', labelpad=10)

# define os anos pulando de 5 em 5 no eixo x
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))

plt.tight_layout()