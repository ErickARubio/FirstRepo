# Fuentes Tier 1 — Fase 1
**Proyecto:** 2026-05-edomex-cdmx
**Agente:** A1 Investigador
**Fecha:** 2026-05-10

---

## Fuentes Tier 1A — Instituciones Nacionales

### F01 — EOD 2017 (Encuesta Origen-Destino en Hogares de la ZMVM)
- **Institución:** INEGI / Instituto de Ingeniería UNAM
- **Tier:** 1A
- **URL:** https://www.inegi.org.mx/programas/eod/2017/
- **Microdatos:** https://www.inegi.org.mx/rnm/index.php/catalog/533
- **Resultados PDF:** https://www.inegi.org.mx/contenidos/programas/eod/2017/doc/resultados_eod_2017.pdf
- **Formato:** Microdatos en CSV + tabulados
- **Cobertura:** 16 alcaldías CDMX + 59 municipios Edomex + Tizayuca, Hidalgo
- **Variables clave:** viajes por municipio origen-destino, propósito del viaje (trabajo), modo de transporte, duración del traslado
- **Relevancia para el video:** Cuantifica el flujo pendular Edomex→CDMX; base de todos los mapas de movilidad; datos de 2017 son los más recientes disponibles a esta escala
- **Dato verificado en búsqueda:** 34,565,491 viajes diarios; 22.5% intermunicipales (Edomex↔CDMX)
- **Nota:** Requiere nueva EOD — la siguiente edición está pendiente desde 2023

---

### F02 — PIBE 2023 (Producto Interno Bruto por Entidad Federativa)
- **Institución:** INEGI
- **Tier:** 1A
- **URL:** https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2024/PIBEF/PIBEF2023_CDMX.pdf
- **Portal:** https://www.inegi.org.mx/app/tabulados/default.aspx?pr=17&vr=7&in=2&tp=20&wr=1&cno=2
- **Formato:** PDF + tabulados descargables
- **Variables clave:** PIB por entidad, PIB por sector de actividad económica
- **Relevancia:** Establece que CDMX = 14.8% PIB nacional; Edomex = 9.1%; servicios = 83.5% PIB CDMX
- **Dato verificado:** Sí, publicado dic 2024 para año fiscal 2023

---

### F03 — IMSS: Puestos de trabajo asegurados por municipio
- **Institución:** IMSS
- **Tier:** 1A
- **URL:** https://datos.gob.mx/busca/dataset/trabajadores-imss-asegurados-por-municipio
- **URL alternativa:** https://www.imss.gob.mx/conoce-el-imss/memoria-estadistica-2023
- **Formato:** CSV mensual
- **Variables clave:** municipio de registro del empleo, número de asegurados, salario base de cotización
- **Relevancia:** Permite estimar cuántos puestos de trabajo formales están registrados en alcaldías de CDMX; combinado con EOD identifica proporción de trabajadores que residen en Edomex
- **Nota de limpieza:** El IMSS registra el municipio del patrón, no del trabajador — requiere cruce con EOD para inferir lugar de residencia
- **Dato de referencia:** CDMX superó 3.5 millones de trabajadores asegurados en 2024

---

### F04 — CONEVAL: Pobreza municipal 2020
- **Institución:** CONEVAL
- **Tier:** 1A
- **URL:** https://www.coneval.org.mx/Medicion/Paginas/Pobreza-municipal.aspx
- **URL Edomex:** https://www.coneval.org.mx/coordinacion/entidades/EstadodeMexico/Paginas/principal.aspx
- **Formato:** Shapefile + Excel por municipio
- **Variables clave:** % en pobreza, % en pobreza extrema, carencias sociales por municipio
- **Relevancia:** Documenta que Ecatepec (43.5% pobreza, 786K personas) y Nezahualcóyotl (523K personas) son simultáneamente municipios expulsores de fuerza laboral y altamente pobres
- **Dato verificado:** Ecatepec = 2° municipio con más pobres en términos absolutos a nivel nacional

---

### F05 — INEGI EFIPEM: Finanzas Públicas Estatales y Municipales
- **Institución:** INEGI
- **Tier:** 1A
- **URL:** https://www.inegi.org.mx/programas/finanzas/
- **Formato:** Excel por entidad y municipio
- **Variables clave:** ingresos propios, transferencias federales, gasto en infraestructura, deuda pública
- **Relevancia:** Permite comparar la estructura fiscal de CDMX vs. municipios de Edomex; documenta la asimetría en capacidad de inversión pública
- **Nota:** Requiere años 2018-2023 para comparativa histórica

---

### F06 — SEDATU: Delimitación de Zonas Metropolitanas 2018
- **Institución:** SEDATU / CONAPO / INEGI
- **Tier:** 1A
- **URL:** https://www.gob.mx/conapo/documentos/delimitacion-de-las-zonas-metropolitanas-de-mexico-2015
- **Versión 2018:** https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/702825006792.pdf
- **Formato:** PDF + shapefile
- **Variables clave:** municipios que integran cada zona metropolitana, criterios de delimitación
- **Relevancia:** Establece la composición oficial de la ZMVM (76 municipios Edomex + 16 alcaldías CDMX + Tizayuca)

---

### F07 — ISN CDMX: Ley de Hacienda del Distrito Federal / CDMX
- **Institución:** Secretaría de Administración y Finanzas CDMX
- **Tier:** 1A
- **URL:** https://transparencia.finanzas.cdmx.gob.mx/repositorio/public/upload/repositorio/Tesoreria/123/b/Criterio_9/123_XV_Impuesto_sobre_nominas_2024.pdf
- **Formato:** PDF normativo
- **Variables clave:** tasa del ISN (4% desde 2025), base gravable, exenciones
- **Relevancia:** Establece el mecanismo fiscal central de la Tesis 1; el ISN recauda del trabajo realizado en CDMX independientemente de la residencia del trabajador

---

### F08 — Diagnóstico Técnico de Movilidad PIM (SEMOVI)
- **Institución:** SEMOVI CDMX
- **Tier:** 1A (gobierno local)
- **URL:** https://semovi.cdmx.gob.mx/storage/app/media/diagnostico-tecnico-de-movilidad-pim.pdf
- **Formato:** PDF
- **Variables clave:** tiempos de traslado, movilidad interestatal, condiciones del transporte público
- **Relevancia:** Documenta que trabajadores de periferia inician viajes 4-6 AM; tiempos promedio de 85 min para viajes Edomex→CDMX
- **Dato verificado:** ONU-Habitat cita 5 horas para cruzar la ZMVM de extremo a extremo

---

## Fuentes Tier 1B — Organismos Multilaterales

### F09 — BID: Gobernanza Metropolitana en América Latina
- **Institución:** Banco Interamericano de Desarrollo
- **Tier:** 1B
- **URL de referencia:** https://publications.iadb.org/publications/spanish/viewer/gobernanza-metropolitana.pdf
- **Relevancia:** Marco comparado de gobernanza metropolitana; posiciona a la ZMVM en contexto regional; referencia para Tesis 3
- **Nota:** Buscar publicación específica sobre ZMVM o México en portal BID

---

### F10 — ONU-Habitat: Movilidad ZMVM
- **Institución:** ONU-Habitat México
- **Tier:** 1B
- **URL:** https://onu-habitat.org/index.php/5-horas-en-transporte-publico-para-cruzar-la-zmvm
- **Relevancia:** Cita verificada: 5 horas para cruzar la ZMVM en transporte público; validación internacional del problema de movilidad

---

## Fuentes Tier 1C — Centros Académicos

### F11 — UNAM / GIITRAL: EOD 2017 herramienta interactiva
- **Institución:** Instituto de Ingeniería UNAM
- **Tier:** 1C
- **URL:** https://giitral.iingen.unam.mx/Estudios/EstudioOD-ZMVM-2017.html
- **Relevancia:** Portal interactivo con visualizaciones de la EOD 2017; útil para identificar flujos específicos por municipio

---

### F12 — WRI: Base de datos ajustada EOD 2017
- **Institución:** World Resources Institute México
- **Tier:** 1C
- **URL:** https://es.wri.org/publicaciones/base-de-datos-ajustada-de-la-encuesta-origen-destino-para-la-zona-metropolitana-del
- **Formato:** Dataset procesado
- **Relevancia:** Versión ajustada y documentada de la EOD para análisis; puede ser más accesible que los microdatos originales de INEGI

---

## Datasets prioritarios a descargar

| # | Nombre | Institución | URL | Variables | Visualización destino |
|---|--------|------------|-----|-----------|----------------------|
| D1 | EOD 2017 microdatos | INEGI | inegi.org.mx/programas/eod/2017/ | origen-destino por municipio, propósito trabajo | Mapa de flujos pendulares |
| D2 | PIBE 2023 por entidad | INEGI | PIBEF2023.pdf | PIB por sector, por entidad | Gráfico comparativo CDMX/Edomex |
| D3 | IMSS asegurados por municipio | IMSS | datos.gob.mx | puestos formales por municipio | Mapa de concentración de empleo |
| D4 | Pobreza municipal CONEVAL 2020 | CONEVAL | coneval.org.mx | % pobreza, n° personas | Mapa coroplético periferia |
| D5 | EFIPEM 2018-2023 | INEGI | inegi.org.mx/programas/finanzas/ | ingreso propio, gasto infraestructura | Comparativa fiscal CDMX vs Edomex |
| D6 | ISN recaudación CDMX | SAF CDMX | finanzas.cdmx.gob.mx | recaudación anual ISN por sector | Infografía de flujo fiscal |
| D7 | Delimitación ZMVM shapefile | SEDATU/CONAPO | conapo.gob.mx | límites municipales, clasificación ZM | Mapa base de la ZMVM |
