import pandas as pd
import matplotlib.pyplot as plt
import os

# Altere para o arquivo que deseja analisar:
# 'cordic_convergence_data_24.csv', 'cordic_convergence_data_26.csv' ou 'cordic_convergence_data_32.csv'
csv_path = 'cordic_convergence_data_32.csv'

df = pd.read_csv(csv_path)
max_n = int(df['N'].max())
base_name = os.path.splitext(os.path.basename(csv_path))[0]
step_ticks = 2  # Espaçamento no eixo X


def configurar_eixos(ax, titulo):
    """Padronização visual dos eixos e legendas."""
    ax.set_title(titulo, fontsize=12, pad=10)
    ax.set_xlabel(r'Número de Iterações ($N$)', fontsize=11)
    ax.set_ylabel(r'Erro Absoluto em Escala Logarítmica (|CORDIC - math.h|)', fontsize=11)
    ax.set_xlim(1, max_n)
    ax.set_xticks(range(1, max_n + 1, step_ticks))
    ax.grid(True, which="both", linestyle=":", alpha=0.6)
    ax.legend(fontsize=9.5, loc='upper right')


fig1, ax1 = plt.subplots(figsize=(9, 5.5), dpi=300)
ax1.semilogy(df['N'], df['Theoretical_Bound'], color='black', linestyle='--', linewidth=1.5, label=r'Limite Teórico Assintótico ($2^{-N}$)')
ax1.semilogy(df['N'], df['Err_Sin_PI_4'], color='#1f77b4', marker='o', markersize=4, linewidth=1.2, label=r'Seno ($\theta = \frac{\pi}{4}$)')
ax1.semilogy(df['N'], df['Err_Cos_PI_4'], color='#ff7f0e', marker='s', markersize=4, linewidth=1.2, label=r'Cosseno ($\theta = \frac{\pi}{4}$)')
ax1.semilogy(df['N'], df['Err_Tan_PI_4'], color='#2ca02c', marker='^', markersize=4, linewidth=1.2, label=r'Tangente ($\theta = \frac{\pi}{4}$)')
configurar_eixos(ax1, f'Convergência das Funções Circulares vs. Limite Teórico (N={max_n})')
fig1.tight_layout()
fig1.savefig(f'{base_name}_circulares.pdf')
fig1.savefig(f'{base_name}_circulares.png')
plt.close(fig1)

fig2, ax2 = plt.subplots(figsize=(9, 5.5), dpi=300)
ax2.semilogy(df['N'], df['Theoretical_Bound'], color='black', linestyle='--', linewidth=1.5, label=r'Limite Teórico Assintótico ($2^{-N}$)')
ax2.semilogy(df['N'], df['Err_Sinh_0_5'], color='#1f77b4', marker='o', markersize=4, linewidth=1.2, label=r'Seno Hiperbólico ($u = 0{,}5$)')
ax2.semilogy(df['N'], df['Err_Cosh_0_5'], color='#ff7f0e', marker='s', markersize=4, linewidth=1.2, label=r'Cosseno Hiperbólico ($u = 0{,}5$)')
ax2.semilogy(df['N'], df['Err_Tanh_0_5'], color='#2ca02c', marker='^', markersize=4, linewidth=1.2, label=r'Tangente Hiperbólica ($u = 0{,}5$)')
configurar_eixos(ax2, f'Convergência das Funções Hiperbólicas vs. Limite Teórico (N={max_n})')
fig2.tight_layout()
fig2.savefig(f'{base_name}_hiperbolicas.pdf')
fig2.savefig(f'{base_name}_hiperbolicas.png')
plt.close(fig2)

fig3, ax3 = plt.subplots(figsize=(9, 5.5), dpi=300)
ax3.semilogy(df['N'], df['Theoretical_Bound'], color='black', linestyle='--', linewidth=1.5, label=r'Limite Teórico Assintótico ($2^{-N}$)')
ax3.semilogy(df['N'], df['Err_Exp_1_0'], color='#1f77b4', marker='o', markersize=4, linewidth=1.2, label=r'Exponencial ($x = 1{,}0$)')
ax3.semilogy(df['N'], df['Err_Ln_2_0'], color='#ff7f0e', marker='s', markersize=4, linewidth=1.2, label=r'Logaritmo Natural ($w = 2{,}0$)')
ax3.semilogy(df['N'], df['Err_Sqrt_2_0'], color='#2ca02c', marker='^', markersize=4, linewidth=1.2, label=r'Raiz Quadrada ($y = 2{,}0$)')
if 'Err_Pow_1_5_1_25' in df.columns:
    ax3.semilogy(df['N'], df['Err_Pow_1_5_1_25'], color='#d62728', marker='d', markersize=4, linewidth=1.2, label=r'Potência ($1{,}5^{1{,}25}$)')
configurar_eixos(ax3, f'Convergência das Funções Transcendentais vs. Limite Teórico (N={max_n})')
fig3.tight_layout()
fig3.savefig(f'{base_name}_transcendentais.pdf')
fig3.savefig(f'{base_name}_transcendentais.png')
plt.close(fig3)


def formatar_notacao_cientifica(val):
    """Converte números em notação científica formatada para o LaTeX com vírgula."""
    if pd.isna(val):
        return "-"
    s = f"{val:.2e}"
    base, exp = s.split('e')
    base = base.replace('.', ',')
    return f"${base} \\times 10^{{{int(exp)}}}$"


if max_n == 24:
    amostras_n = [4, 8, 12, 16, 20, 24]
elif max_n == 26:
    amostras_n = [4, 8, 12, 16, 20, 24, 26]
else:
    amostras_n = [4, 8, 12, 16, 20, 24, 28, 32]

sub_df = df[df['N'].isin(amostras_n)]

tabela_linhas = [
    r"\begin{table}[htbp]",
    r"\centering",
    f"\\caption{{Evolução do erro absoluto das rotinas CORDIC por iteração ($N = {max_n}$)}}",
    f"\\label{{tab:convergencia_{max_n}}}",
    r"\resizebox{\textwidth}{!}{%",
    r"\begin{tabular}{rcccccc}",
    r"\hline",
    r"$N$ & Limite ($2^{-N}$) & $\sin(\frac{\pi}{4})$ & $\cos(\frac{\pi}{4})$ & $\sinh(0{,}5)$ & $\exp(1{,}0)$ & $\sqrt{2{,}0}$ \\",
    r"\hline"
]

for _, r in sub_df.iterrows():
    n = int(r['N'])
    tb = formatar_notacao_cientifica(r['Theoretical_Bound'])
    sin_err = formatar_notacao_cientifica(r['Err_Sin_PI_4'])
    cos_err = formatar_notacao_cientifica(r['Err_Cos_PI_4'])
    sinh_err = formatar_notacao_cientifica(r['Err_Sinh_0_5'])
    exp_err = formatar_notacao_cientifica(r['Err_Exp_1_0'])
    sqrt_err = formatar_notacao_cientifica(r['Err_Sqrt_2_0'])
    tabela_linhas.append(f"{n} & {tb} & {sin_err} & {cos_err} & {sinh_err} & {exp_err} & {sqrt_err} \\\\")

tabela_linhas.extend([
    r"\hline",
    r"\end{tabular}%",
    r"}",
    r"\end{table}"
])

nome_arquivo_tex = f'tabela_convergencia_{max_n}.tex'
with open(nome_arquivo_tex, 'w', encoding='utf-8') as f:
    f.write("\n".join(tabela_linhas))

print(f"Gráficos e tabela salvos com sucesso:")
print(f" - {base_name}_circulares.pdf / .png")
print(f" - {base_name}_hiperbolicas.pdf / .png")
print(f" - {base_name}_transcendentais.pdf / .png")
print(f" - {nome_arquivo_tex}")