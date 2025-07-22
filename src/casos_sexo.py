#%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# %%

df = pd.read_csv('../data/sexo.csv', encoding='latin1', sep=';', skiprows=3, skipfooter=18, engine='python')
df.tail()

#%%

df.rename(columns={'Ano Diagnóstico' : 'ano_diagnostico', 'Masculino' : 'masculino', 'Feminino' : 'feminino'}, inplace=True)

# %%

df = (
    df[df['ano_diagnostico'] != '<1975']
      .drop(columns=['Ignorado', 'Total'])
      .replace('-', 0)
)

#%%

df_long = pd.melt(
    df,
    id_vars=['ano_diagnostico'],
    value_vars=['masculino', 'feminino'],
    var_name='sexo',
    value_name='casos'
)

df_long.head()

# %%

totais = df_long.groupby('sexo')['casos'].sum().reset_index()

#%%

plt.figure(figsize=(15,6))
sns.barplot(data=totais, x='sexo', y='casos', color='royalblue')

plt.title('Número total de casos por sexo', pad=10, color='grey')
plt.xlabel('Sexo', labelpad=10, color='grey')
plt.ylabel('Total de casos', labelpad=10, color='grey')

plt.tight_layout()

plt.savefig('casos_sexo.png')