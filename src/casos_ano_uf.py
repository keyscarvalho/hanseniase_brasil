#%%

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# %%
# importando dataset

df = pd.read_csv('../data/ano_uf_hanseniase.csv', encoding='latin1', sep=';', skiprows=3, skipfooter=18)

# %%
# renomeando a coluna

df.rename(columns={'Ano Diagnóstico' : 'ano_diagnostico'}, inplace = True)
df.head()

#%%

# substituir traços por 0
df.replace('-', 0, inplace=True)

# transformar as colunas UF em uma única coluna
df_long = df.melt(id_vars='ano_diagnostico', 
                  var_name='UF', 
                  value_name='casos')

# converter os casos para tipo numérico
df_long['casos'] = pd.to_numeric(df_long['casos'], errors='coerce')

# filtrando os dados

df_filtrado = df_long[
    (~df_long["UF"].isin(["Total", "IG"])) & 
    (df_long["ano_diagnostico"].astype(str).str.match(r"^\d{4}$"))
]

df = df_filtrado

#%%

# agrupar por UF e somar casos

df_total = df.groupby('UF')['casos'].sum().reset_index()

# ordenar do maior para o menor

df_total.sort_values(by='casos', ascending=False)
# %%
# visualização casos por uf

plt.figure(figsize=(14,6))
sns.barplot(data=df_total, x='UF', y='casos', palette='Reds_r')

plt.title('Total de Casos por UF de 1975 à 2025', pad=20)
plt.xlabel('UF', labelpad=15)
plt.ylabel('Número total de casos', labelpad=15)

plt.savefig('total_casos_uf.png')

#%%

df_total = df.groupby('ano_diagnostico')['casos'].sum().reset_index()

# ordenar do maior para o menor

df_total.sort_values(by='ano_diagnostico', ascending=True)

#%%

# visualização

# Garante que os anos estão como números inteiros (e não strings)
df_total['ano_diagnostico'] = df_total['ano_diagnostico'].astype(int)

plt.figure(figsize=(14, 6))
sns.lineplot(data=df_total, x='ano_diagnostico', y='casos', color='firebrick')

plt.title('Total de Casos de Hanseníase por Ano (1975 a 2025)', pad=20)
plt.xlabel('Ano', labelpad=15)
plt.ylabel('Número total de casos', labelpad=15)

# Define os anos pulando de 5 em 5 no eixo x
anos = np.arange(df_total['ano_diagnostico'].min(), df_total['ano_diagnostico'].max()+1, 5)

plt.tight_layout()
plt.savefig('total_casos_ano.png')
