import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ==============================================================================
# 1. CONFIGURAÇÃO DO ARQUIVO DE ENTRADA
# ==============================================================================
# Altere para a amostra desejada:
# 'stress_test_domain_24.csv', 'stress_test_domain_26.csv' ou 'stress_test_domain_32.csv'
csv_path = 'stress_test_domain_32.csv'

if not os.path.exists(csv_path):
  raise FileNotFoundError(f"Arquivo '{csv_path}' não encontrado.")

df = pd.read_csv(csv_path)
base_name = os.path.splitext(os.path.basename(csv_path))[0]

# Extração dinâmica do número de iterações a partir do nome do arquivo
try:
  n_iter = int(base_name.split('_')[-1])
except ValueError:
  n_iter = 24

# Conversão do domínio de radianos para graus
x_deg = df['Angle_Rad'] * (180.0 / np.pi)
piso_teorico = 2.0 ** (-n_iter)


# ==============================================================================
# 2. GRÁFICO 1: SENO E COSSENO (FOCO NO PISO TEÓRICO)
# ==============================================================================
fig1, ax1 = plt.subplots(figsize=(9, 5.2), dpi=300)

ax1.axhline(
    y=piso_teorico,
    color='black',
    linestyle='--',
    linewidth=1.5,
    label=rf'Limite Teórico Assintótico ($2^{{-{n_iter}}}$)',
)

ax1.semilogy(
    x_deg,
    df['Sin_AbsErr'],
    color='#1f77b4',
    linewidth=1.4,
    label=r'Erro Absoluto Seno ($|\sin_{\mathrm{CORDIC}} - \sin_{\mathrm{math}}|$)',
)

ax1.semilogy(
    x_deg,
    df['Cos_AbsErr'],
    color='#ff7f0e',
    linewidth=1.4,
    label=(
        r'Erro Absoluto Cosseno ($|\cos_{\mathrm{CORDIC}} -'
        r' \cos_{\mathrm{math}}|$)'
    ),
)

ax1.set_title(
    rf'Distribuição do Erro: Seno e Cosseno no 1º Quadrante ($N = {n_iter}$)',
    fontsize=12,
    pad=12,
)
ax1.set_xlabel(r'Ângulo de Entrada $\theta$ (Graus)', fontsize=11)
ax1.set_ylabel('Erro Absoluto em Escala Logarítmica', fontsize=11)
ax1.set_xlim(0, 90)
ax1.set_xticks(np.arange(0, 91, 15))
ax1.grid(True, which='both', linestyle=':', alpha=0.6)
ax1.legend(loc='lower right', fontsize=9.5)
fig1.tight_layout()

fig1.savefig(f'{base_name}_sen_cos.pdf')
fig1.savefig(f'{base_name}_sen_cos.png')
plt.close(fig1)


# ==============================================================================
# 3. GRÁFICO 2: TANGENTE (TRANSIÇÃO DE OCTANTE E COMPORTAMENTO ASSINTÓTICO)
# ==============================================================================
fig2, ax2 = plt.subplots(figsize=(9, 5.2), dpi=300)

ax2.semilogy(
    x_deg,
    df['Tan_AbsErr'],
    color='#2ca02c',
    linewidth=1.4,
    label=(
        r'Erro Absoluto Tangente ($|\tan_{\mathrm{CORDIC}} -'
        r' \tan_{\mathrm{math}}| $)'
    ),
)

ax2.axvline(
    x=45.0,
    color='gray',
    linestyle=':',
    linewidth=1.3,
    label=r'Transição de Octante ($\theta = 45^{\circ}$)',
)

ax2.set_title(
    r'Distribuição do Erro da Tangente com Redução por Octantes ($N ='
    rf' {n_iter}$)',
    fontsize=12,
    pad=12,
)
ax2.set_xlabel(r'Ângulo de Entrada $\theta$ (Graus)', fontsize=11)
ax2.set_ylabel('Erro Absoluto em Escala Logarítmica', fontsize=11)
ax2.set_xlim(0, 90)
ax2.set_xticks(np.arange(0, 91, 15))
ax2.grid(True, which='both', linestyle=':', alpha=0.6)
ax2.legend(loc='upper left', fontsize=9.5)
fig2.tight_layout()

fig2.savefig(f'{base_name}_tangente.pdf')
fig2.savefig(f'{base_name}_tangente.png')
plt.close(fig2)


# ==============================================================================
# 4. GRÁFICO 3: VISÃO PANORÂMICA (SENO, COSSENO E TANGENTE INTEGRADOS)
# ==============================================================================
fig3, ax3 = plt.subplots(figsize=(9, 5.2), dpi=300)

ax3.axhline(
    y=piso_teorico,
    color='black',
    linestyle='--',
    linewidth=1.5,
    label=rf'Limite Teórico ($2^{{-{n_iter}}}$)',
)

ax3.semilogy(
    x_deg,
    df['Sin_AbsErr'],
    color='#1f77b4',
    linewidth=1.2,
    label=r'Seno ($\sin\theta$)',
)
ax3.semilogy(
    x_deg,
    df['Cos_AbsErr'],
    color='#ff7f0e',
    linewidth=1.2,
    label=r'Cosseno ($\cos\theta$)',
)
ax3.semilogy(
    x_deg,
    df['Tan_AbsErr'],
    color='#2ca02c',
    linewidth=1.2,
    label=r'Tangente ($\tan\theta$)',
)

ax3.set_title(
    rf'Estabilidade Numérica no 1º Quadrante: Circulares Integradas ($N ='
    rf' {n_iter}$)',
    fontsize=12,
    pad=12,
)
ax3.set_xlabel(r'Ângulo de Entrada $\theta$ (Graus)', fontsize=11)
ax3.set_ylabel('Erro Absoluto em Escala Logarítmica', fontsize=11)
ax3.set_xlim(0, 90)
ax3.set_xticks(np.arange(0, 91, 15))
ax3.grid(True, which='both', linestyle=':', alpha=0.6)
ax3.legend(loc='lower right', fontsize=9.5)
fig3.tight_layout()

fig3.savefig(f'{base_name}_integrado.pdf')
fig3.savefig(f'{base_name}_integrado.png')
plt.close(fig3)


# ==============================================================================
# 5. EXPORTAÇÃO DA TABELA ESTATÍSTICA FORMATADA PARA LATEX (.tex)
# ==============================================================================
def formatar_notacao(v):
  s = f'{v:.2e}'
  b, e = s.split('e')
  b = b.replace('.', ',')
  return f'${b} \\times 10^{{{int(e)}}}$'


linhas_tex = [
    r'\begin{table}[htbp]',
    r'\centering',
    (
        r'\caption{Estatísticas descritivas de erro absoluto no primeiro'
        rf' quadrante ($N = {n_iter}$, 315 amostras)}}'
    ),
    rf'\label{{tab:estatistica_{n_iter}}}',
    r'\begin{tabular}{lcccc}',
    r'\hline',
    r'Função & Mínimo & Máximo & Média & Desvio Padrão \\',
    r'\hline',
]

descricoes = {
    'Sin_AbsErr': r'Seno ($\sin\theta$)',
    'Cos_AbsErr': r'Cosseno ($\cos\theta$)',
    'Tan_AbsErr': r'Tangente ($\tan\theta$)',
}

for col in ['Sin_AbsErr', 'Cos_AbsErr', 'Tan_AbsErr']:
  rotulo = descricoes[col]
  v_min = formatar_notacao(df[col].min())
  v_max = formatar_notacao(df[col].max())
  v_med = formatar_notacao(df[col].mean())
  v_std = formatar_notacao(df[col].std())
  linhas_tex.append(f'{rotulo} & {v_min} & {v_max} & {v_med} & {v_std} \\\\')

linhas_tex.extend([r'\hline', r'\end{tabular}', r'\end{table}'])

arquivo_tex = f'tabela_estatistica_{n_iter}.tex'
with open(arquivo_tex, 'w', encoding='utf-8') as f:
  f.write('\n'.join(linhas_tex))

print(f'Geração concluída para {csv_path}:')
print(f' - {base_name}_sen_cos.pdf / .png')
print(f' - {base_name}_tangente.pdf / .png')
print(f' - {base_name}_integrado.pdf / .png')
print(f' - {arquivo_tex}')