from pydantic import BaseModel
from typing import List
from typing import List, Optional, Dict, Any

class VariacionParametrosRequest(BaseModel):
    coeficientes: List[float]   # ecuación homogénea
    fx: str                     # f(x) como string, ej: "exp(x)"

class CoefIndRequest(BaseModel):
    coeficientes: List[float]
    g: str
    condiciones: Optional[Dict[str, float]] = None
    paso_a_paso: Optional[bool] = True


class PolinomioCaracteristicoRequest(BaseModel):
    coeficientes: List[float]
    condiciones: Optional[Dict[str, float]] = None  # Puede ir vacío
