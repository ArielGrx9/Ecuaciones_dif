import sympy as sp
from LOGIC.coef_indet import resolver_coeficientes_indeterminados

# -----------------------------
# EJEMPLO DE PRUEBA
# Ecuación:
#     y'' - 2y' + y = x^2 * exp(x)
#
# Condiciones iniciales:
#     y(0) = 1
#     y'(0) = 0
# -----------------------------

payload = {
    "coeficientes": [1, -2, 1],   # corresponde a y'' - 2y' + y
    "g": "x**2 * exp(x)",
    "condiciones": {
        "y(0)": 1,
        "y'(0)": 0
    },
    "paso_a_paso": True
}

resultado = resolver_coeficientes_indeterminados(payload)

# Mostrar resultados importantes
print("\n========================")
print(" SOLUCIÓN OBTENIDA")
print("========================")

print("\nY_h:")
print(resultado["y_h"])

print("\nY_p:")
print(resultado["y_p"])

print("\nY_general:")
print(resultado["y_general"])

if "y_final" in resultado:
    print("\nY_final con condiciones iniciales:")
    print(resultado["y_final"])

print("\n---------------------------")
print("RESIDUO (verificación):")
print(resultado["pasos"]["residuo_yg_minus_g"])

print("---------------------------")

