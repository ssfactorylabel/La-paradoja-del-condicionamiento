"""
IEE Framework v0.2 - Índice de Impacto Estratégico
SSFLABS Research | Producto #2
DOI: 10.5281/zenodo.22262029

Objetivo: Calcular riesgo ANTES de generar respuesta.
Compatible con Muse Spark 1.3 Guardrails (tool output)

Formula: IEE 0.0-1.0 = Impacto si la respuesta es incorrecta
IEE >0.7 = activa fricción + [VERIFY] + cambio KPI a Trust 90d
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
import re

@dataclass
class IEEResult:
    score: float
    level: str # CRITICAL | HIGH | MEDIUM | LOW
    domain: str
    guardrail_action: str
    kpi: str

class IEEFramework:
    """
    Taxonomía IEE v0.2 - Basada en casos reales SSFactoryLabel
    Validación: Samsung A07 - Caso IEE 0.92 documentado
    """

    TAXONOMY = {
        # IEE 90-100 - CRITICAL: Una alucinación = -90% trust
        "CRITICAL": {
            "score": 0.92,
            "domains": ["health_dosage", "health_diagnosis", "legal_contract", "finance_investment", "safety"],
            "keywords": [
                "dosis", "diagnostico", "sintoma", "medicina", "ibuprofeno", "tratamiento",
                "abogado", "contrato", "demanda", "ley", "juicio",
                "invertir", "dinero", "hipoteca", "trading", "cripto",
                "emergencia", "suicidio", "peligro"
            ],
            "action": "[VERIFY] + Cite 2 sources + Suggest human validation",
            "kpi": "Trust_90d"
        },
        # IEE 50-89 - HIGH: Decisión importante
        "HIGH": {
            "score": 0.65,
            "domains": ["work", "education", "career", "relationship"],
            "keywords": [
                "trabajo", "entrevista", "despido", "renuncia", "carrera",
                "estudiar", "universidad", "examen", "tesis",
                "decision", "deberia", "romper", "divorcio"
            ],
            "action": "Pros/Cons + Avoid absolute tone + Provide options",
            "kpi": "Trust_90d"
        },
        # IEE 0-49 - LOW: Creativo
        "LOW": {
            "score": 0.25,
            "domains": ["entertainment", "ideas", "creative", "general"],
            "keywords": [],
            "action": "Normal creative mode",
            "kpi": "Engagement"
        }
    }

    @staticmethod
    def calcular_iee(prompt: str) -> IEEResult:
        """Calcula IEE antes de generar. Esta es la función que se integra a Muse Spark 1.3"""
        prompt_lower = prompt.lower()

        # Check CRITICAL primero
        for level_name in ["CRITICAL", "HIGH"]:
            level = IEEFramework.TAXONOMY[level_name]
            for kw in level["keywords"]:
                if re.search(r'\b' + re.escape(kw) + r'\b', prompt_lower):
                    return IEEResult(
                        score=level["score"],
                        level=level_name,
                        domain=level["domains"][0],
                        guardrail_action=level["action"],
                        kpi=level["kpi"]
                    )

        # Default LOW
        low = IEEFramework.TAXONOMY["LOW"]
        return IEEResult(
            score=low["score"],
            level="LOW",
            domain="general",
            guardrail_action=low["action"],
            kpi=low["kpi"]
        )

    @staticmethod
    def aplicar_guardrail(prompt: str, respuesta: str, iee_result: IEEResult) -> Dict:
        """
        Aplica fricción según IEE. Este output es compatible con RLHF v2 reward.
        """
        if iee_result.score > 0.7:
            # Modo Confianza - Muse Spark 1.3 safety improvement lo hace mejor
            respuesta_final = (
                f"[VERIFY - IEE {iee_result.score:.2f} / {iee_result.level}] {respuesta}\n\n"
                f"---\n"
                f"**Dominio:** {iee_result.domain} | **Impacto:** Alto\n"
                f"**Acción requerida:** Valide con fuente oficial o profesional.\n"
                f"**Confianza del modelo:** Declarada {iee_result.score*100:.0f}% - Requiere validación humana."
            )
            return {
                "respuesta": respuesta_final,
                "modo": "Trust_Mode",
                "iee": iee_result.score,
                "level": iee_result.level,
                "kpi": "90-Day Trust",
                "reward_signal": "truth+utility",
                "should_log": True
            }
        else:
            return {
                "respuesta": respuesta,
                "modo": "Engagement_Mode",
                "iee": iee_result.score,
                "level": iee_result.level,
                "kpi": "Responses/Session",
                "reward_signal": "satisfaction",
                "should_log": False
            }

# Demo factory - corre esto para probar
if __name__ == "__main__":
    tests = [
        "¿Qué dosis de ibuprofeno para un niño de 5 años?",
        "¿Cómo redacto mi contrato de alquiler en Madrid?",
        "¿Debería invertir $10k en NVDA ahora?",
        "¿Cómo preparo mi entrevista de trabajo en Scale?",
        "Cuéntame un chiste de programadores"
    ]

    framework = IEEFramework()

    print("=== SSFLABS IEE Framework v0.2 Demo ===\n")
    for prompt in tests:
        result = framework.calcular_iee(prompt)
        output = framework.aplicar_guardrail(prompt, "[Respuesta del modelo aquí]", result)
        print(f"Prompt: {prompt}")
        print(f" -> IEE: {result.score} | Level: {result.level} | KPI: {output['kpi']}")
        print(f" -> Action: {result.guardrail_action}\n")
