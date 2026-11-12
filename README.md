# Recibos de sueldo en hoja única

Reformatea los recibos de sueldo mensuales (PDF exportados del sistema de liquidación) para que **cada recibo entre en una sola hoja** y la **firma quede siempre en el mismo lugar**. No modifica ningún dato: recorta y reubica el contenido original como gráfico vectorial.

## Para quién
Administración / Contaduría de Grupo Leuk, que carga los recibos al sistema documental o los imprime para firma.

## Qué lee y qué escribe
- **Lee:** un PDF por razón social con el lote mensual (por ejemplo `Recibos de sueldos 10-2026 1.pdf`). Cada empleado tiene dos documentos: ORIGINAL y DUPLICADO, de 1 o 2 páginas físicas cada uno.
- **Escribe:** un PDF por razón social con `N empleados × 2` hojas, nombrado `Recibos MM-AAAA - <RAZÓN SOCIAL> - hoja unica.pdf`.
- Los PDF **no se versionan** (ver `.gitignore`): tienen CUIL, sueldos y datos personales.

## Cuándo corre
Una vez por liquidación, después de recibir el lote del sistema de liquidación. [A CONFIRMAR: periodicidad real y responsable]

## Uso paso a paso
1. Instalar dependencias: `pip install -r requirements.txt`
2. Generar: `python3 src/recibos_hoja_unica.py "entrada/Recibos 10-2026 - X.pdf" "salida/Recibos 10-2026 - X - hoja unica.pdf"`
   Imprime hojas de entrada y salida, rango de escalas aplicadas, cantidad de ORIGINAL/DUPLICADO y escalas menores a 0,75.
3. Verificar: `python3 src/verificar.py "entrada/...pdf" "salida/...pdf"`
4. Revisar a ojo al menos el recibo de menor escala (original y duplicado) y uno a escala 1.0.
5. Repetir por cada razón social (un PDF por CUIT).

## Qué verifica `verificar.py`
- **Integridad:** el texto de cada hoja de salida coincide, ordenado, con el de sus hojas de origen (sin los "Hoja X de Y"). Debe dar 0 diferencias.
- **Firma:** misma altura en todas las hojas (y = 745 pt); centro del ORIGINAL en x = 297,96 pt; extremo derecho del DUPLICADO en x = 557,5 pt (tolerancia ±0,5).
- **Márgenes:** nada de tinta fuera de página.
- **Conteo:** hojas de salida = empleados × 2.

## Qué hacer si falla
- **Diferencias de integridad:** no entregar. Revisar que el PDF de origen tenga capa de texto y que la agrupación hoja 1 / hoja 2 sea correcta.
- **Escala menor a 0,75:** avisar antes de entregar; el recibo tiene demasiado contenido para la franja disponible.
- **PDF sin capa de texto** (impreso a PDF): el tipo ORIGINAL/DUPLICADO se deduce por geometría y la verificación de integridad no aplica a esas hojas. Informarlo.
- **Dueño del proceso:** [A CONFIRMAR]
