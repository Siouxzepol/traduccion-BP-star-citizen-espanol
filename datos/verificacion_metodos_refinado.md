# Verificación de los métodos de refinado

Prueba realizada en LIVE el 26/10/2026 en **Wide Forest Station ARC-L1**, con el mismo manifiesto de **3.050 cSCU** y el mismo mineral, **Beryl**, para evitar comparar condiciones distintas.

La clasificación de coste y rendimiento se obtiene de los resultados numéricos del propio juego. La velocidad conserva el nivel cualitativo de la tabla de referencia y se acompaña del tiempo medido. En `Thermonatic Deposition` la captura no llegó a calcular el pedido y mostró `--`; por eso sus cifras siguen pendientes de una segunda captura.

| Método | Velocidad | Coste | Rendimiento | Coste medido | Tiempo medido | Salida observada |
|---|---|---|---|---:|---:|---:|
| Cormack Method | Alta | Moderado | Bajo | 2.806 aUEC | 4 m 30 s | 1.026 |
| Dinyx Solventation | Muy baja | Bajo | Alto | 1.403 aUEC | 3 h 36 m | 1.466 |
| Electrostarolysis | Moderada | Moderado | Moderado | 2.806 aUEC | 18 m 2 s | 1.246 |
| Gaskin Process | Alta | Alto | Moderado | 8.418 aUEC | 9 m 1 s | 1.246 |
| Pyrometric Chromalysis | Baja | Alto | Alto | 8.418 aUEC | 36 m 5 s | 1.466 |
| Kazen Winnowing | Moderada | Bajo | Bajo | 1.403 aUEC | 13 m 31 s | 1.026 |
| Thermonatic Deposition | Baja | Bajo | Moderado | Pendiente | Pendiente | Pendiente |
| Ferron Exchange | Baja | Moderado | Alto | 2.806 aUEC | 1 h 12 m | 1.466 |
| XCR Reaction | Alta | Alto | Bajo | 8.418 aUEC | 2 m 15 s | 1.026 |

## Escalas comprobadas

- Coste bajo: 1.403 aUEC.
- Coste moderado: 2.806 aUEC.
- Coste alto: 8.418 aUEC.
- Rendimiento bajo: salida total observada de 1.026.
- Rendimiento moderado: salida total observada de 1.246.
- Rendimiento alto: salida total observada de 1.466.

La tabla web coincide con las ocho pruebas que sí devolvieron cifras. Las discrepancias procedían de siete rótulos `_Details` cruzados en la copia instalada de la traducción, no de los resultados calculados por el juego.
