"""
Framework IEE v0.1: Indice de Impacto Emocional
Simula como un LLM detectaria el riesgo antes de responder.
"""

def calcular_iee(prompt: str) -> float:
    """Retorna score entre 0.0 y 1.0"""
    prompt_lower = prompt.lower()
    palabras_alto = ["diagnostico", "abogado", "invertir", "dosis", "contrato", "ley", "dinero"]
    palabras_medio = ["trabajo", "entrevista", "estudiar", "decision", "carrera"]

    if any(p in prompt_lower for p in palabras_alto): return 0.92 # IEE Alto
    if any(p in prompt_lower for p in palabras_medio): return 0.65 # IEE Medio
    return 0.25 # IEE Bajo

def aplicar_guardrail(prompt: str, respuesta: str, iee_score: float) -> dict:
    """Si IEE > 0.7 aplicamos friccion"""
    if iee_score > 0.7:
        return {
            "respuesta": f"[VERIFICAR CON FUENTE] {respuesta} \n\n*Nivel de confianza: {iee_score*100:.0f}%. Recomiendo validar con profesional.*",
            "modo": "Confianza",
            "accion": "Citar fuentes + Friccion"
        }
    else:
        return {"respuesta": respuesta, "modo": "Engagement", "accion": "Respuesta directa"}

# Demo
if __name__ == "__main__":
    prompt = "¿Qué dosis de ibuprofeno para un niño de 5 años?"
    iee = calcular_iee(prompt)
    print(aplicar_guardrail(prompt, "La dosis es 10mg...", iee))
