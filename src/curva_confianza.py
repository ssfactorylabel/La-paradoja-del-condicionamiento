"""
LA PARADOJA DEL CONDICIONAMIENTO - Curva de Confianza
SSFLABS Research | DOI: 10.5281/zenodo.22262029
Validado: Samsung A07 + Muse Spark 1.1 / 1.3 Ready

Formula: Trust(t+1) = Trust(t) + 0.05 - 0.6 * IEE * Hallucination
Figura 1 del memo: 40 dias +0.05, 1 dia -0.6 con IEE=0.92
"""

import matplotlib.pyplot as plt
import numpy as np
import os

def generar_curva_confianza(
    dias_totales=50,
    incremento_diario=0.05,
    dia_alucinacion=40,
    impacto_alucinacion=0.6,
    iee=0.92,
    output_path="curva_confianza_ia_corporate.webp"
):
    # 1. Datos
    dias = np.arange(0, dias_totales + 1)
    confianza = np.zeros_like(dias, dtype=float)

    # Construccion lenta
    for i in range(1, len(dias)):
        confianza[i] = confianza[i-1] + incremento_diario

    # Limite de confianza max (saturacion)
    confianza = np.minimum(confianza, 2.0)

    # Caida por alucinacion en IEE alto
    caida = impacto_alucinacion * iee # 0.6 * 0.92 = 0.552
    confianza[dia_alucinacion:] = confianza[dia_alucinacion:] - caida

    # 2. Plot Corporate Style
    plt.figure(figsize=(10, 6), dpi=300)
    plt.plot(dias, confianza, color='#1F77B4', linewidth=3, label='Trust Score')

    # Linea del evento critico
    plt.axvline(x=dia_alucinacion, color='#D62728', linestyle='--', linewidth=1.5, alpha=0.7, label=f'Critical Hallucination IEE={iee}')

    # Anotacion
    plt.annotate(
        f'-{caida:.2f} Alucinación\nIEE {iee} (Salud/Finanzas)',
        xy=(dia_alucinacion, confianza[dia_alucinacion]),
        xytext=(dia_alucinacion + 2, confianza[dia_alucinacion] - 0.5),
        arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8),
        fontsize=10, weight='bold',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray")
    )

    plt.title('La Paradoja del Condicionamiento: Confianza como Deuda Técnica', fontsize=13, weight='bold', pad=20)
    plt.xlabel('Días de Interacción (construcción de confianza)', fontsize=11)
    plt.ylabel('Nivel de Confianza Acumulada', fontsize=11)
    plt.grid(True, alpha=0.3, linestyle=':')
    plt.legend(loc='lower right')
    plt.tight_layout()

    # 3. Guardar - path robusto
    # Si se corre desde src/, guarda en raiz. Si se corre desde raiz, guarda en raiz.
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if os.path.basename(os.getcwd()) == 'src' else os.getcwd()
    # fallback simple
    final_path = output_path
    if not os.path.isabs(output_path):
        # intenta guardar en raiz del proyecto
        root_candidate = os.path.join(os.path.dirname(__file__), '..', output_path)
        final_path = os.path.abspath(root_candidate)

    # Asegura que exista
    os.makedirs(os.path.dirname(final_path) if os.path.dirname(final_path) else '.', exist_ok=True)

    plt.savefig(final_path, dpi=300, bbox_inches='tight', format='webp')
    print(f"[SSFLABS] Gráfica guardada: {final_path}")
    print(f"Formula: Trust(t+1) = Trust(t) + {incremento_diario} - {impacto_alucinacion} * {iee} * Hallucination")
    print(f"Caida real aplicada: -{caida:.3f}")
    return final_path

if __name__ == "__main__":
    generar_curva_confianza()
