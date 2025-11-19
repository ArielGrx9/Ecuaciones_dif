import sympy as sp
from LOGIC.variacion_parametros import *

x = sp.symbols("x")



# 1. Solución homogénea
y_h, sols, lambdas = solucion_homogenea([1, 0, 1])
print(y_h, sols, lambdas)

# 2. Variación de parámetros
y_p, pasos = variacion_parametros(sols, sp.tan(x), x)
print(y_p, pasos)

# 3. Solución general
y_g = solucion_general(y_h, y_p)
print(y_g)

# 4. Simplificar
y_g_simplificada = simplificar_general(y_g, x)
print(y_g_simplificada)

