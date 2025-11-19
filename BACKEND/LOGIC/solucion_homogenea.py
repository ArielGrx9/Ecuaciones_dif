import sympy as sp

def solucion_homogenea(coef):
    x = sp.symbols('x')
    λ = sp.symbols('λ')

    # Polinomio característico
    n = len(coef)
    pol = sum(coef[i] * λ**(n-i-1) for i in range(n))
    print("Polinomio:", pol)

    # Raíces con multiplicidad
    raices = sp.roots(pol)
    print("Raíces:", raices)

    soluciones = []
    y_h = 0

    # Crear una lista ordenada de raíces para poder saltar conjugados
    lista_raices = list(raices.items())

    # Lista de constantes del mismo tamaño que soluciones que se generen
    total_constantes = sum([
        (1 if not r.is_real else mult) if not r.is_real else mult
        for r, mult in lista_raices
    ])

    C = sp.symbols(f"C0:{total_constantes}")
    c_index = 0

    i = 0
    while i < len(lista_raices):
        r, mult = lista_raices[i]

        # -------------------------
        # CASO: RAÍZ COMPLEJA
        # -------------------------
        if not r.is_real:
            alpha = sp.re(r)
            beta = abs(sp.im(r))

            y1 = sp.exp(alpha*x) * sp.cos(beta*x)
            y2 = sp.exp(alpha*x) * sp.sin(beta*x)

            soluciones += [y1, y2]

            y_h += C[c_index] * y1
            y_h += C[c_index+1] * y2
            c_index += 2

            # Saltar el conjugado
            i += 2
            continue

        # -------------------------
        # CASO: RAÍZ REAL
        # -------------------------
        for k in range(mult):
            yk = x**k * sp.exp(r*x)
            soluciones.append(yk)
            y_h += C[c_index] * yk
            c_index += 1
        
        i += 1

    print("\nSolución homogénea:")
    print(y_h)

    return y_h, soluciones, raices