import { MathJax, MathJaxContext } from "better-react-mathjax";

export default function ResultadoEDO({ data }) {
  if (!data) return null;

  const Bloque = ({ titulo, children }) => (
    <div style={{
      background: "#fff",
      borderRadius: "12px",
      padding: "16px",
      marginBottom: "20px",
      boxShadow: "0 2px 10px rgba(0,0,0,0.08)",
    }}>
      <h3 style={{ margin: 0, marginBottom: "12px", color: "#333", fontSize: "1.1em" }}>
        {titulo}
      </h3>
      {children}
    </div>
  );

  const getLatex = (item) => (typeof item === "string" ? item : item.latex || "");

  return (
    <MathJaxContext>
      <div style={{ marginTop: "30px" }}>

        {/* RAÍCES */}
        {(data.lambdas || data.raices) && (
          <Bloque titulo="Raíces del polinomio característico">
            {(data.lambdas || data.raices).map((item, i) => (
              <div key={i} style={{ margin: "8px 0" }}>
                <MathJax inline>{`\\lambda_{${i + 1}} = ${getLatex(item)}`}</MathJax>
              </div>
            ))}
          </Bloque>
        )}

        {/* POLINOMIO */}
        {data.polinomio && (
          <Bloque titulo="Polinomio característico">
            <MathJax inline>{getLatex(data.polinomio)}</MathJax>
          </Bloque>
        )}

        {/* SOLUCIÓN HOMOGÉNEA */}
        {data.solucion_homogenea && (
          <Bloque titulo="Solución homogénea">
            <MathJax inline>{`y_h(x) = ${getLatex(data.solucion_homogenea)}`}</MathJax>
          </Bloque>
        )}

        {/* SOLUCIÓN PARTICULAR */}
        {data.solucion_particular && (
          <Bloque titulo="Solución particular">
            <MathJax inline>{`y_p(x) = ${getLatex(data.solucion_particular)}`}</MathJax>
          </Bloque>
        )}

        {/* SOLUCIÓN GENERAL */}
        {data.solucion_general && !data.solucion_con_condiciones && (
          <Bloque titulo="Solución general">
            <MathJax inline>{`y(x) = ${getLatex(data.solucion_general)}`}</MathJax>
          </Bloque>
        )}

        {/* SOLUCIÓN CON CONDICIONES */}
        {data.solucion_con_condiciones && (
          <Bloque titulo="Solución con condiciones iniciales">
            <MathJax inline>{`y(x) = ${getLatex(data.solucion_con_condiciones)}`}</MathJax>
          </Bloque>
        )}

        {/* PASOS */}
        {data.pasos && (
          <Bloque titulo="Pasos detallados">
            {data.pasos.wronskiano && (
              <div>
                <strong>Wronskiano:</strong>{" "}
                <MathJax inline>{`W = ${data.pasos.wronskiano}`}</MathJax>
              </div>
            )}
            {data.pasos.u_primas && (
              <>
                <br />
                <strong>u'(x):</strong><br />
                {data.pasos.u_primas.map((u, i) => (
                  <MathJax inline key={i}>{`u'_{${i+1}} = ${u}`}</MathJax>
                ))}
              </>
            )}
            {data.pasos.u_integradas && (
              <>
                <br /><br />
                <strong>u(x):</strong><br />
                {data.pasos.u_integradas.map((u, i) => (
                  <MathJax inline key={i}>{`u_{${i+1}} = ${u}`}</MathJax>
                ))}
              </>
            )}
          </Bloque>
        )}

        {data.error && (
          <Bloque titulo="Error">
            <p style={{ color: "red" }}>{data.error}</p>
          </Bloque>
        )}

      </div>
    </MathJaxContext>
  );
}