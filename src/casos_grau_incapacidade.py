#%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# %%

df = pd.read_csv('../data/graus_incapacidade.csv', encoding='latin1', sep=';', skiprows=3, skipfooter=18)

#%%

df.rename(columns={'Ano Diagnóstico' : 'ano_diagnostico', 'GRAU ZERO' : 'grau_0', 'GRAU I' : 'grau_1', 'GRAU II' : 'grau_2'}, inplace=True)

#%%

# Filtragem

df = (
    df[df['ano_diagnostico'] != '<1975']
      .drop(columns=['Em Branco', 'Não AVALIADO', 'Total'])
      .replace('-', 0)
)

#%%

#%%

df_long = df.melt(id_vars='ano_diagnostico', 
                  var_name='grau_incapacidade', 
                  value_name='casos')

# converter os casos para tipo numérico
df_long['casos'] = pd.to_numeric(df_long['casos'], errors='coerce')

# agrupar e somar os casos

df_total = df_long.groupby('grau_incapacidade')['casos'].sum().reset_index()


#%%

plt.figure(figsize=(15,6))
sns.barplot(data=df_total, x='grau_incapacidade', y='casos', palette='Reds_r')

plt.title('TOTAL DE CASOS POR GRAU DE INCAPACIDADE DE 1975 A 2025', pad=20)
plt.xlabel('Grau de Incapacidade', labelpad=15)
plt.ylabel('Total de Casos', labelpad=15)

plt.savefig('total_casos_grau_incapacidade.png')

#%%

plt.figure(figsize=(14, 6))

sns.lineplot(
    data=df_long,
    x='ano_diagnostico',
    y='casos',
    hue='grau_incapacidade',
    palette='Set1'
)

plt.title('Casos de Hanseníase por Grau de Incapacidade ao Diagnóstico', fontsize=14, pad=20)
plt.xlabel('Ano de Diagnóstico', fontsize=12, labelpad=15)
plt.ylabel('Número de Casos', fontsize=12, labelpad=15)
plt.legend(title='Grau de Incapacidade')
plt.grid(True)

# Eixo X com anos de 5 em 5
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(5))

plt.tight_layout()
plt.savefig('grau_incapacidade_por_ano.png', dpi=300)