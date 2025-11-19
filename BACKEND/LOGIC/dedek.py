import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sympy as sp
from sympy import symbols, Function, dsolve, Eq, exp, I, re, im, latex
import warnings
warnings.filterwarnings('ignore')
import sympy as sp
from sympy import symbols, Function, exp, re, im, Eq, dsolve

class EDHomogenea:
    def __init__(self):
        self.t = symbols('t')
        self.y = Function('y')(self.t)

    def resolver_polinomio_caracteristico(self, coeficientes):
        """
        Resuelve la ecuación diferencial homogénea usando el polinomio característico.
        No imprime nada; solo devuelve raíces y la solución general.
        """
        orden = len(coeficientes) - 1
        lambda_sym = symbols('lambda')

        # Construir polinomio característico
        polinomio = sum(coef * lambda_sym**(orden - i) for i, coef in enumerate(coeficientes))

        # Raíces
        raices = sp.solve(polinomio, lambda_sym)

        # Construir solución general
        solucion_general = self._construir_solucion(raices)
        return {
            "polinomio": polinomio,
            "raices": raices,
            "solucion": solucion_general
        }

    def _construir_solucion(self, raices):
        solucion = 0
        C = symbols(f'C0:{len(raices)}')
        idx = 0

        # Contar multiplicidades
        mult = {}
        for r in raices:
            mult[r] = mult.get(r, 0) + 1

        # Construir solución
        for raiz, m in mult.items():
            if m == 1:
                if raiz.is_real:
                    solucion += C[idx] * exp(raiz * self.t)
                    idx += 1
                else:
                    a = re(raiz)
                    b = im(raiz)
                    solucion += exp(a * self.t) * (C[idx] * sp.cos(b * self.t) + C[idx+1] * sp.sin(b * self.t))
                    idx += 2
            else:
                # raíz repetida
                for k in range(m):
                    solucion += C[idx] * (self.t**k) * exp(raiz * self.t)
                    idx += 1

        return solucion

    def resolver_con_condiciones_iniciales(self, coeficientes, condiciones):
        """
        Resuelve la ED con condiciones iniciales usando dsolve.
        condiciones debe ser un dict: {'y(0)': valor, "y'(0)": valor, ...}
        """
        orden = len(coeficientes) - 1

        # Construir ecuación
        ecuacion = sum(coef * self.y.diff(self.t, orden - i) for i, coef in enumerate(coeficientes))

        # Convertir condiciones a formato SymPy
        ics = {}
        for key, val in condiciones.items():
            if key.startswith('y('):
                # y(0)
                punto = float(key[2:-1])
                ics[self.y.subs(self.t, punto)] = val
            else:
                # y'(0), y''(0), ...
                partes = key.split('(')
                deriv = partes[0]
                punto = float(partes[1][:-1])
                orden_der = deriv.count("'")
                ics[self.y.diff(self.t, orden_der).subs(self.t, punto)] = val

        try:
            solucion = dsolve(Eq(ecuacion, 0), self.y, ics=ics)
            return solucion
        except Exception as e:
            return {"error": str(e)}