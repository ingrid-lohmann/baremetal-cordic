#include <stdio.h>

#include "ieee_utils_print.h"

void print_float_components(FloatIEEE val) {
    printf("\n**** Analise IEEE 754 ****");
    printf("\n Valor real: %.9g", (double)val.x);
    printf("\n Sinal:      %d", val.bits.s);
    printf("\n Expoente:   %d", val.bits.E);
    printf("\n Mantissa:   %u", val.bits.f);
    printf("\n Fracao:     %.9g", (double)val.bits.f / 0x1p23);
    printf("\n*************************\n");
}

void print_double_components(DoubleIEEE val) {
    printf("\n**** Analise IEEE 754 ****");
    printf("\n Valor real: %.17g", val.x);
    printf("\n Sinal:      %llu", (unsigned long long)val.bits.s);
    printf("\n Expoente:   %llu", (unsigned long long)val.bits.E);
    printf("\n Mantissa:   %llu", (unsigned long long)val.bits.f);
    printf("\n Fracao:     %.17g", (double)val.bits.f / 0x1p52);
    printf("\n*************************\n");
}