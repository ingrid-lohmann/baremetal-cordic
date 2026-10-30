import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ==============================================================================
# 1. CONFIGURAÇÃO DO ARQUIVO DE ENTRADA
# ==============================================================================
# Altere para a rodada desejada:
# 'benchmark_results_24.csv', 'benchmark_results_26.csv' ou 'benchmark_results_32.csv'
csv_path = 'benchmark_results_32.csv'

if not os.path.exists(csv_path):
  raise FileNotFoundError(f"Arquivo '{csv_path}' não encontrado.")

df = pd.read_csv(csv_path)
base_name = os.path.splitext(os.path.basename(csv_path))[0]

# Mapeamento de rótulos matemáticos para os gráficos
display_names = {
    'sin_cos': r'$\sin + \cos$',
    'tan': r'$\tan$',
    'atan': r'$\arctan$',
    'sinh_cosh': r'$\sinh + \cosh$',
    'tanh': r'$\tanh$',
    'atanh': r'$\mathrm{artanh}$',
    'exp': r'$\exp$',
    'ln': r'$\ln$',
    'sqrt': r'$\sqrt{x}$',
    'pow': r'$x^y$',
}

# Grupos de funções para os gráficos específicos
grupos = {
    'circulares': ['sin_cos', 'tan', 'atan'],
    'hiperbolicas': ['sinh_cosh', 'tanh', 'atanh'],
    'transcendentais': ['exp', 'ln', 'sqrt', 'pow'],
}


# ==============================================================================
# 2. FUNÇÃO AUXILIAR PARA PLOTAGEM DE BARRAS AGRUPADAS (POR CATEGORIA)
# ==============================================================================
def plot_grupo(df_bench, ops, titulo, sufixo_saida):
  labels = [display_names[op] for op in ops]
  cordic_lats = []
  math_lats = []
  slowdowns = []

  for op in ops:
    c_row = df_bench[
        (df_bench['Operation'] == op) & (df_bench['Implementation'] == 'CORDIC')
    ]
    m_row = df_bench[
        (df_bench['Operation'] == op) & (df_bench['Implementation'] == 'math.h')
    ]

    cordic_lats.append(c_row.iloc[0]['Latency_ns_op'])
    math_lats.append(m_row.iloc[0]['Latency_ns_op'])
    slowdowns.append(c_row.iloc[0]['Slowdown_vs_math'])

  x = np.arange(len(labels))
  largura = 0.35

  fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)
  rects1 = ax.bar(
      x - largura / 2,
      cordic_lats,
      largura,
      label='CORDIC (Software)',
      color='#1f77b4',
      edgecolor='black',
      linewidth=0.8,
  )
  rects2 = ax.bar(
      x + largura / 2,
      math_lats,
      largura,
      label='math.h (Hardware FPU)',
      color='#7f7f7f',
      edgecolor='black',
      linewidth=0.8,
  )

  ax.set_title(titulo, fontsize=12, pad=12)
  ax.set_ylabel('Latência Média por Operação (ns)', fontsize=11)
  ax.set_xticks(x)
  ax.set_xticklabels(labels, fontsize=11)
  ax.legend(fontsize=9.5, loc='upper left')
  ax.grid(axis='y', linestyle=':', alpha=0.6)

  limite_y = max(max(cordic_lats), max(math_lats))
  ax.set_ylim(0, limite_y * 1.25)

  # Anotação com latência e multiplicador de sobrecarga
  for i, rect in enumerate(rects1):
    h = rect.get_height()
    ax.text(
        rect.get_x() + rect.get_width() / 2.0,
        h,
        f'{h:.1f} ns\n({slowdowns[i]:.1f}x)',
        ha='center',
        va='bottom',
        fontsize=8.5,
        fontweight='bold',
        color='#1f77b4',
    )

  for rect in rects2:
    h = rect.get_height()
    ax.text(
        rect.get_x() + rect.get_width() / 2.0,
        h,
        f'{h:.1f} ns\n(ref)',
        ha='center',
        va='bottom',
        fontsize=8.5,
        color='#444444',
    )

  fig.tight_layout()
  fig.savefig(f'{base_name}_{sufixo_saida}.pdf')
  fig.savefig(f'{base_name}_{sufixo_saida}.png')
  plt.close(fig)


# ==============================================================================
# 3. GERAÇÃO DOS TRÊS GRÁFICOS POR CATEGORIA
# ==============================================================================
plot_grupo(
    df,
    grupos['circulares'],
    'Comparativo de Latência: Funções Circulares (CORDIC vs. math.h)',
    'circulares',
)
plot_grupo(
    df,
    grupos['hiperbolicas'],
    'Comparativo de Latência: Funções Hiperbólicas (CORDIC vs. math.h)',
    'hiperbolicas',
)
plot_grupo(
    df,
    grupos['transcendentais'],
    'Comparativo de Latência: Funções Transcendentais (CORDIC vs. math.h)',
    'transcendentais',
)


# ==============================================================================
# 4. GRÁFICO GERAL PANORÂMICO (BARRAS HORIZONTAIS COM TODAS AS OPERAÇÕES)
# ==============================================================================
todas_ops = [
    'sin_cos',
    'tan',
    'atan',
    'sinh_cosh',
    'tanh',
    'atanh',
    'exp',
    'ln',
    'sqrt',
    'pow',
]
labels_todas = [display_names[op] for op in todas_ops]
c_todas = []
m_todas = []
slow_todas = []

for op in todas_ops:
  c = df[(df['Operation'] == op) & (df['Implementation'] == 'CORDIC')].iloc[0]
  m = df[(df['Operation'] == op) & (df['Implementation'] == 'math.h')].iloc[0]
  c_todas.append(c['Latency_ns_op'])
  m_todas.append(m['Latency_ns_op'])
  slow_todas.append(c['Slowdown_vs_math'])

y = np.arange(len(labels_todas))
altura = 0.38

fig_pan, ax_pan = plt.subplots(figsize=(10, 6.8), dpi=300)
b1 = ax_pan.barh(
    y + altura / 2,
    c_todas,
    altura,
    label='CORDIC (Software)',
    color='#1f77b4',
    edgecolor='black',
    linewidth=0.8,
)
b2 = ax_pan.barh(
    y - altura / 2,
    m_todas,
    altura,
    label='math.h (Hardware FPU)',
    color='#7f7f7f',
    edgecolor='black',
    linewidth=0.8,
)

ax_pan.set_title(
    'Visão Panorâmica de Latência por Operação ($10^6$ Amostras)',
    fontsize=12,
    pad=12,
)
ax_pan.set_xlabel('Latência Média por Operação (ns)', fontsize=11)
ax_pan.set_yticks(y)
ax_pan.set_yticklabels(labels_todas, fontsize=11)
ax_pan.invert_yaxis()
ax_pan.legend(fontsize=10, loc='upper right')
ax_pan.grid(axis='x', linestyle=':', alpha=0.6)

max_lat = max(c_todas)
ax_pan.set_xlim(0, max_lat * 1.30)

for i, rect in enumerate(b1):
  w = rect.get_width()
  ax_pan.text(
      w + max_lat * 0.015,
      rect.get_y() + rect.get_height() / 2.0,
      f'{w:.1f} ns ({slow_todas[i]:.1f}x)',
      va='center',
      ha='left',
      fontsize=8.5,
      fontweight='bold',
      color='#1f77b4',
  )

for rect in b2:
  w = rect.get_width()
  ax_pan.text(
      w + max_lat * 0.015,
      rect.get_y() + rect.get_height() / 2.0,
      f'{w:.1f} ns (ref)',
      va='center',
      ha='left',
      fontsize=8,
      color='#444444',
  )

fig_pan.tight_layout()
fig_pan.savefig(f'{base_name}_panoramico.pdf')
fig_pan.savefig(f'{base_name}_panoramico.png')
plt.close(fig_pan)


# ==============================================================================
# 5. EXPORTAÇÃO DA TABELA FORMATADA PARA LATEX (.tex)
# ==============================================================================
nomes_latex = {
    'circular_rotate': r'Rotação Circular (\texttt{rotate})',
    'circular_vector': r'Vetorização Circular (\texttt{vector})',
    'sin_cos': r'Seno e Cosseno ($\sin + \cos$)',
    'tan': r'Tangente ($\tan$)',
    'atan': r'Arco Tangente ($\arctan$)',
    'hyperbolic_rotate': r'Rotação Hiperbólica (\texttt{rotate})',
    'hyperbolic_vector': r'Vetorização Hiperbólica (\texttt{vector})',
    'sinh_cosh': r'Seno e Cosseno Hip. ($\sinh + \cosh$)',
    'tanh': r'Tangente Hiperbólica ($\tanh$)',
    'atanh': r'Arco Tangente Hip. ($\mathrm{artanh}$)',
    'exp': r'Exponencial ($\exp$)',
    'ln': r'Logaritmo Natural ($\ln$)',
    'sqrt': r'Raiz Quadrada ($\sqrt{x}$)',
    'pow': r'Potenciação ($x^y$)',
}

linhas_tex = [
    r'\begin{table}[htbp]',
    r'\centering',
    (
        f'\\caption{{Desempenho temporal e latência média das rotinas CORDIC'
        r' frente à \texttt{math.h} ($10^6$ amostras)}}'
    ),
    f'\\label{{tab:{base_name}}}',
    r'\resizebox{\textwidth}{!}{%',
    r'\begin{tabular}{llcccc}',
    r'\hline',
    (
        r'Operação & Implementação & Tempo Total (s) & Latência (ns/op) &'
        r' Ciclos/op & \textit{Slowdown} \\'
    ),
    r'\hline',
]

for _, row in df.iterrows():
  op = row['Operation']
  op_desc = nomes_latex.get(op, op)
  impl = 'CORDIC' if row['Implementation'] == 'CORDIC' else r'\texttt{math.h}'
  t_tot = f"{row['Total_Time_s']:.4f}".replace('.', ',')
  lat = f"{row['Latency_ns_op']:.2f}".replace('.', ',')
  cyc = f"{row['Cycles_op']:.2f}".replace('.', ',')

  if pd.isna(row['Slowdown_vs_math']):
    slow = '-'
  elif row['Slowdown_vs_math'] == 1.0:
    slow = r'1{,}00$\times$ (ref)'
  else:
    slow = f"{row['Slowdown_vs_math']:.2f}\\times$".replace('.', ',')
    slow = f'${slow}'

  linhas_tex.append(
      f'{op_desc} & {impl} & {t_tot} & {lat} & {cyc} & {slow} \\\\'
  )

linhas_tex.extend(
    [r'\hline', r'\end{tabular}%', r'}', r'\end{table}']
)

tex_filename = f'tabela_{base_name}.tex'
with open(tex_filename, 'w', encoding='utf-8') as f:
  f.write('\n'.join(linhas_tex))

print(f'Geração concluída com sucesso para {csv_path}:')
print(f' - {base_name}_circulares.pdf / .png')
print(f' - {base_name}_hiperbolicas.pdf / .png')
print(f' - {base_name}_transcendentais.pdf / .png')
print(f' - {base_name}_panoramico.pdf / .png')
print(f' - {tex_filename}')