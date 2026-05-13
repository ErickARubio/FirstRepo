# Fuentes Tier 1 — Las remesas en México
**Proyecto:** 2026-05-remesas-mx
**Tesis seleccionada:** Tesis 2 — La geografía invisible del subsidio migrante
**Agente:** A1 Investigador Económico
**Fecha:** 2026-05-12

---

## Fuentes Tier 1A — Instituciones Nacionales

### F01 — Banco de México (Banxico): Remesas por entidad federativa
- **Institución:** Banco de México
- **Tier:** 1A
- **URL portal:** https://www.banxico.org.mx/SieInternet/
- **Series relevantes:** CE100 (remesas totales), series por entidad federativa
- **Formato:** Excel/CSV descargable del portal SIE
- **Variables clave:** Monto de remesas recibidas por estado (millones USD), trimestral y anual
- **Cobertura temporal:** 2003–2024
- **Granularidad geográfica:** Estatal (32 entidades)
- **Dato verificado:** Top 5 estados 2024: Michoacán, Jalisco, Guanajuato, CDMX, Edomex
- **Estado:** Acceso vía portal SIE — descarga manual por estado o reporte nacional

### F02 — INEGI: ENIGH 2022 (Encuesta Nacional de Ingresos y Gastos de los Hogares)
- **Institución:** INEGI
- **Tier:** 1A
- **URL:** https://www.inegi.org.mx/programas/enigh/nc/2022/
- **Microdatos:** https://www.inegi.org.mx/rnm/index.php/catalog/899
- **Formato:** CSV (microdatos de hogares)
- **Variables clave:** ingreso_rem (ingreso por remesas), gasto por rubro, características del hogar
- **Granularidad:** Hogar / estatal
- **Cobertura:** 2022 (última edición bienal disponible)
- **Relevancia:** Mide composición del gasto de hogares receptores vs. no receptores de remesas; porcentaje de hogares receptores por estado
- **Estado:** Microdatos públicos, requieren descarga y procesamiento en R o Python

### F03 — INEGI: PIBE (Producto Interno Bruto por Entidad Federativa) 2023
- **Institución:** INEGI
- **Tier:** 1A
- **URL:** https://www.inegi.org.mx/temas/pibe/
- **Formato:** Excel tabulados
- **Variables clave:** PIB estatal a precios corrientes, crecimiento anual, PIB per cápita
- **Relevancia:** Permite cruzar monto de remesas por estado (Banxico) con crecimiento económico (PIBE) para documentar la correlación negativa
- **Estado:** Disponible en portal, último dato 2023

### F04 — INEGI: Censo de Población y Vivienda 2020
- **Institución:** INEGI
- **Tier:** 1A
- **URL:** https://www.inegi.org.mx/programas/ccpv/2020/
- **Variables clave:** Pirámide de edad por estado, hogares con emigrantes internacionales
- **Granularidad:** Municipal / estatal
- **Relevancia:** Documenta el drenaje demográfico — pirámide de edad invertida en Michoacán, Guanajuato, Jalisco
- **Estado:** Datos públicos, tabulados disponibles sin descarga de microdatos

### F05 — CONAPO: Índice de Intensidad Migratoria 2020
- **Institución:** Consejo Nacional de Población
- **Tier:** 1A
- **URL:** https://www.gob.mx/conapo/documentos/indice-de-intensidad-migratoria-mexico-estados-unidos-2020
- **Formato:** Excel + mapa
- **Variables clave:** Índice municipal de intensidad migratoria, % hogares que reciben remesas, % hogares con emigrantes
- **Granularidad:** Municipal y estatal
- **Relevancia:** Establece cuáles son los municipios de "muy alta" y "alta" intensidad migratoria — el corazón del mapa de la tesis
- **Estado:** Disponible públicamente, 2020 es la edición más reciente

---

## Fuentes Tier 1B — Organismos Multilaterales

### F06 — Banco Mundial: World Development Indicators (WDI)
- **Institución:** Banco Mundial
- **Tier:** 1B
- **API verificada:** https://api.worldbank.org/v2/country/MX/indicator/BX.TRF.PWKR.CD.DT
- **Indicadores:**
  - BX.TRF.PWKR.CD.DT — Remesas recibidas USD corrientes
  - BX.TRF.PWKR.DT.GD.ZS — Remesas como % del PIB
  - NY.GDP.MKTP.CD — PIB México
- **Datos verificados:**
  - 2024: $67,637M USD (3.64% PIB)
  - 2023: $66,237M USD
  - 2022: $61,457M USD
  - 2021: $55,067M USD
  - 2020: $43,977M USD
- **Estado:** API operacional, datos verificados en sesión 2026-05-12

### F07 — CEPAL: Remesas y desarrollo en América Latina
- **Institución:** Comisión Económica para América Latina y el Caribe
- **Tier:** 1B
- **URL portal:** https://www.cepal.org/es/subtemas/migracion-internacional
- **Relevancia:** Estudios sobre correlación remesas-crecimiento económico regional; marco conceptual de "trampa de remesas"; comparativas con otros países LAC
- **Estado:** Publicaciones abiertas en portal CEPAL; buscar "remesas México desarrollo regional"

### F08 — BID: Evaluaciones de impacto de remesas
- **Institución:** Banco Interamericano de Desarrollo
- **Tier:** 1B
- **URL portal:** https://publications.iadb.org/
- **Publicación clave:** "Las remesas y el desarrollo: ¿mito o realidad?" (BID, varios autores)
- **Relevancia:** Evidencia sobre el efecto sustitución (remesas vs. inversión pública); impacto en capital productivo local
- **Estado:** Publicaciones abiertas; buscar "remittances Mexico substitution effect"

### F09 — Pew Research Center: Estimados de mexicanos en EE.UU.
- **Institución:** Pew Research Center
- **Tier:** 1B (think tank de alta reputación metodológica)
- **URL:** https://www.pewresearch.org/hispanic/
- **Variables clave:** Población de origen mexicano en EE.UU., estados de residencia, estatus migratorio estimado
- **Dato de referencia:** ~11-12 millones de mexicanos nacidos en México residen en EE.UU.
- **Estado:** Reportes públicos anuales

---

## Fuentes Tier 1C — Centros Académicos

### F10 — CIDE / COLMEX: Estudios sobre migración mexicana
- **Institución:** CIDE, El Colegio de México
- **Tier:** 1C
- **URL CIDE:** https://www.cide.edu/publicaciones/
- **Relevancia:** Investigación académica sobre circuitos migratorios históricos, Programa Bracero, efectos del IRCA 1986
- **Estado:** Buscar documentos de trabajo sobre "migración circular" y "comunidades de alta migración"

---

## Datasets prioritarios a procesar

| # | Nombre | Institución | Formato | Variables | Visual destino |
|---|--------|-------------|---------|-----------|----------------|
| D1 | Remesas por entidad 2000-2024 | Banxico SIE | Excel/CSV | USD por estado por año | Mapa coroplético + serie temporal |
| D2 | ENIGH 2022 — hogares receptores | INEGI | CSV microdatos | gasto por rubro, ingreso_rem | Gráfico composición del gasto |
| D3 | Índice Intensidad Migratoria 2020 | CONAPO | Excel + shapefile | índice por municipio | Mapa base de circuitos |
| D4 | PIBE 2023 por entidad | INEGI | Excel | PIB per cápita, crecimiento | Scatter plot remesas vs crecimiento |
| D5 | Censo 2020 — pirámide de edad | INEGI | Tabulados web | edad, sexo, por estado | Pirámide demográfica Michoacán vs MX |
| D6 | WDI remesas MX 2000-2024 | Banco Mundial | API verificada | BX.TRF.PWKR.CD.DT | Serie temporal introducción |
