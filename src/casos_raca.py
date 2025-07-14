#%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# %%

df = pd.read_csv('../data/raça.csv', skiprows=3, skipfooter=18, sep=';', encoding='latin1', engine='python')
df.tail()

#%%

df.rename(columns={'Ano Diagnóstico' : 'ano_diagnostico', 'Branca' : 'branca', 'Preta' : 'preta', 'Amarela' : 'amarela', 'Parda' : 'parda', 'Indigena' : 'indigena'}, inplace=True)

#%%

df = (df[df['ano_diagnostico'] != '<1975'].drop(columns=['Ign/Branco', 'Total']).replace('-', 0))

#%%

df_long = pd.melt(
    df,
    id_vars=['ano_diagnostico'],
    value_vars=['branca', 'preta', 'amarela', 'parda', 'indigena'],
    var_name='raca',
    value_name='casos'
)


#%%

# converter os casos para tipo numérico
df_long['casos'] = pd.to_numeric(df_long['casos'], errors='coerce')

#%%

total_por_raca = df_long.groupby('raca')['casos'].sum().reset_index()
total_por_raca = total_por_raca.sort_values(by='casos', ascending=False)

df.to_csv('total_por_raca.csv')

print(total_por_raca)

#%%

plt.figure(figsize=(15,6))
sns.barplot(data=total_por_raca, x='raca', y='casos', color='royalblue')

plt.title('Número total de casos por raca', pad=10, color='grey')
plt.xlabel('Raça', labelpad=10, color='grey')
plt.ylabel('Total de casos', labelpad=10, color='grey')

plt.tight_layout()

plt.savefig('casos_raca.png')