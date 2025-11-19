import { useState } from "react";

/* ------------------ normalizador de expresiones (tu versión) ------------------ */
function validarExpresiones(expr) {
  let normalizar = expr.toLowerCase();

  // Seno
  normalizar = normalizar.replace(/\bsen\b/g, "sin");
  normalizar = normalizar.replace(/\bseno\b/g, "sin");

  // Coseno
  normalizar = normalizar.replace(/\bcoseno\b/g, "cos");

  // Tangente
  normalizar = normalizar.replace(/\btan\b/g, "tan");
  normalizar = normalizar.replace(/\btangente\b/g, "tan");

  // Raíz
  normalizar = normalizar.replace(/\braiz\b/g, "sqrt");
  normalizar = normalizar.replace(/\braíz\b/g, "sqrt");
  normalizar = normalizar.replace(/√\(/g, "sqrt(");
  normalizar = normalizar.replace(/√([a-z0-9]+)/gi, "sqrt($1)");

  // Logaritmos
  normalizar = normalizar.replace(/\blogaritmo\b/g, "log");
  normalizar = normalizar.replace(/\blog natural\b/g, "ln");

  // Variaciones de "e"
  normalizar = normalizar.replace(/\be\^/g, "exp(");
  normalizar = normalizar.replace(/e\^([a-z0-9]+)/gi, "exp($1)");

  // Exp
  normalizar = normalizar.replace(/\bexponencial\b/g, "exp");

  // Potencias
  normalizar = normalizar.replace(/\bcuadrado\b/g, "^2");
  normalizar = normalizar.replace(/\bcubico\b/g, "^3");
  normalizar = normalizar.replace(/\bcúbico\b/g, "^3");

  // Constantes
  normalizar = normalizar.replace(/\bpi\b/g, "pi");
  normalizar = normalizar.replace(/\bπ\b/g, "pi");

  // Derivadas
  normalizar = normalizar.replace(/([a-z])''''\b/g, "diff($1, x, 4)");
  normalizar = normalizar.replace(/([a-z])'''\b/g, "diff($1, x, 3)");
  normalizar = normalizar.replace(/([a-z])''\b/g, "diff($1, x, 2)");
  normalizar = normalizar.replace(/([a-z])'\b/g, "diff($1, x)");

  // limpieza final
  normalizar = normalizar.replace(/\s+/g, " ").trim();

  return normalizar;
}

function esValida(expr) {
  const patron = /^[0-9xyz+\-*/^=().,'\s\|a-záéíóúñπ√]+$/i;
  if (!patron.test(expr)) return false;

  const funcionesValidas = new Set([
    "sin",
    "cos",
    "tan",
    "sinh",
    "cosh",
    "tanh",
    "sqrt",
    "log",
    "ln",
    "exp",
    "diff",
    "y",
    "x",
    "z",
    "pi",
    "e",
    "sen",
    "seno",
    "raiz",
    "exponencial",
    "tan",
    "tangente",
    // por si el usuario escribe palabras normalizables
    "senh",
    "cosh",
    "tanh",
    "logaritmo",
    "log10",
    "cuadrado",
    "cubico",
    "cúbico",
  ]);

  const palabras = expr.toLowerCase().match(/[a-záéíóúñπ]+/g);
  if (!palabras) return true;

  for (let p of palabras) {
    if (!funcionesValidas.has(p)) {
      return false;
    }
  }
  return true;
}

/*Normalizar una condición inicial concreta*/
function normalizeCondition(cond) {
  let c = cond.trim().toLowerCase();

  c = c.replace(/\s*=\s*/, "=");

  // transformar derivadas
  c = c.replace(/([a-z])''''\(/g, "diff($1, x, 4)(");
  c = c.replace(/([a-z])''''/g, "diff($1, x, 4)");
  c = c.replace(/([a-z])'''/g, "diff($1, x, 3)");
  c = c.replace(/([a-z])''/g, "diff($1, x, 2)");
  c = c.replace(/([a-z])'/g, "diff($1, x)");

  // quitar espacios
  c = c.replace(/\s+/g, " ").trim();

  return c;
}

/*Validar formato de cada condición*/
function esCondicionValida(cond) {
  const re1 =
    /^\s*[a-z]('{1,4})?\s*\(\s*-?\d+(\.\d+)?\s*\)\s*=\s*-?\d+(\.\d+)?\s*$/i;
  const re2 =
    /^\s*diff\([a-z]\s*,\s*x(,\s*\d+\s*)?\)\s*\(\s*-?\d+(\.\d+)?\s*\)\s*=\s*-?\d+(\.\d+)?\s*$/i;

  return re1.test(cond) || re2.test(cond);
}

/*Componente principal*/
function EcDif() {
  const [input, setInput] = useState("");
  const [type, setType] = useState("Homogénea");
  const [condsInput, setCondsInput] = useState("");
  const [resultExpression, setResultExpression] = useState("");
  const [resultConditions, setResultConditions] = useState([]);
  const [error, setError] = useState("");

  const handleSend = () => {
    setError("");
    setResultExpression("");
    setResultConditions([]);

    // validación básica de la ecuación
    if (!input || input.trim() === "") {
      setError("Error: Ingresa una ecuación.");
      return;
    }
    if (!esValida(input)) {
      setError("Error: La ecuación contiene caracteres o palabras no válidas.");
      return;
    }

    // normalizar ecuación
    const normalizada = validarExpresiones(input);

    if (!normalizada || normalizada.trim() === "") {
      setError("Error: La ecuación no es válida después de normalizar.");
      return;
    }

    // procesar condiciones (si hay)
    let conds = [];
    if (condsInput && condsInput.trim() !== "") {
      // separar por comas principales
      conds = condsInput
        .split(",")
        .map((c) => c.trim())
        .filter(Boolean);

      // validar cada una
      for (let c of conds) {
        if (!esCondicionValida(c)) {
          setError(
            `❌ Error: Condición inválida: "${c}". Usa formatos como y(0)=2 o y'(0)=1`
          );
          return;
        }
      }

      // normalizar cada condición (derivadas con ')
      const normalizedConds = conds.map((c) => normalizeCondition(c));
      setResultConditions(normalizedConds);
    }

    // todo OK -> setear para mostrar en procedimiento
    setResultExpression(normalizada);
    setError("");
  };

  return (
    <div className="container py-5">
      <h2 className="text-center mb-4">
        Calculadora de ecuaciones diferenciales de orden superior
      </h2>

      {/* Ingreso de ecuación */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h5 className="card-title">Ingresa tu ecuación</h5>

          <div className="input-group">
            <input
              type="text"
              className="form-control"
              placeholder="Ejemplo: y'' + 3y' + 2y = 0"
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />

            <button className="btn btn-danger" onClick={handleSend}>
              Ir
            </button>

            <select
              className="form-select"
              style={{ maxWidth: "180px" }}
              value={type}
              onChange={(e) => setType(e.target.value)}
            >
              <option value="Homogénea">Polinomio característico</option>
              <option value="No Homogénea">Variacón de parámetros</option>
              <option value="No Homogénea">Coeficientes indeterminados</option>
            </select>
          </div>

          <small className="text-muted"></small>
        </div>
      </div>

      {/* Condiciones iniciales */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h5 className="card-title">Condiciones iniciales</h5>

          <input
            type="text"
            className="form-control"
            placeholder="Ej: y(0)=2, y'(0)= -1"
            value={condsInput}
            onChange={(e) => setCondsInput(e.target.value)}
          />
          <small className="text-muted"></small>
        </div>
      </div>

      {/* Mensaje de error */}
      {error && <div className="alert alert-danger">{error}</div>}

      {/* Procedimiento */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h5 className="card-title">Procedimiento</h5>

          <div
            className="border p-3 bg-white rounded"
            style={{ minHeight: "120px" }}
          >
            {resultExpression ? (
              <>
                <p>
                  <strong>Ecuación normalizada:</strong>
                </p>
                <pre>{resultExpression}</pre>

                {resultConditions.length > 0 && (
                  <>
                    <p>
                      <strong>Condiciones iniciales:</strong>
                    </p>
                    <ul>
                      {resultConditions.map((c, i) => (
                        <li key={i}>
                          <pre>{c}</pre>
                        </li>
                      ))}
                    </ul>
                  </>
                )}
              </>
            ) : (
              <p className="text-muted">El procedimiento aparecerá aquí...</p>
            )}
          </div>
        </div>
      </div>

      {/* Gráfica */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h5 className="card-title">Gráfica</h5>
          <div
            className="border bg-white rounded d-flex justify-content-center align-items-center"
            style={{ height: "250px" }}
          >
            <span className="text-muted">Aquí se mostrará la gráfica</span>
          </div>
        </div>
      </div>

      <footer className="bg-dark text-white py-3 mt-5">
        <div className="container text-center">
          <p className="mb-1">Segundo Parcial Ecuaciones Diferenciales</p>
          <small>
            Desarrollado por Johan Uriel Marin Viñas – Angel Ariel García –
            Ulices Karsten Cruz – Derek Hernández Domínguez
          </small>
        </div>
      </footer>
    </div>
  );
}

export default EcDif;
