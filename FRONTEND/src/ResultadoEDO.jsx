import { MathJax, MathJaxContext } from "better-react-mathjax";

export default function ResultadoEDO({ data }) {
  if (!data) return null;

  const Bloque = ({ titulo, children }) => (
    <div
      style={{
        background: "#fff",
        borderRadius: "12px",
        padding: "16px",
        marginBottom: "20px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.08)",
      }}
    >
      <h3 style={{ margin: 0, marginBottom: "12px", color: "#333", fontSize: "1.1em" }}>
        {titulo}
      </h3>
      {children}
    </div>
  );

  // LA FUNCIÓN MÁS FUERTE QUE EXISTE EN EL UNIVERSO
  const getLatex = (item) => {
    if (!item) return "";
    if (typeof item === "string") return item;
    if (item && typeof item === "object") {
      if (item.latex) return item.latex;
      if (item.plain) return item.plain;
      if (item.toString) return item.toString();
    }
    return String(item);
  };

  // CONVIERTE CUALQUIER COSA EN ARRAY
  const toArray = (thing) => {
    if (!thing) return [];
    if (Array.isArray(thing)) return thing;
    if (typeof thing === "object" && thing !== null) {
      return Object.keys(thing).map(key => thing[key]);
    }
    return [thing];
  };

  const raices = toArray(data.lambdas || data.raices || []);

  return (
    <MathJaxContext>
      <div style={{ marginTop: "30px" }}>

        {/* RAÍCES */}
        {raices.length > 0 && (
          <Bloque titulo="Raíces del polinomio característico">
            {raices.map((item, i) => (
              <div key={i} style={{ margin: "8px 0" }}>
                <MathJax inline>{`\\(\\lambda_{${i + 1}} = ${getLatex(item)}\\)`}</MathJax>
              </div>
            ))}
          </Bloque>
        )}

        {/* POLINOMIO */}
        {data.polinomio && (
          <Bloque titulo="Polinomio característico">
            <MathJax inline>{`\\(${getLatex(data.polinomio)}\\)`}</MathJax>
          </Bloque>
        )}

        {/* SOLUCIÓN HOMOGÉNEA */}
        {data.solucion_homogenea && (
          <Bloque titulo="Solución homogénea">
            <MathJax inline>{`\\(y_h(x) = ${getLatex(data.solucion_homogenea)}\\)`}</MathJax>
          </Bloque>
        )}

        {/* SOLUCIÓN PARTICULAR */}
        {data.solucion_particular && (
          <Bloque titulo="Solución particular">
            <MathJax inline>{`\\(y_p(x) = ${getLatex(data.solucion_particular)}\\)`}</MathJax>
          </Bloque>
        )}

        {/* SOLUCIÓN GENERAL */}
        {(data.solucion_general || data.y_general) && (
          <Bloque titulo="Solución general">
            <MathJax inline>{`\\(y(x) = ${getLatex(data.solucion_general || data.y_general)}\\)`}</MathJax>
          </Bloque>
        )}

        {/* CON CONDICIONES INICIALES */}
        {data.solucion_con_condiciones && (
          <Bloque titulo="Solución con condiciones iniciales">
            <MathJax inline>{`\\(y(x) = ${getLatex(data.solucion_con_condiciones)}\\)`}</MathJax>
          </Bloque>
        )}

      </div>
    </MathJaxContext>
  );
}