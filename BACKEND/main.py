from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List
from LOGIC.variacion_parametros import *
import sympy as sp
from models.request_models import VariacionParametrosRequest
from models.request_models import CoefIndRequest
from LOGIC.coef_indet import resolver_coeficientes_indeterminados
from models.request_models import PolinomioCaracteristicoRequest
from LOGIC.polinomio_caracteristico import EDHomogenea
from util.formatear_expresion import normalize_expr



class prueba(BaseModel):
    respuesta : str


app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

x = sp.symbols("x")


@app.post("/variacion_parametros")
def resolver_variacion_parametros(req: VariacionParametrosRequest):

    fx_expr = sp.sympify(req.fx)

    # 1. obtener homogénea
    y_h, sols, lambdas = solucion_homogenea(req.coeficientes)

    # 2. variación de parámetros
    y_p, pasos = variacion_parametros(sols, fx_expr, x)

    if "error" in pasos:
        return pasos  # Wronskiano cero, etc

    # 3. solución general
    y_g = solucion_general(y_h, y_p)

    # 4. simplificar
    y_g_simplificada = simplificar_general(y_g, x)


    return {
    "lambdas": [normalize_expr(l) for l in lambdas],
    "soluciones_homogeneas": [normalize_expr(s) for s in sols],
    "solucion_homogenea": normalize_expr(y_h),
    "solucion_particular": normalize_expr(y_p),
    "solucion_general": normalize_expr(y_g_simplificada),
    "solucion_general": normalize_expr(y_g_simplificada),
    "pasos": pasos
    }

@app.post("/coeficientes_indeterminados")

def api_coef_ind(req: CoefIndRequest):
    try:
        out = resolver_coeficientes_indeterminados({
            "coeficientes": req.coeficientes,
            "g": req.g,
            "condiciones": req.condiciones,
            "paso_a_paso": req.paso_a_paso
        })

        if out.get("error"):
            raise HTTPException(status_code=400, detail=out["error"])

        return out  

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/polinomio-caracteristico")
def resolver_polinomio_caracteristico(payload: PolinomioCaracteristicoRequest):
    solver = EDHomogenea()
    base = solver.resolver_polinomio_caracteristico(payload.coeficientes)

    response = {
        "metodo": "polinomio_caracteristico",
        "polinomio": base["polinomio"],           
        "raices": base["raices"],                 
        "solucion_general": base["solucion"],     
    }

    if payload.condiciones:
        resultado_ci = solver.resolver_con_condiciones_iniciales(
            payload.coeficientes, payload.condiciones
        )
        if "error" in resultado_ci:
            raise HTTPException(status_code=400, detail=resultado_ci["error"])
        response["solucion_con_condiciones"] = resultado_ci  

    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


