import sympy as sp

def normalize_expr(expr):
    if expr is None:
        return {"latex": "", "plain": ""}
    
    try:
        if isinstance(expr, str):
            expr = sp.sympify(expr, locals={"x": sp.symbols("x"), "t": sp.symbols("t")})
        
        # En SymPy 1.14+ ya usa e^{2x} y \ln(x) por defecto, solo limpiamos lo feo
        latex = sp.latex(expr, mode='inline', fold_short_frac=True)
        
        # Solo quitamos \left y \right que SymPy mete de más
        latex = latex.replace(r'\left', '').replace(r'\right', '')
        
        # Bonus: si por algún motivo queda \exp, lo cambiamos manualmente
        if r'\exp' in latex:
            latex = latex.replace(r'\exp', 'e^{')
        
        return {
            "latex": latex,
            "plain": str(expr)
        }
        
    except Exception as e:
        return {
            "latex": f"\\text{{Error: {str(e)}}}",
            "plain": str(expr) if expr else "Error"
        }