import matplotlib.pyplot as plt
import numpy as np

dias = np.arange(0, 51)
confianza = np.minimum(dias * 0.05, 2.0)
confianza[40:] = confianza[40] - 0.6 # Caida

plt.figure(figsize=(10, 6))
plt.plot(dias, confianza, color='#1f77b4', linewidth=3)
plt.axvline(x=40, color='gray', linestyle='--')
plt.annotate('-0.6 Alucinacion IEE 0.92', xy=(40, confianza[40]), xytext=(42, 1.0), arrowprops=dict(facecolor='black'))
plt.title('Curva de Confianza en IA', weight='bold')
plt.xlabel('Dias'); plt.ylabel('Nivel de Confianza'); plt.grid(True, alpha=0.3)
plt.savefig('../curva_confianza_ia_corporate.webp', dpi=300, bbox_inches='tight')
print("Grafica guardada")
