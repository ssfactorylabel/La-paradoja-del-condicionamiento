# LA PARADOJA DEL CONDICIONAMIENTO
### Cómo llevamos RLHF al siguiente nivel: De Engagement a Confianza

**Autor:** Andrés Garbán Hernández | ssfactorylabel Research  
**Fecha:** Julio 2026

---

## El Problema en 1 Línea
Los LLMs actuales optimizan por "engagement". El siguiente moat de 100B es optimizar por "confianza".

Una sola alucinación destruye 40 días de confianza construida.

`Confianza(t+1) = Confianza(t) + 0.05 - 0.6 * IEE * Alucinación`

![Curva de Confianza](curva_confianza_ia_corporate.webp)

*Gráfica 1: 40 días construyendo +0.05. 1 día la destruye -0.6 con IEE Alto.*

## La Solución: Framework IEE
Propongo 3 cambios para que Scale lidere "IA Confiable":

1.  **IEE - Índice de Impacto Emocional:** Detectar riesgo antes de responder. Salud/Ley/Finanzas = IEE > 0.7
2.  **Guardrails de Fricción:** Si IEE alto, el modelo declara confianza, cita 2 fuentes y sugiere validación humana.
3.  **Nuevo KPI:** Medir "Confianza a 90 días" en vez de "Respuestas por sesión".

## Este Repositorio
- `LA_PARADOJA_DEL_CONDICIONAMIENTO_MEMO.pdf` - Memo completo de 5 páginas para el board
- `src/iee_calculator.py` - Prototipo v0.1 del Framework IEE en Python
- `src/curva_confianza.py` - Código para regenerar la gráfica

## El Ask a Scale AI
Buscamos piloto de 30 días para correr IEE en 10k prompts de Salud + Finanzas.  
**Objetivo:** +15% en "intención de volver a usar" en prompts de alto riesgo.

## Conclusión
Scale no solo vende "data". Puede vender **"seguro de confianza para IA"**.  
El mundo no necesita solo IA más grande. Necesita IA a la que le podamos delegar.

---
### Conectemos
Si trabajas en AI Safety, RLHF, o Producto en Scale, Anthropic, OpenAI: hablemos.  
Este es el siguiente paso.
