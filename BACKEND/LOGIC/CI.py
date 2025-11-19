import sympy as sp

def aplicar_condiciones_generales(y_general, condiciones, x):
    """
    Aplica condiciones iniciales o de frontera a una solución simbólica.
    
    condiciones puede ser:
        {0: 1, 1: 0}              → y(0)=1, y'(0)=0
        {"y(0)": 1, "y'(0)": 0}   → igual pero explícito
        {"y(0)": 2, "y(1)": 5}    → diferentes puntos
    """

    # --- 1. Detectar constantes C0, C1, C2, ...
    C = sorted(
        [c for c in y_general.free_symbols if c.name.startswith("C")],
        key=lambda s: int(s.name[1:])
    )

    ecuaciones = []

    for key, valor in condiciones.items():

        # --- 2. Caso corto: cond = {0: value}
        if isinstance(key, int) or isinstance(key, float):
            deriv = key   # orden de derivada
            punto = 0     # por defecto
            expr = y_general.diff(x, deriv).subs(x, punto)
            ecuaciones.append(sp.Eq(expr, valor))
            continue

        # --- 3. Caso completo: "y(1)", "y'(0)", "y''(2)" etc.
        if isinstance(key, str):

            # Detectar derivada
            deriv = key.count("'")

            # Extraer el punto dentro del paréntesis
            punto = float(key.split("(")[1].split(")")[0])

            expr = y_general.diff(x, deriv).subs(x, punto)
            ecuaciones.append(sp.Eq(expr, valor))
            continue

        raise ValueError(f"Formato no reconocido en condición: {key}")

    # --- 4. Resolver el sistema para C0, C1...
    sol = sp.solve(ecuaciones, C, dict=True)

    if not sol:
        raise ValueError("El sistema de ecuaciones no tiene solución o está mal definido.")

    sol = sol[0]

    # --- 5. Sustituir las constantes en la solución general
    y_final = y_general.subs(sol)

    return sp.simplify(y_final), sol