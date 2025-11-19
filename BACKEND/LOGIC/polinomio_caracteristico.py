import sympy as sp
from sympy import symbols, Function, exp, re, im, Eq, dsolve


class EDHomogenea:
    def __init__(self):
        self.t = symbols('t')
        self.y = Function('y')(self.t)

        
    def resolver_polinomio_caracteristico(self, coeficientes):
        orden = len(coeficientes) - 1
        λ = symbols("lambda")

        polinomio = sum(coef * λ**(orden - i) for i, coef in enumerate(coeficientes))
        raices = sp.solve(polinomio, λ)
        solucion = self._construir_solucion(raices)

        # ←←←← AQUÍ EL CAMBIO MÁGICO ←←←←
        from util.formatear_expresion import normalize_expr   # o pega la función si no existe

        return {
            "polinomio": normalize_expr(polinomio),      # ← objeto con .latex
            "raices": [normalize_expr(r) for r in raices],
            "solucion": normalize_expr(solucion),
        }


    def _construir_solucion(self, raices):
        solucion = 0
        C = symbols(f'C0:{len(raices)}')
        idx = 0

        # Contar multiplicidades
        multiplicidad = {}
        for r in raices:
            multiplicidad[r] = multiplicidad.get(r, 0) + 1

        # Construcción de la solución
        for raiz, mult in multiplicidad.items():
            if mult == 1:
                # Raíz simple
                if raiz.is_real:
                    solucion += C[idx] * sp.exp(raiz * self.t)
                    idx += 1
                else:
                    # Raíz compleja a + bi
                    a = re(raiz)
                    b = im(raiz)
                    solucion += sp.exp(a * self.t) * (
                        C[idx] * sp.cos(b * self.t) +
                        C[idx + 1] * sp.sin(b * self.t)
                    )
                    idx += 2
            else:
                # Raíz repetida
                for k in range(mult):
                    solucion += C[idx] * (self.t**k) * sp.exp(raiz * self.t)
                    idx += 1

        return solucion
    
    def normalize_expr(expr):
        if expr is None:
            return {"latex": "", "plain": ""}
        
        try:
            if isinstance(expr, str):
                expr = sp.sympify(expr, locals={"x": sp.symbols("x"), "t": sp.symbols("t")})
            
            # En SymPy 1.14+ ya usa e^{2x} y \ln(x) por defecto, solo limpiamos lo feo
            latex = sp.latex(expr, mode='inline', fold_short_frac=True)
            
            # Solo quitamos \left y \right que SymPy mete de más
            latex = latex.replace(r'\left', '').replace(r'\right', '')
            
            # Bonus: si por algún motivo queda \exp, lo cambiamos manualmente
            if r'\exp' in latex:
                latex = latex.replace(r'\exp', 'e^{')
            
            return {
                "latex": latex,
                "plain": str(expr)
            }
            
        except Exception as e:
            return {
                "latex": f"\\text{{Error: {str(e)}}}",
                "plain": str(expr) if expr else "Error"
            }

 
    def resolver_con_condiciones_iniciales(self, coeficientes, condiciones):
        """
        condiciones = {
            "y(0)": 1,
            "y'(0)": 2,
            "y''(1)": 3
        }
        """
        orden = len(coeficientes) - 1

        # Construir ecuación LHS = 0
        ecuacion = sum(
            coef * self.y.diff(self.t, orden - i)
            for i, coef in enumerate(coeficientes)
        )

        # Convertir condiciones iniciales
        ics = self._procesar_condiciones(condiciones)

        try:
            sol = dsolve(Eq(ecuacion, 0), self.y, ics=ics)
            # Si sol es una Eq, extraemos el rhs
            if hasattr(sol, 'rhs'):
                sol = sol.rhs
            return self.normalize_expr(sol)   # ← directamente objeto con .latex
        except Exception as e:
            return {"error": str(e)}


    def _procesar_condiciones(self, condiciones):
        ics = {}
        for key, val in condiciones.items():

            # CASO: y(0)
            if key.startswith("y("):
                punto = float(key[2:-1])
                ics[self.y.subs(self.t, punto)] = val
                continue

            # CASO: y'(0), y''(1), y'''(2), etc
            deriv, resto = key.split("(")
            punto = float(resto[:-1])
            orden = deriv.count("'")

            ics[self.y.diff(self.t, orden).subs(self.t, punto)] = val

        return ics
