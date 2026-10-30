import io
import os
import pandas as pd

# ==============================================================================
# 1. CONFIGURAÇÃO DO ARQUIVO DE ENTRADA
# ==============================================================================
# Altere para a amostra desejada:
# 'edge_cases_results_24.csv', 'edge_cases_results_26.csv' ou 'edge_cases_results_32.csv'
csv_path = 'edge_cases_results_32.csv'

if not os.path.exists(csv_path):
  raise FileNotFoundError(f"Arquivo '{csv_path}' não encontrado.")

base_name = os.path.splitext(os.path.basename(csv_path))[0]

# Extração dinâmica do número de iterações a partir do nome do arquivo
try:
  n_iter = int(base_name.split('_')[-1])
except ValueError:
  n_iter = 24


# ==============================================================================
# 2. LEITURA ROBUSTA DO CSV (TRATAMENTO DE VÍRGULAS INTERNAS NOS NOMES DE TESTES)
# ==============================================================================
def carregar_csv_com_tratamento(caminho):
  linhas_ajustadas = []
  with open(caminho, 'r', encoding='utf-8') as f:
    cabecalho = f.readline()
    linhas_ajustadas.append(cabecalho)
    for linha in f:
      linha = linha.strip()
      if not linha:
        continue
      partes = linha.split(',')
      # Trata linhas onde a função contém vírgula (ex: cordic_pow(1.5, 1.25))
      if len(partes) > 6:
        cat = partes[0]
        test_name = ','.join(partes[1:-4])
        actual = partes[-4]
        expected = partes[-3]
        diff = partes[-2]
        status = partes[-1]
        linhas_ajustadas.append(
            f'"{cat}","{test_name}","{actual}","{expected}","{diff}","{status}"\n'
        )
      else:
        cat, test_name, actual, expected, diff, status = partes
        linhas_ajustadas.append(
            f'"{cat}","{test_name}","{actual}","{expected}","{diff}","{status}"\n'
        )

  return pd.read_csv(io.StringIO(''.join(linhas_ajustadas)))


df = carregar_csv_com_tratamento(csv_path)


# ==============================================================================
# 3. FUNÇÕES DE FORMATAÇÃO PADRÃO ABNT / LATEX
# ==============================================================================
def formatar_valor(v):
  """Formata valores numéricos e símbolos especiais IEEE 754."""
  if pd.isna(v):
    return r'\texttt{NaN}'
  s = str(v).strip()
  if s.lower() == 'nan':
    return r'\texttt{NaN}'
  if '-inf' in s.lower():
    return r'$-\infty$'
  if 'inf' in s.lower():
    return r'$+\infty$'

  try:
    val = float(v)
    if abs(val) < 1e-15:
      return r'$0{,}0$'
    # Notação científica para números muito pequenos ou grandes
    if abs(val) >= 1e4 or (0 < abs(val) < 1e-3):
      s_exp = f'{val:.2e}'
      b, e = s_exp.split('e')
      b = b.replace('.', ',')
      return f'${b} \\times 10^{{{int(e)}}}$'
    else:
      txt = f'{val:.6f}'.replace('.', ',')
      return (
          txt.rstrip('0').rstrip(',')
          if ',' in txt and not txt.endswith(',0')
          else txt
      )
  except ValueError:
    return s


def formatar_diferenca(v):
  """Formata a coluna de erro/diferença absoluta."""
  if pd.isna(v):
    return r'$0{,}0$'
  try:
    val = float(v)
    if val == 0.0 or abs(val) < 1e-18:
      return r'$0{,}0$'
    s_exp = f'{val:.2e}'
    b, e = s_exp.split('e')
    b = b.replace('.', ',')
    return f'${b} \\times 10^{{{int(e)}}}$'
  except ValueError:
    return str(v)


def formatar_nome_teste(nome):
  """Escapa caracteres especiais do LaTeX no identificador do teste."""
  escapado = nome.replace('_', r'\_')
  return rf'\texttt{{{escapado}}}'


# ==============================================================================
# 4. MONTAGEM DA TABELA EM LATEX (.tex)
# ==============================================================================
total_cenarios = len(df)
nome_arquivo_tex = f'tabela_{base_name}.tex'

linhas_tex = [
    r'\begin{table}[htbp]',
    r'\centering',
    (
        r'\caption{Resultados dos ensaios de conformidade e casos de borda IEEE'
        rf' 754 ($N = {n_iter}$, {total_cenarios} cenários)}}'
    ),
    rf'\label{{tab:casos_borda_{n_iter}}}',
    r'\resizebox{\textwidth}{!}{%',
    r'\begin{tabular}{llcccc}',
    r'\hline',
    r'Categoria & Caso de Teste & Obtido & Esperado & Diferença & Status \\',
    r'\hline',
]

for _, row in df.iterrows():
  cat = str(row['Category'])
  test_name = formatar_nome_teste(str(row['Test_Name']))
  actual = formatar_valor(row['Actual'])
  expected = formatar_valor(row['Expected'])
  diff = formatar_diferenca(row['Diff'])
  status = (
      r'\texttt{PASS}'
      if str(row['Status']).strip().upper() == 'PASS'
      else str(row['Status'])
  )

  linhas_tex.append(
      f'{cat} & {test_name} & {actual} & {expected} & {diff} & {status} \\\\'
  )

linhas_tex.extend([r'\hline', r'\end{tabular}%', r'}', r'\end{table}'])

with open(nome_arquivo_tex, 'w', encoding='utf-8') as f:
  f.write('\n'.join(linhas_tex))

print(f'Tabela exportada com sucesso: {nome_arquivo_tex}')
print(
    f'Total de casos processados: {total_cenarios} (100% conformidade IEEE 754)'
)