#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

#include "ieee_utils.h"
#include "cordic_circular.h"
#include "cordic_hyperbolic.h"
#include "cordic_transcendental.h"

#define DEFAULT_ITERATIONS CORDIC_ITERATIONS

static void print_usage(const char *program_name, FILE *stream) {
    fprintf(stream, "Uso: %s [--iterations N]\n", program_name);
    fprintf(stream, "     %s --help\n", program_name);
    fprintf(stream, "  -n, --iterations N  Numero de iteracoes (1 a %d)\n", CORDIC_ITERATIONS);
    fprintf(stream, "  -h, --help          Mostra esta ajuda\n");
}

static int parse_arguments(int argc, char *argv[], int *iterations) {
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            return 1;
        }

        if (strcmp(argv[i], "--iterations") == 0 || strcmp(argv[i], "-n") == 0) {
            if (i + 1 >= argc) {
                return -1;
            }

            char *end = NULL;
            long value = strtol(argv[++i], &end, 10);
            if (end == argv[i] || *end != '\0' || value < 1 || value > CORDIC_ITERATIONS) {
                return -1;
            }

            *iterations = (int)value;
            continue;
        }

        return -1;
    }

    return 0;
}

static void print_comparison(const char *func_name, double input, double cordic_val, double math_val) {
    double error = fabs(cordic_val - math_val);
    printf("%-10s | in: %8.4f | CORDIC: %15.10f | math.h: %15.10f | Err: %1.2e\n",
           func_name, input, cordic_val, math_val, error);
}

int main(int argc, char *argv[]) {
    int iterations = DEFAULT_ITERATIONS;
    int argument_status = parse_arguments(argc, argv, &iterations);
    if (argument_status == 1) {
        print_usage(argv[0], stdout);
        return 0;
    }
    if (argument_status < 0) {
        print_usage(argv[0], stderr);
        return 2;
    }

    printf("****************************************************************************************\n");
    printf("                  BANCADA DE TESTES: FUNCOES TRANSCENDENTAIS CORDIC                      \n");
    printf("                  Iteracoes: %d | Formato: IEEE 754 64-bit (Double)                    \n", iterations);
    printf("****************************************************************************************\n\n");

    /* 1. Modulo Circular (Trigonometricas) */
    printf("--- [1] Funcoes Circulares (Trigonometricas) ---\n");
    double angles[] = {0.0, PI / 6.0, PI / 4.0, PI / 3.0};
    int num_angles = sizeof(angles) / sizeof(angles[0]);

    for (int i = 0; i < num_angles; i++) {
        double theta = angles[i];
        double sin_c, cos_c;
        cordic_circular_sin_cos(theta, &sin_c, &cos_c, iterations);

        print_comparison("sin(x)", theta, sin_c, sin(theta));
        print_comparison("cos(x)", theta, cos_c, cos(theta));
        print_comparison("tan(x)", theta, cordic_circular_tan(theta, iterations), tan(theta));
        printf("****************************************************************************************\n");
    }

    double tan_values[] = {0.0, 0.577350269, 1.0, 1.732050807};
    for (int i = 0; i < 4; i++) {
        double v = tan_values[i];
        print_comparison("atan(x)", v, cordic_circular_atan(v, iterations), atan(v));
    }
    printf("\n");

    /* 2. Modulo Hiperbolico */
    printf("--- [2] Funcoes Hiperbolicas ---\n");
    double hyp_inputs[] = {0.0, 0.5, 0.8, 1.0};
    for (int i = 0; i < 4; i++) {
        double u = hyp_inputs[i];
        double sinh_c, cosh_c;
        cordic_hyperbolic_sinh_cosh(u, &sinh_c, &cosh_c, iterations);

        print_comparison("sinh(x)", u, sinh_c, sinh(u));
        print_comparison("cosh(x)", u, cosh_c, cosh(u));
        print_comparison("tanh(x)", u, cordic_hyperbolic_tanh(u, iterations), tanh(u));
        printf("****************************************************************************************\n");
    }

    double atanh_inputs[] = {0.0, 0.2, 0.5, 0.75};
    for (int i = 0; i < 4; i++) {
        double v = atanh_inputs[i];
        print_comparison("atanh(x)", v, cordic_hyperbolic_atanh(v, iterations), atanh(v));
    }
    printf("\n");

    /* 3. Modulo Transcendental Composto (exp, ln, sqrt, pow) */
    printf("--- [3] Funcoes Compostas (Exponencial, Logaritmo, Raiz, Potencia) ---\n");
    double exp_inputs[] = {0.2, 0.5, 1.0};
    for (int i = 0; i < 3; i++) {
        double x = exp_inputs[i];
        print_comparison("exp(x)", x, cordic_exp(x, iterations), exp(x));
    }

    double ln_inputs[] = {0.5, 1.0, 2.0, 5.0};
    for (int i = 0; i < 4; i++) {
        double x = ln_inputs[i];
        print_comparison("ln(x)", x, cordic_ln(x, iterations), log(x));
    }

    double sqrt_inputs[] = {2.0, 3.0, 5.0, 9.0};
    for (int i = 0; i < 4; i++) {
        double x = sqrt_inputs[i];
        print_comparison("sqrt(x)", x, cordic_sqrt(x, iterations), sqrt(x));
    }

    double pow_bases[] = {2.0, 3.0, 1.5};
    double pow_exps[] = {3.0, 2.0, 2.5};
    for (int i = 0; i < 3; i++) {
        double b = pow_bases[i];
        double e = pow_exps[i];
        double cordic_res = cordic_pow(b, e, iterations);
        double math_res = pow(b, e);
        double error = fabs(cordic_res - math_res);
        printf("%-10s | %4.1f^%3.1f     | CORDIC: %15.10f | math.h: %15.10f | Err: %1.2e\n",
               "pow(x,y)", b, e, cordic_res, math_res, error);
    }

    printf("****************************************************************************************\n");
    return 0;
}