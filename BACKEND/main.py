from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sympy as sp
from sympy import symbols, Function, dsolve, Eq, exp, I, re, im, latex
import warnings
warnings.filterwarnings('ignore')


class prueba(BaseModel):
    respuesta : str


app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
     CORSMiddleware,
     allow_origins = "*",
     allow_credentials = True,
     allow_methods = ["*"],
     allow_headers =  ["*"]
)


memory_db = {"respuesta": "hola we"}

@app.get("/hola")
def si_la_mami():
    return{"hola" : "we"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



class EDHomogenea:
    def __init__(self):
        self.t = symbols('t')
        self.y = Function('y')(self.t)
        
    def resolver_polinomio_caracteristico(self, coeficientes):
        """Resuelve la ecuación diferencial usando el polinomio característico"""
        print("=" * 60)
        print("RESOLUCIÓN DE ECUACIÓN DIFERENCIAL HOMOGÉNEA")
        print("=" * 60)
        
        # Mostrar la ecuación diferencial
        orden = len(coeficientes) - 1
        ecuacion_str = f"{coeficientes[0]}y^({orden})"
        for i in range(1, len(coeficientes)):
            if coeficientes[i] != 0:
                if orden - i > 1:
                    ecuacion_str += f" + {coeficientes[i]}y^({orden - i})"
                elif orden - i == 1:
                    ecuacion_str += f" + {coeficientes[i]}y'"
                else:
                    ecuacion_str += f" + {coeficientes[i]}y"
        
        ecuacion_str += " = 0"
        print(f"\nEcuación diferencial: {ecuacion_str}")
        
        # Construir y resolver el polinomio característico
        lambda_sym = symbols('lambda')
        pol_caracteristico = sum(coef * lambda_sym**(orden - i) for i, coef in enumerate(coeficientes))
        
        print(f"\nPolinomio característico: {pol_caracteristico} = 0")
        
        # Resolver el polinomio característico
        raices = sp.solve(pol_caracteristico, lambda_sym)
        print(f"\nRaíces del polinomio característico: {raices}")
        
        # Determinar la solución general
        solucion_general = self.obtener_solucion_general(raices)
        print(f"\nSolución general: y(t) = {solucion_general}")
        
        return raices, solucion_general
    
    def obtener_solucion_general(self, raices):
        """Construye la solución general basada en las raíces"""
        solucion = 0
        C_symbols = symbols(f'C1:{len(raices)+1}')
        
        raices_contadas = {}
        for raiz in raices:
            if raiz in raices_contadas:
                raices_contadas[raiz] += 1
            else:
                raices_contadas[raiz] = 1
        
        idx = 0
        for raiz, multiplicidad in raices_contadas.items():
            if multiplicidad == 1:
                if raiz.is_real:
                    solucion += C_symbols[idx] * exp(raiz * self.t)
                else:
                    # Para raíces complejas, usar forma trigonométrica
                    a = re(raiz)
                    b = im(raiz)
                    solucion += exp(a * self.t) * (
                        C_symbols[idx] * sp.cos(b * self.t) + 
                        C_symbols[idx+1] * sp.sin(b * self.t)
                    )
                    idx += 1
                idx += 1
            else:
                # Raíces repetidas
                for k in range(multiplicidad):
                    solucion += C_symbols[idx] * self.t**k * exp(raiz * self.t)
                    idx += 1
        
        return solucion
    
    def resolver_con_condiciones_iniciales(self, coeficientes, condiciones):
        """Resuelve la ED con condiciones iniciales"""
        print("\n" + "=" * 60)
        print("RESOLUCIÓN CON CONDICIONES INICIALES")
        print("=" * 60)
        
        # Crear la ecuación diferencial simbólica
        orden = len(coeficientes) - 1
        ecuacion = sum(coef * self.y.diff(self.t, orden - i) for i, coef in enumerate(coeficientes))
        
        # Resolver con condiciones iniciales
        try:
            solucion = dsolve(Eq(ecuacion, 0), self.y, ics=condiciones)
            print(f"Solución particular: {solucion}")
            return solucion
        except Exception as e:
            print(f"Error al resolver con condiciones iniciales: {e}")
            return None
    
    def graficar_solucion(self, coeficientes, condiciones=None, t_range=(0, 10)):
        """Grafica la solución de la ecuación diferencial"""
        # Convertir a sistema de EDOs de primer orden para solve_ivp
        orden = len(coeficientes) - 1
        
        def sistema_edos(t, y):
            dydt = np.zeros(orden)
            for i in range(orden - 1):
                dydt[i] = y[i + 1]
            
            # Última ecuación: a_n*y^(n) + a_{n-1}*y^(n-1) + ... + a_0*y = 0
            dydt[orden - 1] = -sum(coeficientes[i + 1] * y[orden - 1 - i] for i in range(orden)) / coeficientes[0]
            return dydt
        
        # Condiciones iniciales por defecto
        if condiciones is None:
            y0 = [1] + [0] * (orden - 1)  # y(0)=1, y'(0)=0, etc.
        else:
            y0 = [condiciones.get(f'y({i})', 0) for i in range(orden)]
        
        # Resolver numéricamente
        t_eval = np.linspace(t_range[0], t_range[1], 1000)
        sol = solve_ivp(sistema_edos, t_range, y0, t_eval=t_eval, method='RK45')
        
        # Graficar
        plt.figure(figsize=(12, 8))
        
        # Graficar la solución y sus derivadas
        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
        for i in range(min(orden, 3)):  # Graficar máximo las primeras 3 derivadas
            label = f"y"
            if i == 1:
                label += "'"  # Primera derivada
            elif i == 2:
                label += "''"  # Segunda derivada
            elif i > 2:
                label += f"^({i})"  # Derivadas superiores
            
            plt.plot(sol.t, sol.y[i], color=colors[i % len(colors)], 
                    linewidth=2, label=label)
        
        plt.xlabel('Tiempo (t)')
        plt.ylabel('y(t)')
        plt.title('Solución de la Ecuación Diferencial Homogénea')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        return sol

def main():
    """Función principal con ejemplos interactivos"""
    ed = EDHomogenea()
    
    print("RESOLVEDOR DE ED HOMOGÉNEAS DE ORDEN SUPERIOR")
    print("=" * 50)
    
    while True:
        print("\nOpciones:")
        print("1. Resolver ED de segundo orden: y'' + 3y' + 2y = 0")
        print("2. Resolver ED de tercer orden: y''' - 6y'' + 11y' - 6y = 0")
        print("3. Resolver ED con raíces complejas: y'' + 4y' + 13y = 0")
        print("4. Resolver ED con raíz repetida: y'' - 4y' + 4y = 0")
        print("5. Ingresar coeficientes manualmente")
        print("6. Salir")
        
        opcion = input("\nSeleccione una opción (1-6): ").strip()
        
        if opcion == '1':
            coeficientes = [1, 3, 2]  # y'' + 3y' + 2y = 0
            condiciones = None
            
        elif opcion == '2':
            coeficientes = [1, -6, 11, -6]  # y''' - 6y'' + 11y' - 6y = 0
            condiciones = None
            
        elif opcion == '3':
            coeficientes = [1, 4, 13]  # y'' + 4y' + 13y = 0
            condiciones = None
            
        elif opcion == '4':
            coeficientes = [1, -4, 4]  # y'' - 4y' + 4y = 0
            condiciones = None
            
        elif opcion == '5':
            try:
                orden = int(input("Ingrese el orden de la ED: "))
                coeficientes = []
                print("Ingrese los coeficientes (desde la derivada de mayor orden hasta y):")
                for i in range(orden, -1, -1):
                    if i > 1:
                        coef = float(input(f"Coeficiente para y^({i}): "))
                    elif i == 1:
                        coef = float(input("Coeficiente para y': "))
                    else:
                        coef = float(input("Coeficiente para y: "))
                    coeficientes.append(coef)
                
                coeficientes = coeficientes[::-1]  # Invertir para formato interno
                
                # Preguntar por condiciones iniciales
                usar_condiciones = input("¿Desea ingresar condiciones iniciales? (s/n): ").lower()
                if usar_condiciones == 's':
                    condiciones = {}
                    for i in range(orden):
                        valor = float(input(f"Condición inicial y^({i})(0): "))
                        condiciones[f'y({i})'] = valor
                else:
                    condiciones = None
                    
            except ValueError:
                print("Error: Ingrese valores numéricos válidos")
                continue
                
        elif opcion == '6':
            print("¡Hasta luego!")
            break
            
        else:
            print("Opción no válida")
            continue
        
        # Resolver la ecuación diferencial
        raices, solucion_general = ed.resolver_polinomio_caracteristico(coeficientes)
        
        # Resolver con condiciones iniciales si se proporcionaron
        if condiciones:
            solucion_particular = ed.resolver_con_condiciones_iniciales(coeficientes, condiciones)
        
        # Graficar la solución
        print("\nGenerando gráfica...")
        ed.graficar_solucion(coeficientes, condiciones)
        
        continuar = input("\n¿Desea resolver otra ecuación? (s/n): ").lower()
        if continuar != 's':
            print("¡Hasta luego!")
            break
