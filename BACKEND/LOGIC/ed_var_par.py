import sympy as sp
from homogenea import solucion_homogenea

def variacion_parametros(sols, fx):
    x = sp.symbols('x')
    n = len(sols)

    # MATRIZ DEL WRONSKIANO
    W = sp.Matrix([
        [sp.diff(sols[j], x, i) for j in range(n)]
        for i in range(n)
    ]).det()
    W = sp.simplify(W)

    print("\nWronskiano:")
    print(W)

    if W == 0:
        print("ERROR: El Wronskiano es cero (soluciones dependientes).")
        return sp.nan

    # Calcular u'_k
    u_primas = []
    for k in range(n):
        M = sp.Matrix([
            [sp.diff(sols[j], x, i) for j in range(n)]
            for i in range(n)
        ])
        M[:, k] = sp.Matrix([0]*(n-1) + [fx])

        u_k = M.det() / W
        u_primas.append(u_k)

    # Integrar cada u'
    u = [sp.integrate(up, x) for up in u_primas]

    # yp
    yp = sum(u[k] * sols[k] for k in range(n))
    yp = sp.simplify(yp)

    print("\nSolución particular:")
    print(yp)

    return yp

def solucion_general(y_h, y_p):
    y_g = sp.simplify(y_h + y_p)
    print("\nSolución general:")
    print(sp.latex(y_g))
  
    return sp.simplify(y_g)


def simplificar_general(expr, x):
    """
    Simplifica una solución general de EDO,
    agrupando términos por exponenciales, senos, cosenos,
    y absorbiendo constantes cuando es algebraicamente seguro.
    """

    expr = sp.simplify(expr)
    expr = sp.expand(expr)
    
    # 1. EXPONENCIALES: buscar cualquier cosa de la forma exp(a*x)
    exponentes = set()

    for t in expr.atoms(sp.exp):
        # t = exp(a*x) → guardar solo "a"
        a = sp.simplify(sp.log(t) / x)
        exponentes.add(a)

    # 2. AGRUPAR POR exp(a*x)
    for a in exponentes:
        expr = sp.collect(expr, sp.exp(a*x))

    # 3. AGRUPAR por senos y cosenos si hay raíces complejas
    expr = sp.collect(expr, sp.cos(x))
    expr = sp.collect(expr, sp.sin(x))

    # 4. factor final para embellecer
    expr = sp.simplify(expr)
    expr = sp.factor(expr)

    return expr

import sympy as sp


def verificar_solucion(y, ecuacion, variable):
    """
    Verifica si una función y(x) satisface una ecuación diferencial dada.
    """

    # Detectar el orden de la ED
    derivadas = ecuacion.atoms(sp.Derivative)

    if derivadas:
        orden = max(d.derivative_count for d in derivadas)
    else:
        orden = 0

    # Mapeo de sustituciones
    reemplazos = {}

    # y
    y_func = y
    reemplazos[sp.Function('y')(variable)] = y_func

    # y', y'', ..., y^(orden)
    for k in range(1, orden + 1):
        reemplazos[
            sp.diff(sp.Function('y')(variable), variable, k)
        ] = sp.diff(y_func, variable, k)

    # Sustituir en la ecuación
    resultado = ecuacion.subs(reemplazos)

    # Simplificar
    resultado = sp.simplify(resultado)

    return resultado

x = sp.symbols('x')

y_h, sols, _ = solucion_homogenea([1,-3,3,-1])
y_p = variacion_parametros(sols, sp.exp(x))
y_g = solucion_general(y_h, y_p)
yg_simplificada = simplificar_general(y_g, x)

print(yg_simplificada)
0


