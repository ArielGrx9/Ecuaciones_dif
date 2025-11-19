import { useState } from "react";

function validarExpreciones(expr) {
  let normalizar = expr.toLowerCase();
  // ach dime si quieres mas mmds despues de las 7:30 no puedo

  //Derivada
  normalizar = normalizar.replace(/\bdev\b/g, "der");

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
  // Notación como √x
  normalizar = normalizar.replace(/√\(/g, "sqrt(");
  normalizar = normalizar.replace(/√([a-z0-9]+)/gi, "sqrt($1)");

  // Logaritmos
  normalizar = normalizar.replace(/\blogaritmo\b/g, "log");
  normalizar = normalizar.replace(/\blog10\b/g, "log10");
  normalizar = normalizar.replace(/\bln\b/g, "ln");
  normalizar = normalizar.replace(/\blog natural\b/g, "ln");

  // Variaciones de "e"
  normalizar = normalizar.replace(/\be\^/g, "exp("); // e^x → exp(x
  normalizar = normalizar.replace(/\bexp\(/g, "exp("); // exp → exp

  // e^x sin paréntesis: e^x → exp(x)
  normalizar = normalizar.replace(/e\^([a-z0-9]+)/g, "exp($1)");

  // potencias
  normalizar = normalizar.replace(/\bcuadrado\b/g, "^2");
  normalizar = normalizar.replace(/\bcubico\b/g, "^3");
  normalizar = normalizar.replace(/\bcúbico\b/g, "^3");

  normalizar = normalizar.replace(/\bpi\b/g, "pi"); // ya normal
  normalizar = normalizar.replace(/\bπ\b/g, "pi");

  // y''''  -> diff(y, x, 4)
  normalizar = normalizar.replace(/([a-z])''''\b/g, "diff($1, x, 4)");

  // y'''  -> diff(y, x, 3)
  normalizar = normalizar.replace(/([a-z])'''\b/g, "diff($1, x, 3)");

  // y''  -> diff(y, x, 2)
  normalizar = normalizar.replace(/([a-z])''\b/g, "diff($1, x, 2)");

  // y'  -> diff(y, x)
  normalizar = normalizar.replace(/([a-z])'\b/g, "diff($1, x)");

  return normalizar;
}

function EcDif() {
  const [input, setInput] = useState("");
  const [type, setType] = useState("Homogénea");
  const [resultExpression, setResultExpression] = useState("");

  const handleSend = () => {
    const normalizar = validarExpreciones(input);
    console.log(normalizar);
    console.log(input);
    console.log(type);
    setResultExpression(normalizar);
  };

  return (
    <div className="container py-5">
      {/* Título */}
      <h2 className="text-center mb-4">
        Calculadora de ecuaciones diferenciales de orden superior
      </h2>

      {/* Ingreso de función */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h5 className="card-title">Ingresa tu ecuación</h5>

          <div className="input-group">
            <input
              type="text"
              className="form-control"
              placeholder="f(x) = ..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />

            {/* Boton */}
            <button className="btn btn-danger" onChange={handleSend}>
              Ir
            </button>

            {/* Menu */}
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

          <small className="text-muted">Ejemplo: x^2 + 3x - 2</small>
        </div>
      </div>

      {/* Condiciones iniciales */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h5 className="card-title">Condiciones iniciales</h5>

          <input
            type="text"
            className="form-control"
            placeholder="Ej: x(0) = 2, x'(0) = -1"
          />
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
            <p className="text-muted">El procedimiento aparecerá aquí...</p>
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
            Desarrollado por Johan Uriel Marin Viñas Angel Ariel Garcia Ulices
            Karsten Cruz Dereck
          </small>
        </div>
      </footer>
    </div>
  );
}

export default EcDif;
