# Guía de revisión de la interfaz

Estado: 23/10/2026. Esta guía registra qué pantalla se está revisando; **«parcial» no significa que toda la sección esté terminada**. El catálogo `global.ini` contiene unas 91.000 entradas, incluidas misiones, diálogos, objetos y nombres propios. Que una cadena coincida con el original inglés no demuestra por sí solo que falte traducirla.

| Sección visible en el juego | Familias principales del catálogo | Estado | Trabajo comprobado |
| --- | --- | --- | --- |
| Cabina, HUD y avisos de vuelo | `DXSM_`, `DXSH_`, `HUD_`, `dfm_ui_`, `mfd_` | Parcial | Avisos de escudos y misiles; etiquetas de resultados y escaneo; armamento, reaparición, autodestrucción y estados de salto/acoplamiento. Revisadas las entradas `mfd_` y varias `UI_MF_`. Corregidos avisos de presión atmosférica, esclusa y fijación de misiles; distinguidos la carga y la calibración del motor cuántico. Revisadas varias categorías de escaneo, instrucciones de aterrizaje, mensajes de baliza de rescate/incapacitación y avisos de zonas legales. Primer repaso de mensajes de objetivo por fabricante; detectados errores de sentido en CNOU y Drake. En MISC se corrigieron 42 avisos de vuelo y en ANVL, 8. En AEGS se corrigieron 38 avisos cotejados con el original: contramedidas, acoplamiento, aterrizaje, sectores del escudo, comunicaciones y armamento. Falta contrastar estas cadenas dentro del juego y continuar con el resto de fabricantes. |
| mobiGlas: contratos, diario y notificaciones | `MG_`, `mobiGlas_`, `MissionManager_`, `Notification_` | Parcial | Varias fichas de misión y textos del diario; falta revisar cada pestaña como pantalla. |
| Minería, reciclaje y carga | `HUD_`, `DXSM_`, `UI_` | Parcial | Términos SCU y algunas etiquetas vistas en capturas; falta un repaso sistemático. |
| Inventario, tiendas y refinería | `UI_`, `shop_`, `itemPort_`, `port_`, `vehicle_focus_`, `vehicle_class_`, `kiosk_` | Parcial | Algunas etiquetas de refinería. En la tienda de naves, identificado que enfoque y clase se concatenan: corregidas combinaciones duplicadas como «Transporte: Pasajeros» y «Competición: Carreras». Comparadas todas las clases `vehicle_class_` con el original; traducidos «Carrier» y «Snub Carrier», corregido «Courier» y unificadas dos clases compuestas. La pantalla inicial de Buy-&-Fly sigue mostrando «TOUCH SCREEN TO START» aunque `kiosk_TouchStart` ya está traducida tanto en el repositorio como en el archivo instalado; no se ha identificado otra cadena en `global.ini` que explique esa pantalla. Queda pendiente comprobar si ese rótulo procede de un recurso de interfaz ajeno al catálogo. Falta comprobar el resultado en el juego y revisar el resto de inventario y tiendas. |
| Menús, ajustes y controles | `UI_`, `PAUSE_`, `input_` | Parcial | Dos opciones sociales corregidas en el primer barrido; falta revisar los menús completos. |
| Interacciones, ascensores y terminales | `UI_`, `HUD_` y claves específicas | Parcial | Casos señalados en capturas; falta comprobar el resto de naves y terminales. |
| Textos de misiones y diálogos | Claves de cada personaje o facción | En curso | Battaglia revisado por bloques; Bit Zeros iniciado. Restituida en «Golpe en el espacio profundo» (Headhunters) la sección de planos posibles y detalles de misión omitidos en español; el plano está garantizado, pero el modelo concreto sale de un grupo regional. Auditados los 313 títulos marcados `[BP]`: las 300 descripciones directas y las variantes de las otras 13 familias ya enumeran los planos posibles. No equivale a una revisión completa de la interfaz. |

## Orden de trabajo

1. Cabina y HUD: avisos, armamento, escaneo, MFD y etiquetas de objetivos.
2. mobiGlas: inicio, contratos, diario, mapas, vehículos y reputación.
3. Minería, reciclaje y carga: mensajes contextuales y unidades.
4. Inventario, tiendas, refinería, terminales e interacciones.
5. Menús, ajustes, controles, avisos sociales y notificaciones.
6. Misiones y diálogos por facción, como revisión paralela y separada.

Para cada bloque: comparar con el inglés original, corregir solo las cadenas claras, conservar variables como `~mission(...)` y comprobar etiquetas y recompensas. Después, indicar qué se revisó, qué quedó pendiente y si los cambios siguen en local o se publicaron.

## Auditoría de misiones con `[BP]`

Se añadieron listas a 105 descripciones que carecían de ellas: 76 recuperadas de la misma clave inglesa, 26 de otra descripción con el mismo grupo de recompensas y 3 de otra misión con el mismo grupo, contrastado con `misiones_reputacion_planos.json`. Los nombres de los objetos se conservaron en inglés. La lista indica opciones posibles; no significa que se entreguen todas. Comprobar de nuevo esta correspondencia cuando se extraiga el catálogo de un parche nuevo.

**Punto a comprobar:** varias entradas españolas llevan el sufijo `,P` en la clave y el original inglés no. No cambiarlo en masa hasta confirmar su función en el juego. Por ahora se conserva.

**Bloques anteriores:** cotejados los avisos de cabina Crusader, Argo, Esperia y Greycat con el original inglés; corregidos cinco errores claros en cada bloque, relativos a escaneo, daño, bengalas, escudos y radiación. Estos fabricantes comparten esas cadenas de origen.

**Bloque anterior:** cotejados los avisos de cabina Kruger con el original inglés y corregidas 54 cadenas de sentido erróneo o parcialmente sin traducir, sobre todo acoplamiento, aterrizaje, escudos y sistemas.

**Bloque anterior:** cotejados los avisos de cabina Consolidated Outland con el original inglés y corregidas 41 cadenas. Las claves `Shields_Left_*` y `Shields_Right_*` llevan rótulos ingleses invertidos respecto a su nombre; no se alteraron sin comprobar cómo aparecen dentro del juego.

**Bloque anterior:** cotejados los avisos de cabina Drake con el original inglés y corregidas 38 cadenas, principalmente contramedidas, escudos, piloto automático y munición.

**Bloque anterior:** en Origin, cotejadas las 39 entradas no vacías con el original y corregidas 13 cadenas, incluidos los nombres de contramedidas, el aviso de propulsores y las direcciones de los escudos. Las otras 83 entradas también están vacías en inglés y se dejaron intactas. En la captura del gestor de flota se observó «UBICACI N»; `ShipSelector_Location` contenía «Ubicación» correctamente y se cambió a «Lugar» para evitar el glifo acentuado que no se muestra. «CARGU» no aparece en `global.ini` ni se encontró una clave de cabecera de carga para esta pantalla; queda pendiente comprobar si el rótulo procede de la interfaz del juego y verificar ambas cabeceras tras instalar el archivo.

**Bloque anterior:** cotejadas las 42 entradas no vacías de los avisos de cabina de RSI y las 42 de Tumbril con el inglés original. Corregidas 17 cadenas en cada fabricante: activación de modos y aterrizaje, despegue, direcciones y estado de los escudos, y activación de motores y armas. Las otras 83 entradas de cada fabricante están vacías también en inglés y se dejaron intactas.

**Bloque anterior:** cotejados los avisos de cabina Vanduul y Xi'an con el inglés original. Corregidas 12 cadenas en cada fabricante: avisos de escaneo, daños, despegue y acoplamiento denegados, señuelos, radiación y estados de escudos y motores. Se conservaron las claves y marcas `,P` existentes.

**Bloque anterior:** revisadas las cadenas no vacías `ShipSelector_*` del gestor de flota frente al inglés original. Corregidos dos errores de sentido: la acción `Claim Default Loadout` ahora distingue la reclamación del vehículo con equipamiento predeterminado, y `Submit` ya no se presenta como «Registrar». No se tocó `ShipSelector_Location=Lugar`. Las cabeceras de la captura «UBICACI N» y «CARGU» siguen pendientes de verificación dentro del juego; no se halló una clave `ShipSelector_*` para la cabecera de carga.

**Bloque anterior:** revisados los 20 estados no vacíos `ui_ShipSelector_Info_*` frente al inglés original. Corregidas cuatro cadenas de estado: reclamación al seguro, solicitud en cola, vehículo rastreado y estado desconocido. No se encontró en esta familia una cabecera de carga.

**Bloque anterior:** cotejadas las entradas `RepairOxygenKiosk_*` y `WIP_RepairOxygenKiosk_*` con el inglés original. Corregidas cinco cadenas: las dos descripciones largas del dispensador de oxígeno, el objetivo breve que permanecía en inglés, el título con su etiqueta de reputación y la descripción de ubicación de la variante WIP. Se conservaron `~mission(Route)`, `~mission(Depth)`, las etiquetas y el orden de los apartados presentes en el original.

**Bloque anterior:** cotejadas las 72 cadenas no vacías `shop_ui_CommodityKiosk_*` de la terminal de comercio con el inglés original. Corregidas siete etiquetas: tiempos estimados, ocupación de almacenamiento, selección de contenedor, instrucción para seleccionar, titularidad del grupo y estado «Prohibido». No se alteraron SCU, abreviaturas ni saltos de línea.

**Bloque anterior:** cotejados los 58 mensajes no vacíos `shop_ui_transactionResult_*` con el inglés original. Corregidas seis cadenas: dos mensajes que seguían en inglés, una construcción gramatical incorrecta y tres referencias a «imagen» que en el original designan una instantánea de datos (`snapshot`).

**Bloque anterior:** cotejadas las 39 cadenas no vacías `shop_ui_item_*` y las 15 `shop_ui_tooltip_*` con el inglés original. Corregidas dos etiquetas de artículos: `TRY ON HAT` y `FASHION TYPE`, esta última diferenciada de `STYLE`. Las ayudas emergentes no requerían cambios comprobables.

**Bloque anterior:** cotejados los mensajes `shop_ui_transaction_*`, `shop_ui_resultmsg_*`, `shop_ui_buying_*` y `shop_ui_selling_*` con el inglés original. Corregidas dos cadenas: `buyer account` se refería al comprador, no al destino, y el aviso de almacenamiento alternaba incorrectamente el trato de tú y usted.

**Último bloque:** cotejadas las etiquetas `shop_ui_dropdown_*`, `shop_ui_pageNavigation_*` y `shop_ui_buttondisable_*`, además de las relacionadas con ubicación y refinería, con el inglés original. No se detectaron errores de sentido en esas familias. En la revisión de las cadenas `shop_ui_*` idénticas al inglés se corrigió `Bricked Item Timer`, que seguía sin traducir y cuya pareja `shop_ui_brickedItem` ya empleaba «objeto inutilizado».

**Siguiente bloque:** continuar con otras familias de textos de terminales y comercio. Sigue pendiente comprobar en el juego las cabeceras del gestor de flota y cómo se muestran las parejas enfoque/clase de la tienda de naves. Las coincidencias que quedan con el inglés incluyen nombres propios, abreviaturas, códigos y nombres de minerales que deben conservarse.
