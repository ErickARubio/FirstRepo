# Guía de Registro — APIs Externas

**Proyecto:** Video-Ensayos Cartográficos (ZMVM)
**Última actualización:** 2026-05-10

Sigue este orden. Las APIs marcadas como **[REQUERIDA]** son necesarias para producción.
Las **[OPCIONAL]** solo para funcionalidades específicas.

---

## Tiempo total estimado: 45–60 minutos

| # | Servicio | Tiempo | Aprobación | Tipo |
|---|----------|--------|-----------|------|
| 1 | ElevenLabs | 5 min | Inmediata | REQUERIDA |
| 2 | Pexels | 5 min | Inmediata | OPCIONAL |
| 3 | Unsplash | 10 min | Inmediata | OPCIONAL |
| 4 | Banxico | 5 min | Inmediata | REQUERIDA |
| 5 | INEGI | 10 min | 1-3 días hábiles | REQUERIDA |
| 6 | Datawrapper | 5 min | Inmediata | OPCIONAL |
| 7 | World Bank | 0 min | Sin registro | — |

---

## 1. ElevenLabs — Síntesis de voz IA ✅ REQUERIDA

**Tiempo estimado:** 5 minutos | **Aprobación:** Inmediata

### Pasos

1. Ir a **https://elevenlabs.io**
2. Clic en **"Sign Up"** (esquina superior derecha)
3. Registrarse con email o con cuenta de Google
4. Confirmar el email si se registró con email (revisar inbox)
5. Una vez dentro del panel, clic en el **ícono de perfil** (esquina superior derecha)
6. Seleccionar **"Profile + API key"**
7. En la sección **"API Key"**, copiar la clave que aparece (empieza con `sk_...`)
8. Abrir el archivo `.env` en la raíz del proyecto
9. Pegar la clave en:
   ```
   ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Plan gratuito
- **10,000 caracteres/mes** (~7 minutos de voz)
- Para este proyecto se necesitan ~820 palabras × 5 chars promedio = ~4,100 chars por versión completa
- El plan gratuito alcanza para **2 versiones completas** del video por mes
- Plan "Starter" ($5 USD/mes) da 30,000 chars — suficiente para producción

### Nota
La voz **Mateo (es-MX)** está disponible en el plan gratuito. Si no la encuentras, buscar en el panel de voces con filtro "Spanish" + "Mexican".

---

## 2. Pexels — Banco de imágenes gratuito ⚡ OPCIONAL

**Tiempo estimado:** 5 minutos | **Aprobación:** Inmediata

### Pasos

1. Ir a **https://www.pexels.com/api/**
2. Clic en **"Get Started"**
3. Crear cuenta con email o Google (si ya tienes cuenta Pexels, inicia sesión)
4. Completar el formulario de solicitud de API:
   - **"What will you use the API for?"**: seleccionar "Personal project" o "Commercial project"
   - Descripción breve: "Producción de video-ensayos documentales sobre economía urbana"
5. Clic en **"Submit"**
6. La clave aparece inmediatamente en la página siguiente
7. Copiar la clave y pegarla en `.env`:
   ```
   PEXELS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Plan gratuito
- **200 requests/hora**, **20,000 requests/mes**
- Sin marca de agua
- Licencia: uso libre en proyectos comerciales y personales sin atribución obligatoria

---

## 3. Unsplash — Banco de imágenes gratuito ⚡ OPCIONAL

**Tiempo estimado:** 10 minutos | **Aprobación:** Inmediata (acceso demo) / 1-2 días (producción)

### Pasos

1. Ir a **https://unsplash.com/join** y crear una cuenta
2. Confirmar el email
3. Ir a **https://unsplash.com/developers**
4. Clic en **"Your apps"** → **"New Application"**
5. Aceptar los términos de uso (leer la sección sobre atribución — requerida)
6. Completar el formulario:
   - **Application name**: `zmvm-video-essays`
   - **Description**: "Producción de video-ensayos documentales sobre economía y urbanismo"
   - **Website**: dejar en blanco si no tienes
7. Clic en **"Create application"**
8. En la página de la aplicación, copiar:
   - **"Access Key"** → pegar en `.env` como `UNSPLASH_ACCESS_KEY=`
   - **"Secret key"** → pegar en `.env` como `UNSPLASH_SECRET_KEY=`

### Plan gratuito (Demo)
- **50 requests/hora**
- Las imágenes en modo demo tienen marca de agua en la API de descarga (no en uso real)
- Para producción real: solicitar upgrade a "Production" — revisión manual, 1-2 días

### Atribución requerida
Unsplash **requiere atribución** en el video o descripción: "Foto por [Nombre] en Unsplash"

---

## 4. Banxico SIE API — Datos económicos México ✅ REQUERIDA

**Tiempo estimado:** 5 minutos | **Aprobación:** Inmediata (token generado al instante)

### Pasos

1. Ir directamente a **https://www.banxico.org.mx/SieAPIRest/service/v1/token**
2. Iniciar sesión con tu cuenta de Banxico, **o** crear una nueva:
   - Clic en **"Registrarse"**
   - Llenar nombre, email y contraseña
   - Confirmar el email
3. Una vez autenticado, la página muestra tu **token de acceso** directamente
4. Copiar el token (cadena larga alfanumérica)
5. Pegar en `.env`:
   ```
   BANXICO_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Acceso
- Sin límite de requests documentado para uso académico/personal
- Acceso a todas las series del SIE (Sistema de Información Económica): tipo de cambio, inflación, tasas, balanza de pagos, remesas, etc.
- La serie de **remesas (CE81)** y **tipo de cambio (SF43718)** son las más relevantes para este proyecto

---

## 5. INEGI API de Indicadores — Datos nacionales México ✅ REQUERIDA

**Tiempo estimado:** 10 minutos de solicitud | **Aprobación:** 1-3 días hábiles

### Pasos

1. Ir a **https://www.inegi.org.mx/servicios/api_indicadores.html**
2. Hacer scroll hacia abajo hasta la sección **"Solicitud de token"**
3. Clic en el botón **"Solicitar token"** (abre un formulario en línea)
4. Completar el formulario:
   - **Nombre completo**
   - **Correo electrónico** (institucional preferido, pero personal funciona)
   - **Institución / Organización**: si es personal, poner "Proyecto independiente de análisis de datos"
   - **Propósito de uso**: "Análisis de indicadores económicos y demográficos para producción de video-ensayos educativos sobre economía urbana de México"
5. Clic en **"Enviar"**
6. Esperar email de confirmación con el token (generalmente 1-3 días hábiles)
7. Cuando llegue el email, copiar el token y pegar en `.env`:
   ```
   INEGI_TOKEN=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

### Plan gratuito
- Sin costo para uso académico y personal
- Acceso a todos los indicadores del BIE (Banco de Información Económica): PIB, empleo, demografía, precios, etc.

### Datos clave para este proyecto
- Indicador `6200093066` — PIB Nacional (verificación)
- Indicador `6207020032` — Población total por entidad
- Censos de Población — requiere descarga directa, no API

---

## 6. Datawrapper — Mapas y gráficos publicables ⚡ OPCIONAL

**Tiempo estimado:** 5 minutos | **Aprobación:** Inmediata

### Pasos

1. Ir a **https://www.datawrapper.de** y crear una cuenta gratuita
2. Confirmar el email
3. Ir a **https://app.datawrapper.de/account/api-tokens**
4. Clic en **"Create API Token"**
5. Asignar nombre al token: `zmvm-project`
6. Seleccionar permisos: **"Read + Write"** (necesario para crear y publicar gráficos via API)
7. Clic en **"Create"**
8. Copiar el token que aparece (solo se muestra una vez — guardarlo)
9. Pegar en `.env`:
   ```
   DATAWRAPPER_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### Plan gratuito
- Ilimitados gráficos embebidos
- 10 gráficos/día via API en el plan gratuito
- Sin marca de agua en el plan gratuito (a diferencia de Flourish)
- Los gráficos son públicos a menos que tengas plan de pago

---

## 7. World Bank Open Data — Sin registro ✅ LIBRE

**Tiempo estimado:** 0 minutos | **Sin token requerido**

La API del Banco Mundial es completamente abierta.

### URL base de uso directo
```
https://api.worldbank.org/v2/country/{pais}/indicator/{indicador}?format=json
```

### Ejemplos relevantes para el proyecto
```
# PIB México (USD corrientes)
https://api.worldbank.org/v2/country/MX/indicator/NY.GDP.MKTP.CD?format=json&mrv=5

# PIB per cápita México
https://api.worldbank.org/v2/country/MX/indicator/NY.GDP.PCAP.CD?format=json&mrv=5

# Remesas recibidas (% del PIB)
https://api.worldbank.org/v2/country/MX/indicator/BX.TRF.PWKR.DT.GD.ZS?format=json&mrv=5
```

No se requiere configuración en `.env`.

---

## Verificar todo de una vez

Después de llenar el `.env`, ejecutar:

```bash
python 00_Orchestrator/tools/test_connections.py
```

Resultado esperado cuando todo está listo:
```
  ✅  ElevenLabs        Cuota disponible: 9,180 chars / 10,000
  ✅  Pexels            Requests restantes este mes: 19,987
  ✅  Unsplash          Conectado
  ✅  Banxico           Conectado (serie SF43718 tipo de cambio OK)
  ✅  INEGI             Conectado (indicador PIB OK)
  ✅  Datawrapper       Conectado como: tu_usuario
  ✅  World Bank        Sin token requerido — acceso libre OK

  7 de 7 APIs configuradas correctamente.
```

---

## Orden de prioridad si el tiempo es limitado

Si solo puedes registrarte en algunas APIs hoy, este es el orden de impacto:

1. **ElevenLabs** — sin voz no hay video
2. **Banxico** — datos de remesas y economía (registro instantáneo)
3. **INEGI** — solicitar ya porque tarda 1-3 días
4. **Datawrapper** — para exportar los gráficos sin Flourish
5. **Pexels + Unsplash** — solo si decides agregar imágenes documentales (este video no las usa)
