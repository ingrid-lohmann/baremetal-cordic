# ⚙️ baremetal-cordic

**Uma biblioteca matemática C99 unificada para sistemas embarcados sem unidade de ponto flutuante (FPU).**

O **baremetal-cordic** é uma implementação em software de alta fidelidade do algoritmo CORDIC (*Coordinate Rotation Digital Computer*). Projetada estritamente sob o padrão C99, a biblioteca permite o cálculo de funções matemáticas elementares em precisão dupla (`double` - 64 bits) utilizando apenas operações de soma, subtração e deslocamento de bits (*bitshift*). 

Este projeto foi concebido para contornar a ausência de multiplicadores combinacionais em hardware, sendo ideal para microcontroladores de baixo custo, hardwares restritos e modelos de referência para síntese em FPGA.

## 🚀 Principais Características

* **Zero Dependências:** Substitui a `<math.h>` para as funções suportadas. Não requer FPU, instruções FMA (*Fused Multiply-Add*) ou bibliotecas externas.
* **Teoria Unificada:** Baseado na formulação de J. S. Walther, cobrindo os domínios circular e hiperbólico.
* **Rigor IEEE 754:** Manipulação direta da mantissa e do expoente via `union`. Tratamento completo e seguro de casos excepcionais (Infinitos, `NaN` e subnormais) através do módulo `ieee_utils`.
* **Alta Precisão Numérica:** Calibrada estatisticamente para $N = 32$ iterações, garantindo convergência total para a mantissa de 53 bits do tipo `double` (erros na ordem de $10^{-16}$ para raízes e $10^{-10}$ para funções circulares).
* **Funções Suportadas:**
  * **Circulares:** `sin`, `cos`, `tan`, `atan` (com redução periódica de argumento).
  * **Hiperbólicas:** `sinh`, `cosh`, `tanh`, `atanh`.
  * **Transcendentais:** `exp`, `ln`, `sqrt`.

## 🛠️ Requisitos e Integração

Por ser estritamente *bare-metal* e não utilizar alocação dinâmica de memória (`malloc`), a integração é imediata em qualquer compilador aderente ao padrão C99. Basta adicionar os arquivos do diretório `src/` ao *build system* do seu projeto (Makefile, CMake ou IDE de desenvolvimento embarcado).

## 📚 Fundamentação Teórica e Referências

O desenvolvimento desta biblioteca e suas garantias de convergência numérica foram estritamente baseados na literatura clássica e moderna sobre aritmética computacional e no algoritmo CORDIC:

* **Walther, J. S. (1971).** *A Unified Algorithm for Elementary Functions.* A obra definitiva que unificou o CORDIC nos sistemas circular, hiperbólico e linear, cujas equações estruturam a arquitetura principal desta biblioteca.
* **Volder, J. E. (1959).** *The CORDIC Trigonometric Computing Technique.* A publicação original que introduziu o método iterativo para cálculos trigonométricos.
* **Muller, J.-M. (2016).** *Elementary Functions: Algorithms and Implementation (3rd ed.).* Utilizado para a fundamentação da convergência assintótica da raiz quadrada e análise de erro em ponto flutuante.
* **IEEE Std 754-2019.** *IEEE Standard for Floating-Point Arithmetic.* A norma global seguida para o tratamento rigoroso de bits da mantissa, valores excepcionais (`NaN`, $\infty$) e subnormais.
* **Andraka, R. (1998).** *A Survey of CORDIC Algorithms for FPGA Based Computers.* Referência central para as justificativas de implementação de CORDIC em hardwares desprovidos de unidades de multiplicação dedicadas (FPUs).
* **Cody, W. J., & Waite, W. (1980).** *Software Manual for the Elementary Functions.* Base para a estratégia de redução de argumento e tratamento das singularidades nos polos tangenciais.
