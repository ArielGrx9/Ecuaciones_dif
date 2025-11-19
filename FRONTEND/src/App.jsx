import { useState } from "react";
import {
  resolverVariacionParametros,
  resolverCoefInd,
  resolverPolinomioCaracteristico,
} from "./api/api";
import ResultadoEDO from "./ResultadoEDO";

function parseCondiciones(condStr) {
  if (!condStr.trim()) return null;

  const dict = {};

  condStr.split(";").forEach(par => {
    const [key, value] = par.split("=").map(s => s.trim());
    if (key && value && !isNaN(Number(value))) {
      dict[key] = Number(value);
    }
  });
  
  return Object.keys(dict).length ? dict : null;
}

export default function App() {
  const [metodo, setMetodo] = useState("");
  const [salida, setSalida] = useState(null);
  const [error, setError] = useState("");

  // Inputs
  const [coef, setCoef] = useState("");
  const [fx, setFx] = useState("");
  const [g, setG] = useState("");
  const [condiciones, setCondiciones] = useState("");
 

    async function enviar() {
  setSalida(null);
  setError("");

  try {
    let payload, res;

    // Parse seguro de coeficientes
 const coefList = coef
  .split(",")
  .map(c => c.trim())
  .filter(c => c !== "" && c !== "-" && c !== "+")
  .map(c => {
    const num = parseFloat(c);
    if (isNaN(num)) return null;
    // Si es entero (como 1, -4, 2), lo mandamos como entero
    return num % 1 === 0 ? parseInt(c, 10) : num;
  })
  .filter(n => n !== null);
  

      const condicionesDict = parseCondiciones(condiciones);

    if (coefList.length === 0 || coefList.some(isNaN)) {
      setError("Coeficientes inválidos");
      return;
    }

    // Parse seguro de condiciones
    const condList = condiciones
      ? condiciones.split(";").map(c => c.trim()).filter(c => c.length)
      : [];

    // Asegurar g como string
    const gStr = g ? g : "0";

    if (metodo === "variacion") {
      if (!fx.trim()) {
        setError("Debes ingresar f(x)");
        return;
      }

      payload = {
        coeficientes: coefList,
        fx: fx.trim(),
      };
      res = await resolverVariacionParametros(payload);
    }

    if (metodo === "coef") {
      payload = {
        coeficientes: coefList,
        g: g || "0",
        condiciones: condicionesDict,
        paso_a_paso: true
      };
      res = await resolverCoefInd(payload);
    }


   if (metodo === "poli") {
  const condicionesDict = parseCondiciones(condiciones);

  payload = {
    coeficientes: coefList,
    condiciones: condicionesDict,  
  };
  res = await resolverPolinomioCaracteristico(payload);
}

    setSalida(res.data);
  } catch (err) {
    console.error(err);
    setError(err.response?.data?.detail || "Error al procesar la petición.");
  }
}

 
  

  return (
    <div className="container" style={{ padding: 30 }}>
      <h2>Calculadora de Ecuaciones Diferenciales</h2>

      {/* Métodos */}
      <label>Método</label>
      <select
        className="form-select"
        value={metodo}
        onChange={(e) => setMetodo(e.target.value)}
      >
        <option value="">Selecciona...</option>
        <option value="variacion">Variación de parámetros</option>
        <option value="coef">Coeficientes indeterminados</option>
        <option value="poli">Polinomio característico</option>
      </select>

      {/* FORMULARIOS */}
      {metodo && (
        <div className="card p-3 mt-3">
          <label>Coeficientes (ej: 1, -3, 2)</label>
          <input
            className="form-control"
            value={coef}
            onChange={(e) => setCoef(e.target.value)}
          />

          {metodo === "variacion" && (
            <>
              <label className="mt-3">f(x)</label>
              <input
                className="form-control"
                value={fx}
                onChange={(e) => setFx(e.target.value)}
              />
            </>
          )}

          {metodo === "coef" && (
            <>
              <label className="mt-3">g(x)</label>
              <input
                className="form-control"
                value={g}
                onChange={(e) => setG(e.target.value)}
              />
            </>
          )}

          {(metodo === "coef" || metodo === "poli") && (
            <>
              <label className="mt-3">
                Condiciones (separadas por ";") — opcional
              </label>
              <input
                className="form-control"
                value={condiciones}
                onChange={(e) => setCondiciones(e.target.value)}
              />
            </>
          )}

          <button className="btn btn-danger mt-3" onClick={enviar}>
            Resolver
          </button>
        </div>
      )}

      {/* ERROR */}
      {error && <div className="alert alert-danger mt-3">{error}</div>}

      {/* RESULTADO */}
      {salida && (
        <div className="card p-3 mt-3">
          <h4>Resultado:</h4>
          <ResultadoEDO data={salida} />
         
        </div>
      )}
    </div>
  );
}
