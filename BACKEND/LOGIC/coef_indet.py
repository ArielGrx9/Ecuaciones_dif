import sympy as sp
from homogenea import solucion_homogenea
from validador import validar_solucion
def _decompose_term_simple(term, x):
    """
    Detecta la estructura del término: exp(a*x), trig (cos/sin) y resto polinomial.
    Devuelve (a, b, trig, poly) donde:
      - a: exponent coef (0 si no hay exp)
      - b: trig frequency (0 si no hay trig)
      - trig: None, 'cos', 'sin'
      - poly: factor restante (sympy expr), por ejemplo 3*x**2 o 1
    Esta versión es deliberadamente simple y cubre los casos típicos.
    """
    t = sp.simplify(term)
    a = sp.Integer(0)
    b = sp.Integer(0)
    trig = None
    poly = t

    # factorizar producto
    factors = sp.Mul.make_args(t)

    # buscar exp(a*x)
    for f in factors:
        if f.func == sp.exp:
            arg = f.args[0]
            # arg normalmente a*x
            a = sp.simplify(arg / x)
            poly = sp.simplify(poly / f)

    # buscar cos or sin
    for f in factors:
        if f.func == sp.cos or f.func == sp.sin:
            trig = 'cos' if f.func == sp.cos else 'sin'
            arg = f.args[0]
            b = sp.simplify(arg / x)
            poly = sp.simplify(poly / f)

    poly = sp.simplify(poly)
    return sp.simplify(a), sp.simplify(b), trig, poly

def detectar_resonancia(sols, roots, gx, x):
    """
    sols: lista de soluciones base [y1, y2, ...] (de solucion_homogenea_simple)
    roots: dict de raices (salida de sp.roots)
    gx: g(x) (SymPy expr)
    x: sympy symbol
    Retorna: lista de dicts informando por cada término de g(x):
      {
        'term': term,
        'decomp': (a,b,trig,poly),
        'resonancias': [ (root, multiplicidad, applied_mult) , ... ],
        'needs_multiplicacion_por_x': m  # máximo m a multiplicar (0 si no)
      }
    """
    gx = sp.simplify(gx)
    terms = sp.Add.make_args(gx)
    report = []

    # normalizar roots dict keys for comparison: compute (alpha,beta) pairs
    root_info = []
    for r, mult in roots.items():
        alpha = sp.simplify(sp.re(r))
        beta = sp.simplify(sp.im(r))
        root_info.append((r, alpha, beta, mult))

    for t in terms:
        a, b, trig, poly = _decompose_term_simple(t, x)
        m_needed = 0
        matched_roots = []
        # polinomial term (a==0 and trig is None)
        if trig is None and a == 0:
            # check if lambda=0 is a root
            for r, alpha, beta, mult in root_info:
                if sp.simplify(alpha) == 0 and sp.simplify(beta) == 0:
                    # multiplicidad m indica cuántas veces aparece lambda=0
                    matched_roots.append((r, mult, mult))  # se sugiere multiplicidad mult
                    m_needed = max(m_needed, mult)
        elif trig is None and a != 0:
            # exp(a*x) pure
            for r, alpha, beta, mult in root_info:
                if sp.simplify(alpha - a) == 0 and sp.simplify(beta) == 0:
                    matched_roots.append((r, mult, mult))
                    m_needed = max(m_needed, mult)
        else:
            # trig case or exp*trig (a maybe non-zero)
            for r, alpha, beta, mult in root_info:
                # match alpha==a and abs(beta)==abs(b)
                if sp.simplify(alpha - a) == 0 and sp.simplify(abs(beta) - abs(b)) == 0:
                    matched_roots.append((r, mult, mult))
                    m_needed = max(m_needed, mult)

        report.append({
            'term': t,
            'decomp': (a, b, trig, poly),
            'resonancias': matched_roots,
            'needs_multiplication_by_x_power': m_needed
        })

    return report


def proponer_particular(g, raices_homogeneas, x):

    # --------------------------
    # 1. Caso: polinomio puro
    # --------------------------
    if g.is_polynomial(x):
        n = sp.degree(g, x)
        A = sp.symbols(f"A0:{n+1}")
        propuesta_base = sum(A[i] * x**i for i in range(n+1))
        b = 0
        return propuesta_base * x**b, propuesta_base, b

    # ---------------------------------------
    # 2. Caso: g(x) = polinomio * exp(a*x)
    # ---------------------------------------
    exp_factor = None
    for fac in sp.Mul.make_args(g):
        if fac.func == sp.exp:
            exp_factor = fac
            break

    if exp_factor is not None:
        # Obtener a en exp(a*x)
        arg = exp_factor.args[0]    # a*x
        a = sp.simplify(arg / x)

        # Separar polinomio
        pol_part = sp.simplify(g / exp_factor)

        # Polinomio * exp(ax)
        if pol_part.is_polynomial(x):
            grado = sp.degree(pol_part, x)
            A = sp.symbols(f"A0:{grado+1}")
            propuesta_base = sum(A[i] * x**i for i in range(grado+1))
        # exp(a*x) solo
        elif pol_part.is_Number:
            A = sp.symbols("A0")
            propuesta_base = A
        else:
            raise ValueError("Exp(ax)*f(x) donde f(x) no es polinomio.")

        # Resonancia: comprobar si a es raíz homogénea
        b = 0
        for r, mult in raices_homogeneas:
            if r == a:
                b = mult
                break

        return propuesta_base * sp.exp(a*x) * x**b, propuesta_base * sp.exp(a*x), b

    # --------------------------
    # 3. Caso: senos y cosenos
    # --------------------------
    if g.has(sp.sin(x)) or g.has(sp.cos(x)):

        # Detectar frecuencia w
        w = None
        for t in g.atoms(sp.sin, sp.cos):
            arg = t.args[0]
            w = sp.simplify(arg / x)
            break

        A0, A1 = sp.symbols("A0 A1")
        propuesta_base = A0*sp.sin(w*x) + A1*sp.cos(w*x)

        # resonancia compleja → revisar ± wi
        b = 0
        for r, mult in raices_homogeneas:
            # raíz compleja r = α + β i → frecuencia β
            if r.is_real:
                continue
            beta = abs(sp.im(r))
            if sp.simplify(beta - w) == 0:
                b = mult
                break

        return propuesta_base * x**b, propuesta_base, b

    # --------------------------
    # Si no coincide con nada
    # --------------------------
    raise ValueError("g(x) no es una forma válida para coeficientes indeterminados")



def normalizar_sol_dict(sol, propuesta, x):

    """
    Normaliza la salida de sympy.solve para extraer los valores de los coeficientes A0, A1, ...
    Soporta:
    - Diccionarios
    - Listas con diccionarios
    - Listas con tuplas (soluciones paramétricas)
    - Parámetros libres -> se asignan a 0
    """

    # -------- CASO 1: dict --------
    if isinstance(sol, dict):
        return sol

    # -------- CASO 2: lista --------
    if isinstance(sol, list):

        # lista con un diccionario
        if len(sol) == 1 and isinstance(sol[0], dict):
            return sol[0]

        # lista con varios diccionarios
        if len(sol) > 1 and isinstance(sol[0], dict):
            return sol[0]

        # lista con un número: [2]
        if len(sol) == 1 and isinstance(sol[0], (int, float, sp.Number)):
            constantes = list(propuesta.free_symbols - {x})
            if len(constantes) != 1:
                raise ValueError("Solve devolvió lista con número pero hay múltiples constantes")
            return {constantes[0]: sol[0]}

        # -------- CASO NUEVO: lista con tupla paramétrica --------
        if len(sol) == 1 and isinstance(sol[0], tuple):
            tupla = sol[0]

            # Ordenar coeficientes por nombre: A0, A1, A2...
            coeficientes = sorted(
                list(propuesta.free_symbols - {x}),
                key=lambda s: s.name
            )

            if len(tupla) != len(coeficientes):
                raise ValueError("La tupla paramétrica no coincide con el número de coeficientes.")

            sol_final = {}

            # asignar valores
            for sym, val in zip(coeficientes, tupla):

                # Si el valor depende del propio símbolo → parámetro libre
                if sym in val.free_symbols:
                    sol_final[sym] = 0
                else:
                    sol_final[sym] = val

            return sol_final

    # -------- CASO 3: número --------
    if isinstance(sol, (int, float, sp.Number)):
        constantes = list(propuesta.free_symbols - {x})
        if len(constantes) != 1:
            raise ValueError("Solve devolvió número pero hay múltiples constantes")
        return {constantes[0]: sol}

    # -------- CASO DESCONOCIDO --------
    raise ValueError(f"Formato desconocido de solución: {sol}")

def sustituir_y_resolver(propuesta, coef, g, x):
    """
    coef = [a_n, ..., a_1, a_0]  (igual que en la ecuación homogénea)
    Ecuación: a_n y^(n) + ... + a1*y' + a0*y = g(x)
    """
    # --- 1: Detectar constantes A0, A1... ---
    constantes = list(propuesta.free_symbols - {x})

    # --- 2: Calcular derivadas ---
    y = propuesta
    derivadas = [y]
    for k in range(1, len(coef)):
        derivadas.append(sp.diff(derivadas[-1], x))

    # --- 3: Construir LHS ---
    lhs = 0
    n = len(coef)
    for i in range(n):
        lhs += coef[i] * derivadas[n - i - 1]

    lhs = sp.simplify(lhs)

    # --- 4: Igualar con g(x) ---
    eq = sp.Eq(lhs, g)

    # --- 5: Resolver ---
    sol = sp.solve(eq, constantes)

    # 🔧 NORMALIZAR LA SOLUCIÓN
    sol = normalizar_sol_dict(sol, propuesta, x)

    return lhs, sol

def extraer_raices(soluciones, x):
    raices = {}

    for sol in soluciones:

        # Caso exp(r*x)
        if sol.has(sp.exp):
            exp_part = [f for f in sol.atoms(sp.exp)][0]
            r = sp.simplify(exp_part.args[0] / x)

            # Detectar potencia de x
            potencia = 0
            for factor in sp.Mul.make_args(sol):
                if factor.is_Pow and factor.base == x:
                    potencia = factor.exp

            mult = potencia + 1

            raices[r] = raices.get(r, 0) + mult
            continue

        # Caso seno/coseno  => raíz compleja
        if sol.has(sp.sin) or sol.has(sp.cos):
            trig = list(sol.atoms(sp.sin, sp.cos))[0]
            w = sp.simplify(trig.args[0] / x)

            # Representamos raíz compleja como 0 ± wi
            r_complex = sp.I*w

            # Ambas funciones seno/coseno vienen por pares
            raices[r_complex] = 1
            continue

    # Convertir a lista de tuplas
    return [(r, raices[r]) for r in raices]

def normalizar_solucion_general(expr, C, x):
    """
    Reescribe la solución general en forma estándar:
    C0*exp(x) + C1*exp(-x/2)*cos(...) + C2*exp(-x/2)*sin(...) + particular
    """
    expr = sp.simplify(sp.expand(expr))

    # 1. Extraer parte con exp(x)
    term_exp_x = expr.expand().coeff(sp.exp(x))

    # 2. Extraer parte con exp(-x/2)*cos(...)
    term_cos = expr.expand().coeff(sp.exp(-x/2) * sp.cos(sp.sqrt(3)*x/2))

    # 3. Extraer parte con exp(-x/2)*sin(...)
    term_sin = expr.expand().coeff(sp.exp(-x/2) * sp.sin(sp.sqrt(3)*x/2))

    # 4. Particular = expr - homogénea
    homog = (term_exp_x * sp.exp(x)
             + term_cos * sp.exp(-x/2) * sp.cos(sp.sqrt(3)*x/2)
             + term_sin * sp.exp(-x/2) * sp.sin(sp.sqrt(3)*x/2))

    particular = sp.simplify(expr - homog)

    return sp.simplify(homog + particular)

x = sp.symbols('x') 
g = x**2*sp.exp(2*x)
y_h, sols, ra = solucion_homogenea([1, -2, 1]) 
raices = extraer_raices(sols, x)
coeficientes = [1, -2, 1] 


propuesta, _, _ = proponer_particular(g, raices, x)

print(f"propuesta: {propuesta}")
lhs, sol = sustituir_y_resolver(propuesta, coeficientes, g, x)

# sol YA ES dict
y_p = propuesta.subs(sol)
y_p = sp.simplify(y_p)

y_general = sp.simplify(y_h + y_p)

print("Solución general: ", y_general)
C0, C1 = sp.symbols("C1, C2")

y_general =  (C0 + C1*x + (x**2 - 4*x + 6)*sp.exp(x))*sp.exp(x)

residuo, es_correcta = validar_solucion(y_general, [1, -2, 1], x**2 * sp.exp(2*x), x)

print("Residuo:", residuo)
print("¿Solución correcta?:", es_correcta)