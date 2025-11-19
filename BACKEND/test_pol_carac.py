from LOGIC.polinomio_caracteristico import EDHomogenea

solver = EDHomogenea()

coef = [1, -3, 2]
cond = {"y(0)": 2, "y'(0)": 1}

resp1 = solver.resolver_polinomio_caracteristico(coef)
resp2 = solver.resolver_con_condiciones_iniciales(coef, cond)

print(resp1)
print(resp2)