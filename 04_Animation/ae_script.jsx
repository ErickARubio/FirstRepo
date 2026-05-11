// ae_script.jsx — Generado por Agente A5
// Proyecto: El impuesto que no regresa (2026-05-edomex-cdmx)
// Fecha: 2026-05-10
// After Effects ExtendScript (ES3 compatible)
//
// INSTRUCCIONES:
//   1. Instalar fuentes Inter y JetBrains Mono antes de ejecutar
//   2. En After Effects: File > Scripts > Run Script File... > seleccionar este archivo
//   3. El script crea la composición maestra y las 14 composiciones de escena
//   4. Importar manualmente los assets (WAV, SVG, PNG) después de ejecutar

// ─── CONFIGURACIÓN GLOBAL ─────────────────────────────────────────────────────

var PROJECT_SLUG   = "2026-05-edomex-cdmx";
var PROJECT_TITLE  = "El impuesto que no regresa";
var FRAME_RATE     = 24;
var WIDTH          = 1920;
var HEIGHT         = 1080;
var TOTAL_SECONDS  = 390; // 6:30

// Paleta — Institucional Moderno (variante ZMVM)
// Valores en escala 0–1 para AE (dividir hex entre 255)
var C = {
    bg_white:      [1.000, 1.000, 1.000],   // #FFFFFF
    bg_light:      [0.957, 0.965, 0.976],   // #F4F6F9
    bg_dark:       [0.051, 0.067, 0.090],   // #0D1117
    text_primary:  [0.051, 0.106, 0.165],   // #0D1B2A
    text_secondary:[0.290, 0.384, 0.455],   // #4A6274
    blue_cdmx:     [0.000, 0.447, 0.710],   // #0072B5
    orange_edomex: [0.910, 0.322, 0.039],   // #E8520A
    red_alert:     [0.753, 0.224, 0.169],   // #C0392B
    text_light:    [0.957, 0.957, 0.941]    // #F4F6F9 (para fondos oscuros)
};

// Definición de escenas: [número, nombre_slug, inicio_seg, duracion_seg, fondo]
var SCENES = [
    [1,  "APERTURA",       0,   15, "dark"],
    [2,  "ISN_MECANISMO",  15,  30, "white"],
    [3,  "PIB_PASTEL",     45,  20, "white"],
    [4,  "CRECIMIENTO",    65,  25, "white"],
    [5,  "SISTEMA_TYPO",   90,  20, "white"],
    [6,  "FLUJOS_EOD",     110, 30, "light"],
    [7,  "JORNADA",        140, 30, "white"],
    [8,  "FLUJO_FISCAL",   170, 30, "white"],
    [9,  "METRO_LIMITE",   200, 30, "light"],
    [10, "POBREZA",        230, 30, "light"],
    [11, "TENSION_ISN",    260, 40, "white"],
    [12, "VIVIENDA",       300, 35, "light"],
    [13, "EL_DATO",        335, 30, "dark"],
    [14, "CIERRE",         365, 25, "dark"]
];

// ─── UTILIDADES ───────────────────────────────────────────────────────────────

function padNum(n, width) {
    var s = String(n);
    while (s.length < width) s = "0" + s;
    return s;
}

function sceneCompName(num, slug) {
    return PROJECT_SLUG + "_SC" + padNum(num, 2) + "_" + slug;
}

function getBgColor(type) {
    if (type === "dark")  return C.bg_dark;
    if (type === "light") return C.bg_light;
    return C.bg_white;
}

// ─── CREAR CARPETAS EN EL PROYECTO ────────────────────────────────────────────

function createFolderIfMissing(name) {
    var items = app.project.items;
    for (var i = 1; i <= items.length; i++) {
        if (items[i] instanceof FolderItem && items[i].name === name) {
            return items[i];
        }
    }
    return app.project.items.addFolder(name);
}

function setupFolders() {
    var folders = {};
    folders.comps   = createFolderIfMissing("00_COMPS");
    folders.scenes  = createFolderIfMissing("01_SCENES");
    folders.maps    = createFolderIfMissing("02_MAPS");
    folders.charts  = createFolderIfMissing("03_CHARTS");
    folders.voice   = createFolderIfMissing("04_VOICE");
    folders.music   = createFolderIfMissing("05_MUSIC");
    return folders;
}

// ─── CREAR COMPOSICIÓN MAESTRA ────────────────────────────────────────────────

function createMasterComp(folders) {
    var name = PROJECT_SLUG + "_MASTER";
    var comp = app.project.items.addComp(
        name, WIDTH, HEIGHT, 1, TOTAL_SECONDS, FRAME_RATE
    );
    comp.parentFolder = folders.comps;
    // Fondo negro por defecto en la maestra
    var bg = comp.layers.addSolid(C.bg_dark, "BG_MASTER", WIDTH, HEIGHT, 1);
    bg.moveToEnd();
    return comp;
}

// ─── CREAR COMPOSICIÓN DE ESCENA ──────────────────────────────────────────────

function createSceneComp(sceneData, folders) {
    var num      = sceneData[0];
    var slug     = sceneData[1];
    var startSec = sceneData[2];
    var durSec   = sceneData[3];
    var bgType   = sceneData[4];

    var name = sceneCompName(num, slug);
    var comp = app.project.items.addComp(
        name, WIDTH, HEIGHT, 1, durSec, FRAME_RATE
    );
    comp.parentFolder = folders.scenes;

    // Fondo de la escena
    var bgColor = getBgColor(bgType);
    var bg = comp.layers.addSolid(bgColor, "BG", WIDTH, HEIGHT, 1);
    bg.moveToEnd();

    return comp;
}

// ─── AGREGAR PLACEHOLDER DE TEXTO ─────────────────────────────────────────────

function addPlaceholderText(comp, content, fontSize, color, posX, posY) {
    var textLayer = comp.layers.addText(content);
    var srcText   = textLayer.property("ADBE Text Properties")
                              .property("ADBE Text Document");
    var textDoc   = srcText.value;

    textDoc.fontSize  = fontSize;
    textDoc.fillColor = color;
    // Nota: la fuente exacta depende del nombre instalado en el sistema
    // Ajustar "Inter-Bold" al nombre exacto que muestra AE en Character panel
    try { textDoc.font = "Inter-Bold"; } catch(e) {}
    textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    srcText.setValue(textDoc);

    textLayer.property("Position").setValue([posX, posY]);
    textLayer.name = "TXT_" + content.substring(0, 20).replace(/\s/g, "_");
    return textLayer;
}

// ─── ANIMACIÓN FADE-IN BÁSICA ─────────────────────────────────────────────────

function applyFadeIn(layer, startTimeSec, durationSec) {
    var opProp = layer.property("Transform").property("Opacity");
    opProp.setValueAtTime(startTimeSec, 0);
    opProp.setValueAtTime(startTimeSec + durationSec, 100);
    // Aplicar Easy Ease Out al keyframe de inicio
    try {
        var key1 = opProp.nearestKeyIndex(startTimeSec);
        opProp.setTemporalEaseAtKey(key1,
            [new KeyframeEase(0, 33.33)],
            [new KeyframeEase(100, 33.33)]
        );
    } catch(e) {}
}

// ─── ANIMACIÓN SLIDE-UP + FADE ────────────────────────────────────────────────

function applySlideUpFadeIn(layer, startTimeSec, durationSec, offsetPx) {
    offsetPx = offsetPx || 30;
    var finalPos = layer.property("Transform").property("Position").value;

    // Opacity
    applyFadeIn(layer, startTimeSec, durationSec);

    // Position slide
    var posProp = layer.property("Transform").property("Position");
    posProp.setValueAtTime(startTimeSec,              [finalPos[0], finalPos[1] + offsetPx]);
    posProp.setValueAtTime(startTimeSec + durationSec, finalPos);
    try {
        var key1 = posProp.nearestKeyIndex(startTimeSec);
        posProp.setTemporalEaseAtKey(key1,
            [new KeyframeEase(0, 33.33), new KeyframeEase(0, 33.33)],
            [new KeyframeEase(0, 33.33), new KeyframeEase(0, 33.33)]
        );
    } catch(e) {}
}

// ─── COUNT-UP ANIMADO ─────────────────────────────────────────────────────────

function addCountUp(comp, finalValue, prefix, suffix, startTimeSec, fontSize, color) {
    prefix  = prefix  || "";
    suffix  = suffix  || "";
    fontSize = fontSize || 96;
    color   = color   || C.text_primary;

    // Null para el slider
    var nullLayer = comp.layers.addNull(comp.duration);
    nullLayer.name = "COUNTER_NULL_" + finalValue;
    var sliderEffect = nullLayer.property("Effects").addProperty("ADBE Slider Control");
    sliderEffect.property("ADBE Slider Control-0001").setValueAtTime(startTimeSec, 0);
    sliderEffect.property("ADBE Slider Control-0001").setValueAtTime(startTimeSec + 1.5, finalValue);

    // Ease-out exponencial en el slider
    try {
        var k2 = sliderEffect.property("ADBE Slider Control-0001").nearestKeyIndex(startTimeSec + 1.5);
        sliderEffect.property("ADBE Slider Control-0001").setTemporalEaseAtKey(k2,
            [new KeyframeEase(finalValue, 0)],
            [new KeyframeEase(0, 0)]
        );
    } catch(e) {}

    // Texto con expresión
    var textLayer = comp.layers.addText(prefix + String(finalValue) + suffix);
    textLayer.name = "COUNTER_" + finalValue;
    var srcText = textLayer.property("ADBE Text Properties").property("ADBE Text Document");
    var textDoc = srcText.value;
    textDoc.fontSize  = fontSize;
    textDoc.fillColor = color;
    textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    try { textDoc.font = "Inter-Bold"; } catch(e) {}
    srcText.setValue(textDoc);

    // Expresión count-up
    srcText.expression =
        'var ctrl = thisComp.layer("' + nullLayer.name + '")' +
        '           .effect("Slider Control")("Slider"); ' +
        'var val = Math.round(ctrl); ' +
        '"' + prefix + '" + val.toLocaleString("es-MX") + "' + suffix + '"';

    textLayer.property("Position").setValue([WIDTH / 2, HEIGHT / 2]);
    return textLayer;
}

// ─── CONTENIDO ESPECÍFICO POR ESCENA ─────────────────────────────────────────

function populateScene(sceneData, comp) {
    var num = sceneData[0];

    // Escena 5 — Pantalla tipográfica CDMX vs EDOMEX
    if (num === 5) {
        var cdmxLabel = addPlaceholderText(comp, "CDMX",
            96, C.blue_cdmx, WIDTH * 0.28, HEIGHT * 0.35);
        var edomexLabel = addPlaceholderText(comp, "EDOMEX",
            96, C.orange_edomex, WIDTH * 0.72, HEIGHT * 0.35);
        var lineL = addPlaceholderText(comp, "Produce el empleo",
            36, C.text_primary, WIDTH * 0.28, HEIGHT * 0.50);
        var lineR = addPlaceholderText(comp, "Produce los trabajadores",
            36, C.text_primary, WIDTH * 0.72, HEIGHT * 0.50);
        var arrow = addPlaceholderText(comp, "←  →",
            72, C.text_primary, WIDTH * 0.50, HEIGHT * 0.43);

        applySlideUpFadeIn(cdmxLabel,  0.5, 0.6);
        applyFadeIn(arrow,             1.2, 0.4);
        applySlideUpFadeIn(edomexLabel,1.5, 0.6);
        applySlideUpFadeIn(lineL,      2.0, 0.4);
        applySlideUpFadeIn(lineR,      2.0, 0.4);
    }

    // Escena 6 — Counter 7,770,000
    if (num === 6) {
        // El contador empieza a los 15 seg dentro de la escena (01:50+0:15 = 02:05)
        var counter6 = addCountUp(comp, 7770000, "", " viajes/día", 15, 96, C.text_primary);
        counter6.property("Position").setValue([WIDTH / 2, HEIGHT * 0.65]);
        applyFadeIn(counter6, 14.5, 0.5);
    }

    // Escena 9 — Texto "195 estaciones. 0 en Edomex."
    if (num === 9) {
        var txt9 = addPlaceholderText(comp,
            "195 estaciones.",
            72, C.text_primary, WIDTH / 2, HEIGHT * 0.82);
        var txt9b = addPlaceholderText(comp,
            "0 en Edomex.",
            72, C.red_alert, WIDTH / 2, HEIGHT * 0.92);
        applySlideUpFadeIn(txt9,  12, 0.5);
        applySlideUpFadeIn(txt9b, 13, 0.5);
    }

    // Escena 10 — Counter 43.5 y 786000
    if (num === 10) {
        var counter10a = addCountUp(comp, 43.5, "", "% en pobreza", 8, 96, C.red_alert);
        counter10a.property("Position").setValue([WIDTH / 2, HEIGHT * 0.55]);
        var counter10b = addCountUp(comp, 786000, "", " personas", 11, 72, C.text_primary);
        counter10b.property("Position").setValue([WIDTH / 2, HEIGHT * 0.68]);
        var txt10c = addPlaceholderText(comp,
            "2° municipio con más pobres de México",
            36, C.text_secondary, WIDTH / 2, HEIGHT * 0.80);
        applyFadeIn(counter10a, 7.5, 0.5);
        applyFadeIn(counter10b, 10.5, 0.5);
        applySlideUpFadeIn(txt10c, 16, 0.5);
    }

    // Escena 13 — Texto progresivo "El dato que no existe"
    if (num === 13) {
        var line13a = addPlaceholderText(comp,
            "¿Cuánto del ISN de CDMX viene de trabajo mexiquense?",
            44, C.text_light, WIDTH / 2, HEIGHT * 0.38);
        var line13b = addPlaceholderText(comp,
            "Ese dato no existe.",
            72, C.orange_edomex, WIDTH / 2, HEIGHT * 0.52);
        var line13c = addPlaceholderText(comp,
            "Podría calcularse.",
            48, [0.576, 0.776, 0.918], // #93C6E4
            WIDTH / 2, HEIGHT * 0.65);

        applyFadeIn(line13a, 3.0,  0.6);
        applyFadeIn(line13b, 8.0,  0.5);
        applyFadeIn(line13c, 13.0, 0.5);
    }

    // Escena 14 — Texto de cierre
    if (num === 14) {
        var txt14 = addPlaceholderText(comp,
            "La frontera invisible tiene precio.\nNadie lo ha cobrado todavía.",
            36, C.text_light, WIDTH / 2, HEIGHT * 0.87);
        applyFadeIn(txt14, 9, 0.7);
    }
}

// ─── AGREGAR ESCENAS A LA COMPOSICIÓN MAESTRA ─────────────────────────────────

function addSceneToMaster(masterComp, sceneComp, startSec, durSec) {
    var layer = masterComp.layers.add(sceneComp, durSec);
    layer.startTime = startSec;
    layer.name      = sceneComp.name;
    return layer;
}

// ─── AGREGAR GUÍA DE USUARIO ──────────────────────────────────────────────────

function addUserGuideLayer(masterComp) {
    var guide = masterComp.layers.addText(
        "SIGUIENTE PASO: Importar assets\n" +
        "1. Importar WAV (voice/) en carpeta 04_VOICE\n" +
        "2. Importar mapas SVG/PNG en carpeta 02_MAPS\n" +
        "3. Importar gráficos en carpeta 03_CHARTS\n" +
        "4. Ver animation_plan.md para sincronización"
    );
    guide.name = "_GUIA_USUARIO_BORRAR";
    guide.enabled = false; // Capa desactivada — solo referencia
    return guide;
}

// ─── EJECUTAR SCRIPT ──────────────────────────────────────────────────────────

function buildProject() {
    if (!app.project) {
        alert("Error: no hay un proyecto abierto en After Effects.");
        return;
    }

    app.beginUndoGroup("Build " + PROJECT_SLUG);

    try {
        // Carpetas
        var folders = setupFolders();

        // Composición maestra
        var masterComp = createMasterComp(folders);

        // Crear escenas y agregarlas a la maestra
        var sceneComps = [];
        for (var i = 0; i < SCENES.length; i++) {
            var sd   = SCENES[i];
            var comp = createSceneComp(sd, folders);
            populateScene(sd, comp);
            addSceneToMaster(masterComp, comp, sd[2], sd[3]);
            sceneComps.push(comp);
        }

        // Guía de usuario en la maestra
        addUserGuideLayer(masterComp);

        // Mover maestra a carpeta comps
        masterComp.parentFolder = folders.comps;

        app.endUndoGroup();

        alert(
            "✅ Proyecto creado exitosamente.\n\n" +
            "Composición maestra: " + masterComp.name + "\n" +
            "Escenas creadas: " + sceneComps.length + "\n" +
            "Duración total: " + Math.floor(TOTAL_SECONDS / 60) + ":" +
                padNum(TOTAL_SECONDS % 60, 2) + "\n\n" +
            "Siguiente paso:\n" +
            "Importar los assets (WAV, SVG/PNG de mapas y gráficos)\n" +
            "según animation_plan.md"
        );

    } catch (err) {
        app.endUndoGroup();
        alert("Error al construir el proyecto:\n" + err.message +
              "\n\nLínea: " + err.line);
    }
}

buildProject();
