# Notas

## Decisiones y por qué
- **Recorte vectorial con PyMuPDF (`show_pdf_page`)** en vez de regenerar el recibo: garantiza que los datos no cambien.
- **Detección de bloques por tinta (render 150 dpi), no por texto:** funciona también con PDF sin capa de texto.
- **Firma a escala 1.0 y a altura fija:** es lo que permite cargarla al sistema documental / firmarla siempre en el mismo lugar; lo que se achica es el bloque de datos.
- **Firma del empleado al margen derecho, la del empleador centrada**, tal como las definió la usuaria.

## Probado
- Lote de 98 páginas → 58 hojas (29 empleados), escalas 0,792–1,0, 0 diferencias de texto, firma en y 745,08–745,56 pt.
- Lote de 12 páginas → 6 hojas (3 empleados), escalas 0,811–0,830, 0 diferencias.

## Descartado / no hecho
- Un PDF por empleado y extracción de subconjuntos: se ofrecen, no se hacen por defecto.

## Pendiente
- [A CONFIRMAR] Periodicidad, responsable y ubicación real de los PDF de entrada y salida.
- [A CONFIRMAR] Si se quiere un ejemplo con datos ficticios en el repo.
- Observaciones de datos del lote original (fechas de aportes anteriores al ingreso, contribuciones negativas, codificación de la Ñ) se informaron a la usuaria; no se corrigieron porque el proceso no toca datos.
