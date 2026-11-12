# Reglas del proyecto (recibos de sueldo en hoja única)

Leé esto antes de tocar el código. Son los criterios acordados con la usuaria (contadora/auditora de Grupo Leuk).

## Regla innegociable
**Nunca reescribir ni recalcular datos.** Se recorta y se reubica como gráfico vectorial del PDF original. Cambian márgenes y escala, jamás importes, nombres, CUIL, conceptos ni marcadores internos del sistema (`#R1#`, `#R31#`, etc.). Si algo no entra, se reduce la escala; no se elimina ni se resume nada.

## Firma
- Línea de firma siempre a **y = 745 pt, escala 1.0**.
- ORIGINAL ("FIRMA DEL EMPLEADOR"): línea **centrada**, centro en x = 297,96 pt.
- DUPLICADO ("FIRMA DEL EMPLEADO"): extremo derecho de la línea en **x = 557,5 pt**. El texto "RECIBÍ…" viaja en la misma banda, a la izquierda; la banda no se parte.

## Composición
- Misma franja horizontal de recorte (x 26,5 a 569,5) en todos los PDF.
- Una escala por recibo: `min(1.0, espacio_disponible / alto_total)`. Nunca agrandar. Si baja de 0,75, avisar.
- "Hoja 1 de 1" en gris en el pie.
- Reemplazos de recibos sueltos: sustituir original y duplicado en la misma posición alfabética, no al final.

## Verificación obligatoria antes de entregar
Integridad de texto (0 diferencias), posición de firma, nada recortado, conteo = empleados × 2, y revisión visual del recibo más comprimido. La comparación de texto no detecta recortes: la revisión visual no se saltea.

## Salida y datos
- Un PDF por razón social/CUIT, orden alfabético: `Recibos MM-AAAA - <RAZÓN SOCIAL> - hoja unica.pdf`.
- **Nunca subir PDF de recibos al repo** (datos personales). Para ejemplos, usar datos ficticios.
- Ofrecer, sin darlo por hecho: un PDF por empleado o extracción de un subconjunto.

## Estilo
Español rioplatense, terminología contable precisa. No inventar datos; marcar lo que requiere confirmación.
