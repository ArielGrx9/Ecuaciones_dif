import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// Variación de parámetros
export function resolverVariacionParametros(payload) {
  return api.post("/variacion_parametros", payload);
}

// Coeficientes indeterminados
export function resolverCoefInd(payload) {
  return api.post("/coeficientes_indeterminados", payload);
}

// Polinomio característico
export function resolverPolinomioCaracteristico(payload) {
  return api.post("/polinomio-caracteristico", payload);
}

export default api;
