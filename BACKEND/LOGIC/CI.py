import sympy as sp

def aplicar_condiciones_generales(y_general, condiciones, x):
    """
    Aplica condiciones iniciales o a una solución simbólica.
    
    condiciones puede ser:
        {0: 1, 1: 0}              → y(0)=1, y'(0)=0
        {"y(0)": 1, "y'(0)": 0}   → igual pero explícito
        {"y(0)": 2, "y(1)": 5}    → diferentes puntos
    """

    C = sorted(
        [c for c in y_general.free_symbols if c.name.startswith("C")],
        key=lambda s: int(s.name[1:])
    )

    ecuaciones = []

    for key, valor in condiciones.items():

        if isinstance(key, int) or isinstance(key, float):
            deriv = key   # orden de derivada
            punto = 0     # por defecto
            expr = y_general.diff(x, deriv).subs(x, punto)
            ecuaciones.append(sp.Eq(expr, valor))
            continue

        if isinstance(key, str):

            deriv = key.count("'")

            punto = float(key.split("(")[1].split(")")[0])

            expr = y_general.diff(x, deriv).subs(x, punto)
            ecuaciones.append(sp.Eq(expr, valor))
            continue

        raise ValueError(f"Formato no reconocido en condición: {key}")

    sol = sp.solve(ecuaciones, C, dict=True)

    if not sol:
        raise ValueError("El sistema de ecuaciones no tiene solución o está mal definido.")

    sol = sol[0]

  
    y_final = y_general.subs(sol)

    return sp.simplify(y_final), sol