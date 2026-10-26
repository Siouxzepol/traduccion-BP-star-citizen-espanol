# Star Citizen — traducción + BP al español de España

Traducción comunitaria no oficial para Star Citizen. El mismo paquete incluye los archivos para las instalaciones `LIVE` y `PTU`; cada una utiliza su propia carpeta de localización `spanish_(spain)`.

## Compatibilidad y versión de la traducción

**LIVE 4.10.2 · PTU 4.10.3 · Traducción: v1.0.36** — Actualizado el 26/10/2026. [Descargar el parche](https://github.com/Siouxzepol/traduccion-BP-star-citizen-espanol/releases/latest/download/Traduccion_SC_es-ES_LIVE.zip).

La localización añade marcadores `[BP]` y `[REP n]` a los títulos de misión cuando las recompensas son inequívocas para todas las variantes que comparten ese título. También añade reputación y posibles planos a ciertas descripciones de misión cuando pueden asociarse sin ambigüedad. Los planos pueden ser aleatorios y no se garantiza que se entreguen todos. El número de versión se incrementará con cada nueva publicación del parche.

## Instalación sencilla (LIVE y PTU)

1. Cierra Star Citizen.
2. Descarga el [paquete ZIP de la última versión](https://github.com/Siouxzepol/traduccion-BP-star-citizen-espanol/releases/latest/download/Traduccion_SC_es-ES_LIVE.zip).
3. Extrae su contenido en la carpeta raíz de Star Citizen, la que contiene las carpetas `LIVE` y `PTU` (por ejemplo, `C:\\Program Files\\Roberts Space Industries\\StarCitizen\\`).
4. Si Windows pregunta si quieres reemplazar archivos, confirma después de guardar una copia del archivo anterior.
5. Inicia el juego y selecciona español de España.

El ZIP ya incluye ambas rutas:

```text
LIVE/data/Localization/spanish_(spain)/global.ini
PTU/data/Localization/spanish_(spain)/global.ini
```

No extraigas el ZIP dentro de `LIVE` ni de `PTU`, porque se duplicaría la carpeta. Al extraerlo en la raíz de Star Citizen, se instalará automáticamente el archivo correspondiente a cada versión. Si solo tienes instalada una de las dos versiones, la otra carpeta no afecta al juego.

## Instalación manual

Si prefieres no usar el ZIP, copia el [`global.ini`](https://github.com/Siouxzepol/traduccion-BP-star-citizen-espanol/blob/main/global.ini) en una de estas rutas, guardando antes una copia del archivo original:

```text
LIVE/data/Localization/spanish_(spain)/global.ini
PTU/data/Localization/spanish_(spain)/global.ini
```

Las actualizaciones del juego pueden sobrescribir el archivo o añadir cadenas nuevas; revisa este repositorio después de cada actualización.

## Datos de misiones

Los títulos de misión incluyen `[BP]` si todas las variantes identificadas ofrecen planos y `[REP n]` si todas comparten la misma recompensa de reputación de facción. Las descripciones de ciertas misiones incluyen más detalles de sus recompensas. Los planos de un grupo pueden ser aleatorios; no se garantiza que se entreguen todos. El [catálogo completo de recompensas por contrato](datos/misiones_reputacion_planos.json) y el [catálogo de componentes de nave](datos/componentes_nave.json) sirven también como referencias complementarias. Consulta [cómo leer y actualizar los catálogos](datos/README.md).

## Comprobación de minerales

Los nombres de los minerales se mantienen en inglés para coincidir con las guías y los terminales del juego. Antes de publicar cambios en `global.ini`, ejecuta `python herramientas/verificar_minerales.py`. La comprobación detecta nombres incorrectos o cruzados en los 26 minerales minables y en los subtipos que usa el gestor de carga.

## Criterios para las publicaciones

Las notas de cada release deben describir los cambios en pasado mediante participios como `Corregido`, `Añadida` o `Actualizado`. También deben incluir siempre los enlaces al [Discord de La Colmena](https://discord.gg/FQTpFjN) y al [canal de Twitch de Norrisplay](https://www.twitch.tv/norrisplay).

## Créditos

Autor y responsable de la traducción: **Sioux_Atreides**  
Clan: **La Colmena**

Este proyecto es comunitario y no está afiliado a Cloud Imperium Games ni a Roberts Space Industries. Star Citizen y sus marcas pertenecen a sus respectivos titulares.

## Comunidad

- [Discord de La Colmena](https://discord.gg/FQTpFjN)
- [Twitch de Norrisplay](https://www.twitch.tv/norrisplay)
