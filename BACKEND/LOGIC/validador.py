import sympy as sp
def validar_solucion(y, coeficientes, g, x):
    """
    Valida si una función y(x) satisface la ecuación diferencial:
    a_n y^(n) + ... + a_1 y' + a_0 y = g(x)

    Retorna:
    - expresión L[y] - g(x)
    - True si es 0, False si no lo es
    """
    n = len(coeficientes)
    derivadas = [y]

    # Construir las derivadas necesarias
    for k in range(1, n):
        derivadas.append(sp.diff(derivadas[-1], x))

    # Construir L[y]
    lhs = 0
    for i in range(n):
        lhs += coeficientes[i] * derivadas[n - i - 1]

    lhs = sp.simplify(lhs)

    # Checar si LHS - g == 0
    residuo = sp.simplify(lhs - g)

    return residuo, sp.simplify(residuo) == 0


