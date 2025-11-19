import { useState } from "react";

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

  return normalizar;
}

//Caracteres permitidos

function esValida(expr) {
  const patron = /^[0-9x-yz+\-*/^().\s\|a-z]+$/i;

  const funcionesValidados = [
    "sin",
    "cos",
    "tan",
    "sqrt",
    "log",
    "ln",
    "exp",
    "diff",
    "x",
    "y",
    "z",
  ];

  const palabras = expr.toLowerCase().match(/\b[a-zñáéíóú]+\b/g);

  if (!palabras) return true;

  for (let p of palabras) {
    if (!funcionesValidados.includes(p)) {
      return false;
    }
  }

  return true;
}
function EcDif() {
  const [input, setInput] = useState("");
  const [type, setType] = useState("Homogénea");
  const [resultExpression, setResultExpression] = useState("");
  const [error, setError] = useState("");

  const handleSend = () => {
    // Validar sintaxis básica
    if (!esValida(input)) {
      setError("Error: La ecuación contiene caracteres no válidos.");
      setResultExpression("");
      return;
    }

    const normalizada = validarExpresiones(input);

    // Si quedó vacía o sin sentido
    if (!normalizada || normalizada.trim() === "") {
      setError("Error: La ecuación no es válida.");
      setResultExpression("");
      return;
    }

    setError("");
    setResultExpression(normalizada);
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
              <option value="Homogénea">Homogénea</option>
              <option value="No homogénea">No homogénea</option>
            </select>
          </div>

          {error && <p className="text-danger mt-2">{error}</p>}
        </div>
      </div>

      {/* Procedimiento */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h5 className="card-title">Procedimiento</h5>

          <div
            className="border p-3 bg-white rounded"
            style={{ minHeight: "120px" }}
          >
            {resultExpression ? (
              <p>{resultExpression}</p>
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
