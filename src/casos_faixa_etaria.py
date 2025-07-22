#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# %%

df = pd.read_csv('../data/faixa_etaria.csv'
                 ,encoding='latin1'
                 , sep=';'
                 , skiprows=3, skipfooter=18)
df.head()

#%%

df.rename(columns={'Ano Diagnóstico' : 'ano_diagnostico', '0 a 14 anos' : '0-14', '15 anos e mais' : '15 ou mais' }, inplace=True)

#%%

# Filtragem

df = (
    df[df['ano_diagnostico'] != '<1975']
      .drop(columns=['IGN', 'Total'])
      .replace('-', 0)
)

#%%

df_long = df.melt(id_vars='ano_diagnostico', 
                  var_name='idade', 
                  value_name='casos')

# converter os casos para tipo numérico
df_long['casos'] = pd.to_numeric(df_long['casos'], errors='coerce')


# agrupar e somar os casos

df_total = df_long.groupby('idade')['casos'].sum().reset_index()

#%%

plt.figure(figsize=(15,6))
sns.barplot(data=df_total, x='idade', y='casos', palette='Reds_r')

plt.title('TOTAL DE CASOS POR FAIXA ETÁRIA DE 1975 A 2025', pad=20)
plt.xlabel('Idade', labelpad=15)
plt.ylabel('Total de Casos', labelpad=15)

plt.savefig('total_casos_faixa_etaria.png')

#%%

df_long = df_long.sort_values(by='ano_diagnostico', ascending=True)

df_long

#%%

plt.figure(figsize=(12, 6))

sns.lineplot(data=df, x='ano_diagnostico', y='0-14', color='royalblue')

plt.title('Casos de Hanseníase – Faixa Etária: 0 a 14 anos (Brasil)', fontsize=14, pad=20)
plt.xlabel('Ano do Diagnóstico', fontsize=12)
plt.ylabel('Número de Casos (0 a 14 anos)', fontsize=12)

# Pular anos de 5 em 5 no eixo X
import matplotlib.ticker as ticker
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))

plt.grid(True)
plt.tight_layout()
plt.gca().invert_yaxis()

plt.savefig('casos_0a14_anos.png', dpi=300)

#%%

plt.figure(figsize=(12, 6))

sns.lineplot(data=df, x='ano_diagnostico', y='15 ou mais', color='royalblue')

plt.title('Casos de Hanseníase – Faixa Etária: 15 anos ou mais (Brasil)', fontsize=14, pad=20)
plt.xlabel('Ano do Diagnóstico', fontsize=12)
plt.ylabel('Número de Casos (15 anos ou mais)', fontsize=12)

# Pular anos de 5 em 5 no eixo X
import matplotlib.ticker as ticker
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))

plt.grid(True)
plt.tight_layout()

plt.savefig('casos_15mais_anos.png', dpi=300)