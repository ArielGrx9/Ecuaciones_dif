import sympy as sp
from LOGIC.solucion_homogenea import solucion_homogenea


def variacion_parametros(sols, fx, variable=sp.symbols('x')):
    """
    Recibe:
        sols: lista de soluciones de la homogénea [y1, y2, ...]
        fx: función f(x) del lado derecho de la EDO
        variable: la variable (x)
    Retorna:
        yp: solución particular
        pasos: dict con paso a paso del proceso
    """

    x = variable
    n = len(sols)

    pasos = {
        "wronskiano": None,
        "u_primas": [],
        "u_integradas": [],
        "solucion_particular": None
    }

    # --- Wronskiano ---
    W = sp.Matrix([
        [sp.diff(sols[j], x, i) for j in range(n)]
        for i in range(n)
    ]).det()

    W = sp.simplify(W)
    pasos["wronskiano"] = str(W)

    if W == 0:
        return None, {"error": "El Wronskiano es cero. Soluciones dependientes."}

    # --- Calcular u'_k ---
    u_primas = []
    for k in range(n):
        M = sp.Matrix([
            [sp.diff(sols[j], x, i) for j in range(n)]
            for i in range(n)
        ])
        M[:, k] = sp.Matrix([0]*(n-1) + [fx])  # reemplazar columna k

        u_k = sp.simplify(M.det() / W)
        u_primas.append(u_k)
        pasos["u_primas"].append(str(u_k))

    # --- Integrar u'_k ---
    u = []
    for uk in u_primas:
        integ = sp.simplify(sp.integrate(uk, x))
        u.append(integ)
        pasos["u_integradas"].append(str(integ))

    # --- Solución particular ---
    yp = sum(u[k] * sols[k] for k in range(n))
    yp = sp.simplify(yp)
    pasos["solucion_particular"] = str(yp)

    return yp, pasos


def solucion_general(y_h, y_p):
    return sp.simplify(y_h + y_p)


def simplificar_general(expr, x):
    expr = sp.simplify(expr)
    expr = sp.expand(expr)

    exponentes = set()

    for t in expr.atoms(sp.exp):
        a = sp.simplify(sp.log(t) / x)
        exponentes.add(a)

    for a in exponentes:
        expr = sp.collect(expr, sp.exp(a*x))

    expr = sp.collect(expr, sp.cos(x))
    expr = sp.collect(expr, sp.sin(x))

    return sp.factor(sp.simplify(expr))


def verificar_solucion(y, ecuacion, variable):
    derivadas = ecuacion.atoms(sp.Derivative)
    orden = max([d.derivative_count for d in derivadas], default=0)

    reemplazos = {}
    y_func = y
    reemplazos[sp.Function('y')(variable)] = y_func

    for k in range(1, orden + 1):
        reemplazos[sp.diff(sp.Function('y')(variable), variable, k)] = sp.diff(y_func, variable, k)

    return sp.simplify(ecuacion.subs(reemplazos))
