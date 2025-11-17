function EcDif() {
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
            />
            <button className="btn btn-danger">Ir</button>
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
    </div>
  );
}

export default EcDif;
