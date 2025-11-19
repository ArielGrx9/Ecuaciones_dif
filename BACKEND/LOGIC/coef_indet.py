import sympy as sp
from typing import Dict, Any, List, Tuple, Optional

try:
    from LOGIC.solucion_homogenea import solucion_homogenea
except Exception:
    def solucion_homogenea(coef):
        x = sp.symbols("x")
        n = len(coef)-1
        lam = sp.symbols('lambda')
        pol = sum(c*lam**(n-i) for i,c in enumerate(coef))
        roots = sp.solve(pol, lam)
        sols = [sp.exp(r*x) for r in roots]
        y_h = sum(sp.symbols(f"C{i}")*sols[i] for i in range(len(sols)))
        return y_h, sols, roots

def normalize_expr(expr):
    """Convierte cualquier cosa en {latex: ..., plain: ...}"""
    if expr is None:
        return {"latex": "", "plain": ""}
    try:
        if isinstance(expr, str):
            expr = sp.sympify(expr, locals={"x": sp.symbols("x")})
        latex = sp.latex(expr, mode='inline')
        latex = latex.replace(r'\left', '').replace(r'\right', '')
        return {"latex": latex, "plain": str(expr)}
    except:
        return {"latex": "\\text{Error}", "plain": str(expr)}


def _decompose_term_simple(term: sp.Expr, x: sp.Symbol):
    t = sp.simplify(term)
    a = sp.Integer(0)
    b = sp.Integer(0)
    trig = None
    poly = t

    factors = sp.Mul.make_args(t)

    for f in factors:
        if f.func == sp.exp:
            arg = f.args[0]
            a = sp.simplify(arg / x)
            poly = sp.simplify(poly / f)

    for f in factors:
        if f.func == sp.cos or f.func == sp.sin:
            trig = 'cos' if f.func == sp.cos else 'sin'
            arg = f.args[0]
            b = sp.simplify(arg / x)
            poly = sp.simplify(poly / f)

    poly = sp.simplify(poly)
    return sp.simplify(a), sp.simplify(b), trig, poly


def extraer_raices(soluciones: List[sp.Expr], x: sp.Symbol):
    raices = {}
    for sol in soluciones:
        if sol.has(sp.exp):
            exp_part = [f for f in sol.atoms(sp.exp)][0]
            r = sp.simplify(exp_part.args[0] / x)
            potencia = 0
            for factor in sp.Mul.make_args(sol):
                if factor.is_Pow and factor.base == x:
                    potencia = int(factor.exp)
            mult = potencia + 1
            raices[r] = raices.get(r, 0) + mult
            continue
        if sol.has(sp.sin) or sol.has(sp.cos):
            trig = list(sol.atoms(sp.sin, sp.cos))[0]
            w = sp.simplify(trig.args[0] / x)
            r_complex = sp.I * w
            raices[r_complex] = raices.get(r_complex, 0) + 1
            continue
    return [(r, raices[r]) for r in raices]


def detectar_resonancia(sols, roots_dict: List[Tuple[sp.Expr,int]], gx: sp.Expr, x: sp.Symbol):
    report = []
    gx = sp.simplify(gx)
    terms = sp.Add.make_args(gx)
    root_info = []
    for r, mult in roots_dict:
        alpha = sp.simplify(sp.re(r))
        beta = sp.simplify(sp.im(r))
        root_info.append((r, alpha, beta, mult))
    for t in terms:
        a, b, trig, poly = _decompose_term_simple(t, x)
        m_needed = 0
        matched = []
        if trig is None and a == 0:
            for r, alpha, beta, mult in root_info:
                if sp.simplify(alpha) == 0 and sp.simplify(beta) == 0:
                    matched.append((r, mult, mult))
                    m_needed = max(m_needed, mult)
        elif trig is None and a != 0:
            for r, alpha, beta, mult in root_info:
                if sp.simplify(alpha - a) == 0 and sp.simplify(beta) == 0:
                    matched.append((r, mult, mult))
                    m_needed = max(m_needed, mult)
        else:
            for r, alpha, beta, mult in root_info:
                if sp.simplify(alpha - a) == 0 and sp.simplify(abs(beta) - abs(b)) == 0:
                    matched.append((r, mult, mult))
                    m_needed = max(m_needed, mult)
        report.append({
            'term': str(t),
            'decomp': (str(a), str(b), str(trig), str(poly)),
            'resonancias': [(str(r), mult, m) for (r,m,m2) in matched for mult in [m2]],
            'needs_multiplication_by_x_power': int(m_needed)
        })
    return report


def proponer_particular(g: sp.Expr, raices_homogeneas: List[Tuple[sp.Expr,int]], x: sp.Symbol):
    g = sp.simplify(g)

    if g.is_polynomial(x):
        n = sp.degree(g, x)
        A = sp.symbols(f"A0:{n+1}")
        propuesta_base = sum(A[i] * x**i for i in range(n+1))
        m = 0
        for r, mult in raices_homogeneas:
            if sp.simplify(r) == 0:
                m = max(m, mult)
        return propuesta_base * x**m, propuesta_base, m

    exp_fac = None
    for f in sp.Mul.make_args(g):
        if f.func == sp.exp:
            exp_fac = f
            break

    if exp_fac is not None:
        a = sp.simplify(exp_fac.args[0] / x)
        pol_part = sp.simplify(g / exp_fac)
        if pol_part.is_Number:
            grado = 0
            A = sp.symbols("A0")
            base = A
        elif pol_part.is_polynomial(x):
            grado = sp.degree(pol_part, x)
            A = sp.symbols(f"A0:{grado+1}")
            base = sum(A[i]*x**i for i in range(grado+1))
        else:
            raise ValueError("Exp(ax)*f(x) donde f(x) no es polinomio no soportado.")

        b = 0
        for r, mult in raices_homogeneas:
            if sp.simplify(r - a) == 0:
                b = max(b, mult)
        return base * sp.exp(a*x) * x**b, base * sp.exp(a*x), b

    if g.has(sp.sin) or g.has(sp.cos):
        trigs = list(g.atoms(sp.sin, sp.cos))
        trig = trigs[0]
        w = sp.simplify(trig.args[0]/x)
        A0, A1 = sp.symbols("A0 A1")
        base = A0*sp.sin(w*x) + A1*sp.cos(w*x)
        b = 0
        for r, mult in raices_homogeneas:
            if not r.is_real:
                beta = abs(sp.im(r))
                if sp.simplify(beta - w) == 0:
                    b = max(b, mult)
        return base * x**b, base, b

    raise ValueError("g(x) no es una forma válida para coeficientes indeterminados")


def normalizar_sol_dict(sol, propuesta, x: sp.Symbol):
    if isinstance(sol, dict):
        return sol
    if isinstance(sol, list):
        if len(sol) == 1 and isinstance(sol[0], dict):
            return sol[0]
        if len(sol) == 1 and isinstance(sol[0], (int, float, sp.Number)):
            constantes = list(propuesta.free_symbols - {x})
            if len(constantes) != 1:
                raise ValueError("Solve devolvió número pero hay múltiples constantes")
            return {constantes[0]: sol[0]}
        if len(sol) == 1 and isinstance(sol[0], tuple):
            tupla = sol[0]
            coeficientes = sorted(list(propuesta.free_symbols - {x}), key=lambda s: s.name)
            if len(tupla) != len(coeficientes):
                sol_final = {sym: 0 for sym in coeficientes}
                return sol_final
            sol_final = {}
            for sym, val in zip(coeficientes, tupla):
                sol_final[sym] = 0 if sym in val.free_symbols else val
            return sol_final
    if isinstance(sol, (int, float, sp.Number)):
        constantes = list(propuesta.free_symbols - {x})
        if len(constantes) != 1:
            raise ValueError("Solve devolvió número pero hay múltiples constantes")
        return {constantes[0]: sol}
    raise ValueError(f"Formato desconocido de solución: {sol}")


def sustituir_y_resolver(propuesta: sp.Expr, coef: List[float], g: sp.Expr, x: sp.Symbol):
    constantes = list(propuesta.free_symbols - {x})
    y = propuesta
    derivadas = [y]
    for k in range(1, len(coef)):
        derivadas.append(sp.diff(derivadas[-1], x))
    lhs = sum(coef[i] * derivadas[len(coef) - i - 1] for i in range(len(coef)))
    lhs = sp.simplify(lhs)
    eq = sp.Eq(lhs, g)
    sol = sp.solve(eq, constantes)
    sol = normalizar_sol_dict(sol, propuesta, x)
    return lhs, sol


def aplicar_condiciones_generales(y_general: sp.Expr, condiciones: Dict[Any, float], x: sp.Symbol):
    C = sorted([c for c in y_general.free_symbols if str(c).startswith("C")], key=lambda s: int(str(s)[1:]))
    ecuaciones = []
    for key, valor in condiciones.items():
        if isinstance(key, (int, float)):
            deriv = int(key)
            punto = 0
            expr = sp.simplify(y_general.diff(x, deriv).subs(x, punto))
            ecuaciones.append(sp.Eq(expr, valor))
            continue
        if isinstance(key, str):
            deriv = key.count("'")
            punto = float(key.split("(")[1].split(")")[0])
            expr = sp.simplify(y_general.diff(x, deriv).subs(x, punto))
            ecuaciones.append(sp.Eq(expr, valor))
            continue
        raise ValueError(f"Formato no reconocido en condición: {key}")
    sol = sp.solve(ecuaciones, C, dict=True)
    if not sol:
        raise ValueError("No se encontró solución para las condiciones iniciales")
    sol = sol[0]
    y_final = sp.simplify(y_general.subs(sol))
    return y_final, sol


def resolver_coeficientes_indeterminados(payload: Dict[str, Any]):

    x = sp.symbols('x')
    coeficientes = payload.get("coeficientes")
    if coeficientes is None:
        return {"error": "Se requieren coeficientes."}

    g_raw = payload.get("g")
    if g_raw is None:
        return {"error": "Se requiere g (lado derecho)."}
    g = sp.sympify(g_raw) if isinstance(g_raw, str) else g_raw

    condiciones = payload.get("condiciones", None)

    # 1) Homogénea
    y_h, sols, lambdas = solucion_homogenea(coeficientes)
    pasos = {}
    coeficientes = [int(c) for c in coeficientes]

    λ = sp.symbols('lambda')
    n = len(coeficientes)
    polinomio = sum(coef * λ**(n - 1 - i) for i, coef in enumerate(coeficientes))
    pasos["polinomio_caracteristico"] = str(polinomio)
    pasos["lambdas"] = [str(l) for l in lambdas]
    pasos["soluciones_base"] = [str(s) for s in sols]

    # 2) Raíces y resonancia
    raices_info = extraer_raices(sols, x)
    pasos["raices_info"] = [(str(r), int(m)) for r, m in raices_info]
    pasos["deteccion_resonancia"] = detectar_resonancia(sols, raices_info, g, x)

    # 3) Propuesta particular
    propuesta, propuesta_base, mult_x = proponer_particular(g, raices_info, x)
    pasos["propuesta"] = str(propuesta)
    pasos["propuesta_base"] = str(propuesta_base)
    pasos["multiplicar_x_por"] = int(mult_x)

    # 4) Sustituir y resolver
    lhs, sol_consts = sustituir_y_resolver(propuesta, coeficientes, g, x)
    pasos["lhs"] = str(lhs)
    pasos["sistema_resolver"] = str(sp.Eq(lhs, g))
    pasos["constantes_encontradas"] = {str(k): str(v) for k, v in sol_consts.items()}

    # 5) Construir soluciones
    y_p = sp.simplify(propuesta.subs(sol_consts))
    y_g = sp.simplify(y_h + y_p)
    pasos["y_particular"] = str(y_p)
    pasos["y_general_before_CI"] = str(y_g)

    # 6) Condiciones iniciales
    y_final = None
    if condiciones:
        try:
            y_final, sol_C = aplicar_condiciones_generales(y_g, condiciones, x)
            pasos["aplicar_CI"] = {"y_final": str(y_final), "constantes": {str(k): str(v) for k, v in sol_C.items()}}
        except Exception as e:
            pasos["aplicar_CI"] = {"error": str(e)}
    else:
        pasos["aplicar_CI"] = None

    # 7) Validación rápida
    try:
        from LOGIC.validador import validar_solucion
    except:
        def validar_solucion(y, coef, gexpr, var):
            n = len(coef)
            derivs = [y]
            for _ in range(1, n):
                derivs.append(sp.diff(derivs[-1], var))
            return sp.simplify(sum(coef[i] * derivs[n-1-i] for i in range(n)) - gexpr)

    residuo = validar_solucion(y_g, coeficientes, g, x)
    pasos["residuo_yg_minus_g"] = str(residuo)
    pasos["es_cero"] = residuo == 0

    
    result = {
        "lambdas": [normalize_expr(l)["latex"] for l in lambdas],
        "soluciones_homogeneas": [normalize_expr(s)["latex"] for s in sols],

        "solucion_homogenea": normalize_expr(y_h),
        "solucion_particular": normalize_expr(y_p),
        "solucion_general": normalize_expr(y_final) if y_final is not None else normalize_expr(y_g),

        "pasos": pasos,

        # Compatibilidad con tests viejos
        "y_h": normalize_expr(y_h),
        "y_p": normalize_expr(y_p),
        "y_general": normalize_expr(y_g),
    }

    if y_final is not None:
        result["y_final"] = normalize_expr(y_final)
        result["solucion_general"] = normalize_expr(y_final)

    return result