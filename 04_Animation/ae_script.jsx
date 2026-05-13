// ae_script.jsx — Generado por Agente A5
// Proyecto: La geografía invisible del subsidio migrante (2026-05-remesas-mx)
// Fecha: 2026-05-13
// After Effects ExtendScript (ES3 compatible)
//
// INSTRUCCIONES:
//   1. Instalar Bebas Neue Bold y Barlow Medium/Condensed antes de ejecutar
//   2. En After Effects: File > Scripts > Run Script File... > seleccionar este archivo
//   3. El script crea la composición maestra y las 14 composiciones de escena
//   4. Importar manualmente los assets (WAV, SVG, PNG) después de ejecutar
//   5. Consultar animation_plan.md para instrucciones de sincronización

// ─── CONFIGURACIÓN GLOBAL ─────────────────────────────────────────────────────

var PROJECT_SLUG  = "2026-05-remesas-mx";
var PROJECT_TITLE = "La geografía invisible del subsidio migrante";
var FRAME_RATE    = 24;
var WIDTH         = 1920;
var HEIGHT        = 1080;
var TOTAL_SECONDS = 390; // 6:30

// Paleta — Documental Oscuro
// Valores en escala 0–1 para AE (hex / 255)
var C = {
    bg_dark:    [0.071, 0.071, 0.071],   // #121212
    gold:       [0.961, 0.773, 0.094],   // #F5C518 — remesas, acento principal
    red:        [0.902, 0.224, 0.275],   // #E63946 — alerta, riesgo
    blue:       [0.227, 0.525, 1.000],   // #3A86FF — comparativo
    gray:       [0.627, 0.627, 0.627],   // #A0A0A0 — texto secundario
    offwhite:   [0.949, 0.949, 0.941]    // #F2F2F0 — texto principal
};

// Definición de escenas: [número, slug, inicio_seg, duracion_seg]
// Todas las escenas usan fondo oscuro — paleta Documental Oscuro
var SCENES = [
    [1,  "CONTADOR_REMESAS",  0,   25],
    [2,  "MAPA_DUAL",         25,  20],
    [3,  "BRACERO",           45,  30],
    [4,  "FLUJOS_MIG",        75,  25],
    [5,  "HOGAR_RURAL",       100, 20],
    [6,  "DONA_GASTO",        120, 30],
    [7,  "BARRA_INVERSION",   150, 30],
    [8,  "BARRAS_INV",        180, 30],
    [9,  "PIRAMIDE",          210, 30],
    [10, "CICLO",             240, 30],
    [11, "LINEAS_DUAL",       270, 40],
    [12, "RIESGO_EEUU",       310, 35],
    [13, "PUEBLO_VACIO",      345, 25],
    [14, "PREGUNTA_FINAL",    370, 20]
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
    folders.comps  = createFolderIfMissing("00_COMPS");
    folders.scenes = createFolderIfMissing("01_SCENES");
    folders.images = createFolderIfMissing("02_IMAGES");
    folders.maps   = createFolderIfMissing("03_MAPS");
    folders.charts = createFolderIfMissing("04_CHARTS");
    folders.voice  = createFolderIfMissing("05_VOICE");
    folders.music  = createFolderIfMissing("06_MUSIC");
    return folders;
}

// ─── CREAR COMPOSICIÓN MAESTRA ────────────────────────────────────────────────

function createMasterComp(folders) {
    var name = PROJECT_SLUG + "_MASTER";
    var comp = app.project.items.addComp(
        name, WIDTH, HEIGHT, 1, TOTAL_SECONDS, FRAME_RATE
    );
    comp.parentFolder = folders.comps;
    var bg = comp.layers.addSolid(C.bg_dark, "BG_MASTER", WIDTH, HEIGHT, 1);
    bg.moveToEnd();
    return comp;
}

// ─── CREAR COMPOSICIÓN DE ESCENA ──────────────────────────────────────────────

function createSceneComp(sceneData, folders) {
    var num    = sceneData[0];
    var slug   = sceneData[1];
    var durSec = sceneData[3];

    var name = sceneCompName(num, slug);
    var comp = app.project.items.addComp(
        name, WIDTH, HEIGHT, 1, durSec, FRAME_RATE
    );
    comp.parentFolder = folders.scenes;

    // Fondo oscuro para todas las escenas — paleta Documental Oscuro
    var bg = comp.layers.addSolid(C.bg_dark, "BG", WIDTH, HEIGHT, 1);
    bg.moveToEnd();

    return comp;
}

// ─── CAPAS DE TEXTO ───────────────────────────────────────────────────────────

function addText(comp, content, fontSize, color, posX, posY, fontName) {
    fontName = fontName || "BebaNeu-Regular";
    var textLayer = comp.layers.addText(content);
    var srcText   = textLayer.property("ADBE Text Properties")
                              .property("ADBE Text Document");
    var textDoc   = srcText.value;

    textDoc.fontSize  = fontSize;
    textDoc.fillColor = color;
    textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    try { textDoc.font = fontName; } catch(e) {}
    srcText.setValue(textDoc);

    textLayer.property("Transform").property("Position").setValue([posX, posY]);
    textLayer.name = "TXT_" + content.substring(0, 24).replace(/[\s\n]/g, "_");
    return textLayer;
}

// ─── ANIMACIONES BÁSICAS ──────────────────────────────────────────────────────

function applyFadeIn(layer, startSec, durSec) {
    var op = layer.property("Transform").property("Opacity");
    op.setValueAtTime(startSec, 0);
    op.setValueAtTime(startSec + durSec, 100);
    try {
        var k1 = op.nearestKeyIndex(startSec);
        op.setTemporalEaseAtKey(k1,
            [new KeyframeEase(0, 33)],
            [new KeyframeEase(0, 33)]
        );
    } catch(e) {}
}

function applySlideUpFade(layer, startSec, durSec, offsetPx) {
    offsetPx = offsetPx || 30;
    applyFadeIn(layer, startSec, durSec);
    var pos = layer.property("Transform").property("Position");
    var finalPos = pos.value;
    pos.setValueAtTime(startSec, [finalPos[0], finalPos[1] + offsetPx]);
    pos.setValueAtTime(startSec + durSec, finalPos);
    try {
        var k1 = pos.nearestKeyIndex(startSec);
        pos.setTemporalEaseAtKey(k1,
            [new KeyframeEase(0, 33), new KeyframeEase(0, 33)],
            [new KeyframeEase(0, 33), new KeyframeEase(0, 33)]
        );
    } catch(e) {}
}

function applyScaleIn(layer, startSec, durSec) {
    var sc = layer.property("Transform").property("Scale");
    sc.setValueAtTime(startSec, [0, 0]);
    sc.setValueAtTime(startSec + durSec, [100, 100]);
    applyFadeIn(layer, startSec, durSec);
    try {
        var k1 = sc.nearestKeyIndex(startSec);
        sc.setTemporalEaseAtKey(k1,
            [new KeyframeEase(0, 33), new KeyframeEase(0, 33)],
            [new KeyframeEase(0, 33), new KeyframeEase(0, 33)]
        );
    } catch(e) {}
}

// ─── COUNT-UP ANIMADO ─────────────────────────────────────────────────────────

function addCountUp(comp, finalValue, prefix, suffix, startSec, fontSize, color, fontName) {
    prefix   = prefix   || "";
    suffix   = suffix   || "";
    fontSize = fontSize || 120;
    color    = color    || C.gold;
    fontName = fontName || "BebaNeu-Regular";

    // Null con Slider Control para manejar la expresión
    var nullLayer = comp.layers.addNull(comp.duration);
    nullLayer.name = "COUNTER_NULL_" + String(finalValue).replace(/\./g, "_");

    var sliderFx = nullLayer.property("Effects").addProperty("ADBE Slider Control");
    var slider   = sliderFx.property("ADBE Slider Control-0001");
    slider.setValueAtTime(startSec, 0);
    slider.setValueAtTime(startSec + 1.5, finalValue);

    // Ease-out exponencial (velocidad alta al inicio, frena al final)
    try {
        var k2 = slider.nearestKeyIndex(startSec + 1.5);
        slider.setTemporalEaseAtKey(k2,
            [new KeyframeEase(finalValue * 0.5, 5)],
            [new KeyframeEase(0, 0)]
        );
    } catch(e) {}

    // Capa de texto con expresión
    var textLayer = comp.layers.addText(prefix + String(finalValue) + suffix);
    textLayer.name = "COUNTER_" + String(finalValue);
    var srcText = textLayer.property("ADBE Text Properties").property("ADBE Text Document");
    var textDoc = srcText.value;
    textDoc.fontSize  = fontSize;
    textDoc.fillColor = color;
    textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
    try { textDoc.font = fontName; } catch(e) {}
    srcText.setValue(textDoc);

    // Expresión: formatea el número con separadores
    srcText.expression =
        'var ctrl = thisComp.layer("' + nullLayer.name + '")' +
        '           .effect("Slider Control")("Slider"); ' +
        'var val = Math.round(ctrl); ' +
        'var s = "' + prefix + '"; ' +
        'var n = String(val); ' +
        'var result = ""; ' +
        'var count = 0; ' +
        'for (var i = n.length - 1; i >= 0; i--) { ' +
        '    if (count > 0 && count % 3 === 0) result = "," + result; ' +
        '    result = n.charAt(i) + result; ' +
        '    count++; ' +
        '} ' +
        's + result + "' + suffix + '"';

    textLayer.property("Transform").property("Position").setValue([WIDTH / 2, HEIGHT / 2 - 40]);
    return { text: textLayer, null: nullLayer };
}

// ─── SÓLIDO DE COLOR (placeholder para gráficos) ─────────────────────────────

function addColorRect(comp, color, w, h, posX, posY, name) {
    var solid = comp.layers.addSolid(color, name || "RECT", w, h, 1);
    solid.property("Transform").property("Position").setValue([posX, posY]);
    return solid;
}

// ─── CONTENIDO ESPECÍFICO POR ESCENA ─────────────────────────────────────────

function populateScene(sceneData, comp) {
    var num = sceneData[0];

    // ESCENA 01 — Contador tipográfico $67,637,000,000
    if (num === 1) {
        var result = addCountUp(comp, 67637000000, "$", " USD", 2, 96, C.gold);
        result.text.property("Transform").property("Position").setValue([WIDTH / 2, HEIGHT / 2 - 80]);
        applyFadeIn(result.text, 1.8, 0.4);

        var lblUSD = addText(comp, "USD", 32, C.gray, WIDTH / 2, HEIGHT / 2 - 20, "Barlow-Medium");
        applyFadeIn(lblUSD, 4, 0.4);

        var ln1 = addText(comp, "Mayor que los ingresos petroleros", 34, C.offwhite, WIDTH / 2, HEIGHT * 0.68, "Barlow-Medium");
        var ln2 = addText(comp, "Mayor que la IED", 34, C.offwhite, WIDTH / 2, HEIGHT * 0.74, "Barlow-Medium");
        var ln3 = addText(comp, "Primera fuente de divisas de México", 34, C.offwhite, WIDTH / 2, HEIGHT * 0.80, "Barlow-Medium");
        applySlideUpFade(ln1, 8.0, 0.4);
        applySlideUpFade(ln2, 8.5, 0.4);
        applySlideUpFade(ln3, 9.0, 0.4);

        var src = addText(comp, "Banco Mundial, BX.TRF.PWKR.CD.DT, 2024", 22, C.gray, WIDTH - 320, HEIGHT - 40, "BarlowCondensed-Regular");
        applyFadeIn(src, 2, 0.3);
    }

    // ESCENA 02 — Mapa coroplético dual (placeholder texto)
    if (num === 2) {
        var title2 = addText(comp, "TOP 5 ESTADOS — REMESAS 2024", 48, C.gold, WIDTH / 2, HEIGHT * 0.12, "BebaNeu-Regular");
        applySlideUpFade(title2, 0.5, 0.4);

        // Placeholder para los 5 estados
        var estados = ["Michoacán", "Guanajuato", "Jalisco", "Estado de México", "Guerrero"];
        for (var i = 0; i < estados.length; i++) {
            var eLbl = addText(comp, (i + 1) + ". " + estados[i], 36, C.offwhite, WIDTH / 2, HEIGHT * 0.30 + i * 60, "Barlow-Medium");
            applySlideUpFade(eLbl, 1.5 + i * 0.3, 0.4);
        }

        var overlay = addText(comp, "IMPORTAR: M01 remesas por estado + M02 PIB estatal", 24, C.gray, WIDTH / 2, HEIGHT * 0.88, "BarlowCondensed-Regular");
        applyFadeIn(overlay, 0.5, 0.3);

        var src2 = addText(comp, "Banxico SIE, 2024 — INEGI PIBE, 2023", 22, C.gray, WIDTH - 300, HEIGHT - 40, "BarlowCondensed-Regular");
        applyFadeIn(src2, 0.5, 0.3);
    }

    // ESCENA 03 — Bracero (placeholder para imagen + datos sobreimprestos)
    if (num === 3) {
        // El asset de imagen se importa manualmente (I01 — Library of Congress)
        var ph3 = addText(comp, "IMPORTAR: I01 — Bracero Program\n(Library of Congress — dominio público)", 36, C.gray, WIDTH / 2, HEIGHT / 2 - 60, "Barlow-Medium");
        applyFadeIn(ph3, 0, 0.5);

        // Bloque de datos que irá sobreimpuesto en la foto
        var bTitle = addText(comp, "PROGRAMA BRACERO / 1942–1964", 56, C.gold, WIDTH * 0.28, HEIGHT * 0.78, "BebaNeu-Regular");
        bTitle.property("Transform").property("AnchorPoint").setValue([0, 0]);
        var b1 = addText(comp, "4,500,000 mexicanos", 42, C.offwhite, WIDTH * 0.28, HEIGHT * 0.84, "BebaNeu-Regular");
        var b2 = addText(comp, "Michoacán — Guanajuato — Jalisco → California — Texas — Illinois", 28, C.gray, WIDTH * 0.28, HEIGHT * 0.90, "Barlow-Medium");
        applySlideUpFade(bTitle, 3, 0.4);
        applySlideUpFade(b1, 3.2, 0.4);
        applySlideUpFade(b2, 3.4, 0.4);
    }

    // ESCENA 04 — Flujos migratorios (placeholder para mapa + texto)
    if (num === 4) {
        var ph4 = addText(comp, "IMPORTAR: M03 — Flujos migratorios\n(4 capas: 1964 / 1990 / 2010 / 2024)", 36, C.gray, WIDTH / 2, HEIGHT / 2 - 40, "Barlow-Medium");
        applyFadeIn(ph4, 0, 0.5);

        var txt4 = addText(comp, "Las rutas no cambiaron. Solo crecieron.", 44, C.offwhite, WIDTH / 2, HEIGHT * 0.88, "Barlow-Medium");
        applySlideUpFade(txt4, 17, 0.4);

        var src4 = addText(comp, "CONAPO, Índice de Intensidad Migratoria 2020", 22, C.gray, WIDTH - 320, HEIGHT - 40, "BarlowCondensed-Regular");
        applyFadeIn(src4, 0.5, 0.3);
    }

    // ESCENA 05 — Hogar rural (placeholder para imagen + texto sobreimpuesto)
    if (num === 5) {
        var ph5 = addText(comp, "IMPORTAR: I02 — Hogar rural Michoacán\n(Google Imagen 4 — prompt en visual_brief.md)", 36, C.gray, WIDTH / 2, HEIGHT / 2 - 40, "Barlow-Medium");
        applyFadeIn(ph5, 0, 0.5);

        var b5a = addText(comp, "67,637 millones de dólares anuales", 44, C.gold, WIDTH / 2, HEIGHT * 0.72, "BebaNeu-Regular");
        var b5b = addText(comp, "sin banco central  /  sin política pública  /  sin plan", 30, C.offwhite, WIDTH / 2, HEIGHT * 0.82, "Barlow-Medium");
        applySlideUpFade(b5a, 4, 0.4);
        applySlideUpFade(b5b, 4.5, 0.4);
    }

    // ESCENA 06 — Dona gasto hogares (placeholder)
    if (num === 6) {
        var title6 = addText(comp, "¿ADÓNDE VA EL DINERO CUANDO LLEGA?", 52, C.gold, WIDTH / 2, HEIGHT * 0.10, "BebaNeu-Regular");
        applySlideUpFade(title6, 0.3, 0.4);

        // Placeholder dona — se reemplaza con gráfico importado
        var donaPlh = addColorRect(comp, C.gray, 500, 500, WIDTH / 2, HEIGHT / 2, "DONA_PLACEHOLDER");
        applyFadeIn(donaPlh, 2, 0.5);
        donaPlh.property("Transform").property("Opacity").setValueAtTime(0.1, 0);
        donaPlh.property("Transform").property("Opacity").setValueAtTime(0.5, 15);

        var lbl6 = addText(comp, "IMPORTAR: G01 — Gráfico dona ENIGH 2022\n(Datawrapper / matplotlib SVG)", 28, C.gray, WIDTH / 2, HEIGHT * 0.85, "Barlow-Medium");
        applyFadeIn(lbl6, 0.3, 0.3);

        var highlight6 = addText(comp, "Solo 5–15% se ahorra o invierte", 48, C.gold, WIDTH / 2, HEIGHT * 0.92, "BebaNeu-Regular");
        applySlideUpFade(highlight6, 15, 0.4);

        var src6 = addText(comp, "INEGI, ENIGH 2022", 22, C.gray, WIDTH - 200, HEIGHT - 40, "BarlowCondensed-Regular");
        applyFadeIn(src6, 2, 0.3);
    }

    // ESCENA 07 — Barra progreso 5-15%
    if (num === 7) {
        // Barra de fondo
        var barBg = addColorRect(comp, [0.2, 0.2, 0.2], 1600, 80, WIDTH / 2, HEIGHT / 2, "BAR_BG");
        applyFadeIn(barBg, 2, 0.3);

        // Segmento consumo (azul) — 1360px = 85%
        var barConsume = addColorRect(comp, C.blue, 1360, 80, WIDTH / 2 - 120, HEIGHT / 2, "BAR_CONSUME");
        barConsume.property("Transform").property("Position").setValue([640 + 1, HEIGHT / 2]);
        applyFadeIn(barConsume, 2.5, 0.3);

        // Segmento ahorro (dorado) — 240px = 15% max
        var barSave = addColorRect(comp, C.gold, 240, 80, WIDTH - 120, HEIGHT / 2, "BAR_SAVE");
        applyFadeIn(barSave, 3.0, 0.3);

        var pctConsume = addText(comp, "85–95%", 96, C.blue, WIDTH / 2 - 200, HEIGHT / 2 - 100, "BebaNeu-Regular");
        var lblConsume = addText(comp, "consumo básico", 36, C.offwhite, WIDTH / 2 - 200, HEIGHT / 2 - 30, "Barlow-Medium");
        var pctSave    = addText(comp, "5–15%", 96, C.gold, WIDTH - 200, HEIGHT / 2 - 100, "BebaNeu-Regular");
        var lblSave    = addText(comp, "ahorro e inversión", 30, C.gray, WIDTH - 200, HEIGHT / 2 - 30, "Barlow-Medium");

        applySlideUpFade(pctConsume, 5, 0.4);
        applySlideUpFade(lblConsume, 5.5, 0.4);
        applySlideUpFade(pctSave, 6.5, 0.4);
        applySlideUpFade(lblSave, 7.0, 0.4);

        var quote7a = addText(comp, "Las remesas no son capital de desarrollo.", 34, C.offwhite, WIDTH / 2, HEIGHT * 0.78, "Barlow-Medium");
        var quote7b = addText(comp, "Son el precio de vivir donde el Estado decidió no invertir.", 34, C.red, WIDTH / 2, HEIGHT * 0.86, "Barlow-Medium");
        applySlideUpFade(quote7a, 20, 0.4);
        applySlideUpFade(quote7b, 22, 0.4);

        var src7 = addText(comp, "Estudios basados en ENIGH 2022, BID, CEPAL", 22, C.gray, WIDTH - 320, HEIGHT - 40, "BarlowCondensed-Regular");
        applyFadeIn(src7, 2, 0.3);
    }

    // ESCENA 08 — Barras comparativas inversión pública
    if (num === 8) {
        var title8 = addText(comp, "INVERSIÓN PÚBLICA EN INFRAESTRUCTURA / HABITANTE", 44, C.offwhite, WIDTH / 2, HEIGHT * 0.10, "BebaNeu-Regular");
        var sub8   = addText(comp, "Promedio 2018–2023", 28, C.gray, WIDTH / 2, HEIGHT * 0.17, "Barlow-Medium");
        applySlideUpFade(title8, 2, 0.4);
        applyFadeIn(sub8, 2.3, 0.3);

        // Barra izquierda — estados con alta dependencia (roja, más baja)
        var barL = addColorRect(comp, C.red, 240, 280, WIDTH * 0.38, HEIGHT * 0.58, "BAR_ALTA_DEP");
        var lbl8L = addText(comp, "Estados alta\ndependencia remesas", 28, C.offwhite, WIDTH * 0.38, HEIGHT * 0.82, "Barlow-Medium");
        applyFadeIn(barL, 6, 0.6);
        applyFadeIn(lbl8L, 6.3, 0.3);

        // Barra derecha — promedio nacional (azul, más alta)
        var barR = addColorRect(comp, C.blue, 240, 420, WIDTH * 0.62, HEIGHT * 0.52, "BAR_PROMEDIO");
        var lbl8R = addText(comp, "Promedio\nnacional", 28, C.offwhite, WIDTH * 0.62, HEIGHT * 0.82, "Barlow-Medium");
        applyFadeIn(barR, 7, 0.6);
        applyFadeIn(lbl8R, 7.3, 0.3);

        var quote8a = addText(comp, "Las remesas no solo cubren la ausencia del Estado.", 32, C.offwhite, WIDTH / 2, HEIGHT * 0.90, "Barlow-Medium");
        var quote8b = addText(comp, "TAMBIÉN LA SOSTIENEN.", 52, C.red, WIDTH / 2, HEIGHT * 0.96, "BebaNeu-Regular");
        applySlideUpFade(quote8a, 20, 0.4);
        applySlideUpFade(quote8b, 23, 0.4);

        var src8 = addText(comp, "SHCP — Presupuesto ejercido por entidad; BID", 22, C.gray, WIDTH - 300, HEIGHT - 40, "BarlowCondensed-Regular");
        applyFadeIn(src8, 2, 0.3);
    }

    // ESCENA 09 — Pirámide demográfica doble
    if (num === 9) {
        var title9 = addText(comp, "PIRÁMIDE DE EDAD — 2020", 52, C.offwhite, WIDTH / 2, HEIGHT * 0.09, "BebaNeu-Regular");
        applySlideUpFade(title9, 2, 0.4);

        var lbl9L = addText(comp, "MICHOACÁN", 40, C.gray, WIDTH * 0.28, HEIGHT * 0.15, "BebaNeu-Regular");
        var lbl9R = addText(comp, "MÉXICO PROMEDIO", 40, C.blue, WIDTH * 0.72, HEIGHT * 0.15, "BebaNeu-Regular");
        applyFadeIn(lbl9L, 2.2, 0.3);
        applyFadeIn(lbl9R, 2.2, 0.3);

        var ph9 = addText(comp, "IMPORTAR: G04 — Pirámide de edad\nINEGI, Censo de Población 2020\n(dos pirámides lado a lado)", 30, C.gray, WIDTH / 2, HEIGHT / 2 + 40, "Barlow-Medium");
        applyFadeIn(ph9, 2.5, 0.4);

        // Highlight cohorte 20-40 — indicador de texto
        var cohorte = addText(comp, "Cohorte 20–40 años: VISIBLEMENTE MENOR en Michoacán →", 28, C.red, WIDTH / 2, HEIGHT * 0.82, "Barlow-Medium");
        applySlideUpFade(cohorte, 12, 0.4);

        var quote9 = addText(comp, "Los que construirían la economía local ya no están.", 34, C.offwhite, WIDTH / 2, HEIGHT * 0.90, "Barlow-Medium");
        applySlideUpFade(quote9, 15, 0.4);

        var src9 = addText(comp, "INEGI, Censo de Población y Vivienda 2020", 22, C.gray, WIDTH - 320, HEIGHT - 40, "BarlowCondensed-Regular");
        applyFadeIn(src9, 2, 0.3);
    }

    // ESCENA 10 — Diagrama ciclo cerrado
    if (num === 10) {
        // 4 nodos en disposición de cuadrado
        // Centro del comp: (960, 540). Nodos a 300px del centro.
        var cx = WIDTH / 2;
        var cy = HEIGHT / 2;
        var r  = 260;

        var nodePositions = [
            [cx, cy - r],       // arriba: "Economía local estancada"
            [cx + r, cy],       // derecha: "Jóvenes migran"
            [cx, cy + r],       // abajo: "Remesas llegan"
            [cx - r, cy]        // izquierda: "Estado no invierte"
        ];

        var nodeLabels = [
            "Economía local\nestancada",
            "Jóvenes migran",
            "Remesas llegan",
            "Estado\nno invierte"
        ];

        var nodeColors = [C.gold, C.red, C.blue, C.gray];

        for (var i = 0; i < 4; i++) {
            var nSolid = comp.layers.addSolid(nodeColors[i], "NODE_" + (i + 1), 180, 80, 1);
            nSolid.property("Transform").property("Position").setValue(nodePositions[i]);
            applyScaleIn(nSolid, 2 + i * 0.5, 0.5);

            var nText = addText(comp, nodeLabels[i], 24, C.bg_dark, nodePositions[i][0], nodePositions[i][1], "Barlow-Medium");
            applyFadeIn(nText, 2.2 + i * 0.5, 0.3);
        }

        // Texto de cierre del ciclo
        var cycleTxt = addText(comp, "SESENTA AÑOS. EL MISMO CICLO.", 64, C.offwhite, WIDTH / 2, HEIGHT * 0.92, "BebaNeu-Regular");
        applySlideUpFade(cycleTxt, 18, 0.4);

        // Nota de producción
        var note10 = addText(comp, "Conectar nodos con flechas curvas en AE (Path con trim path)\nFlecha final (4→1) en #F5C518 — cierra el ciclo", 24, C.gray, WIDTH / 2, HEIGHT * 0.15, "BarlowCondensed-Regular");
        applyFadeIn(note10, 0, 0.5);
        note10.enabled = false; // Solo referencia, desactivar antes de render
    }

    // ESCENA 11 — Gráfico líneas doble (placeholder)
    if (num === 11) {
        var title11 = addText(comp, "REMESAS vs. POBREZA EXTREMA — 2000–2024", 48, C.offwhite, WIDTH / 2, HEIGHT * 0.09, "BebaNeu-Regular");
        applySlideUpFade(title11, 2, 0.4);

        var ph11 = addText(comp, "IMPORTAR: G06 — Gráfico de líneas doble\nRemesas (USD) + % pobreza extrema CONEVAL\n(Datawrapper d3-lines / matplotlib)", 32, C.gray, WIDTH / 2, HEIGHT / 2, "Barlow-Medium");
        applyFadeIn(ph11, 2, 0.4);

        var annot11 = addText(comp, "Las remesas sí funcionan.\nPero 60 años no son suficientes para salir de la trampa.", 34, C.offwhite, WIDTH / 2, HEIGHT * 0.80, "Barlow-Medium");
        applySlideUpFade(annot11, 18, 0.4);

        var src11 = addText(comp, "Banco Mundial WDI; CONEVAL, medición de pobreza 2000–2022", 22, C.gray, WIDTH - 400, HEIGHT - 40, "BarlowCondensed-Regular");
        applyFadeIn(src11, 2, 0.3);
    }

    // ESCENA 12 — Mapa riesgo EE.UU. (placeholder)
    if (num === 12) {
        var title12 = addText(comp, "UN ÚNICO PUNTO DE FALLA", 72, C.red, WIDTH / 2, HEIGHT * 0.12, "BebaNeu-Regular");
        applySlideUpFade(title12, 2, 0.4);

        var ph12 = addText(comp, "IMPORTAR: M04 — Mapa EE.UU. + México\n(estados alta concentración + estados dependientes de remesas)", 30, C.gray, WIDTH / 2, HEIGHT / 2, "Barlow-Medium");
        applyFadeIn(ph12, 2, 0.4);

        // Iconos de riesgo — texto placeholder
        var risk1 = addText(comp, "⚠ Recesión", 36, C.red, WIDTH * 0.25, HEIGHT * 0.72, "Barlow-Medium");
        var risk2 = addText(comp, "⚠ Política migratoria", 36, C.red, WIDTH * 0.50, HEIGHT * 0.72, "Barlow-Medium");
        var risk3 = addText(comp, "⚠ Deportaciones", 36, C.red, WIDTH * 0.75, HEIGHT * 0.72, "Barlow-Medium");
        applyScaleIn(risk1, 8, 0.4);
        applyScaleIn(risk2, 12, 0.4);
        applyScaleIn(risk3, 16, 0.4);

        var quote12 = addText(comp, "Si el flujo se interrumpe, no tienen alternativa.", 34, C.offwhite, WIDTH / 2, HEIGHT * 0.88, "Barlow-Medium");
        applySlideUpFade(quote12, 26, 0.4);

        var src12 = addText(comp, "Pew Research Center 2023; CONAPO", 22, C.gray, WIDTH - 280, HEIGHT - 40, "BarlowCondensed-Regular");
        applyFadeIn(src12, 2, 0.3);
    }

    // ESCENA 13 — Pueblo vacío (placeholder para imagen + texto)
    if (num === 13) {
        var ph13 = addText(comp, "IMPORTAR: I03 — Calle pueblo rural\n(Google Imagen 4 — prompt en visual_brief.md)", 34, C.gray, WIDTH / 2, HEIGHT / 2 - 40, "Barlow-Medium");
        applyFadeIn(ph13, 0, 0.5);

        var t13a = addText(comp, "Las comunidades donde la emigración baja", 36, C.offwhite, WIDTH / 2, HEIGHT * 0.78, "Barlow-Medium");
        var t13b = addText(comp, "aún no tienen economía local que las reciba.", 36, C.offwhite, WIDTH / 2, HEIGHT * 0.86, "Barlow-Medium");
        applySlideUpFade(t13a, 7, 0.4);
        applySlideUpFade(t13b, 8, 0.4);

        var src13 = addText(comp, "CONAPO", 22, C.gray, WIDTH - 140, HEIGHT - 40, "BarlowCondensed-Regular");
        applyFadeIn(src13, 2, 0.3);
    }

    // ESCENA 14 — Pregunta final tipográfica
    if (num === 14) {
        // 3s de negro antes de la primera línea
        var line14a = addText(comp, "¿Quién paga la deuda", 72, C.offwhite, WIDTH / 2, HEIGHT * 0.38, "BebaNeu-Regular");
        var line14b = addText(comp, "de sesenta años", 72, C.gold, WIDTH / 2, HEIGHT * 0.52, "BebaNeu-Regular");
        var line14c = addText(comp, "de desarrollo postergado?", 72, C.offwhite, WIDTH / 2, HEIGHT * 0.66, "BebaNeu-Regular");

        // Sin slide-up — solo fade puro (escena más restringida del video)
        applyFadeIn(line14a, 3.0, 0.6);
        applyFadeIn(line14b, 6.0, 0.5);
        applyFadeIn(line14c, 9.0, 0.5);

        // Fade final a negro: la opacidad del fondo (una capa encima) sube a 100
        var fadeOut = comp.layers.addSolid(C.bg_dark, "FADE_TO_BLACK", WIDTH, HEIGHT, 1);
        var fadeOp  = fadeOut.property("Transform").property("Opacity");
        fadeOp.setValueAtTime(14.5, 0);
        fadeOp.setValueAtTime(16.0, 100); // fade final en 1.5s
    }
}

// ─── AGREGAR ESCENAS A LA COMPOSICIÓN MAESTRA ─────────────────────────────────

function addSceneToMaster(masterComp, sceneComp, startSec, durSec) {
    var layer = masterComp.layers.add(sceneComp, durSec);
    layer.startTime = startSec;
    layer.name      = sceneComp.name;
    return layer;
}

// ─── GUÍA DE USUARIO ──────────────────────────────────────────────────────────

function addUserGuide(masterComp) {
    var guide = masterComp.layers.addText(
        "PASOS DESPUÉS DE EJECUTAR ESTE SCRIPT:\n" +
        "1. Importar WAV de voz (11 chunks) → carpeta 05_VOICE\n" +
        "2. Importar imágenes (I01 B&W Bracero, I02 Hogar, I03 Pueblo) → 02_IMAGES\n" +
        "3. Importar mapas SVG/PNG (M01-M04) → 03_MAPS\n" +
        "4. Importar gráficos SVG (G01-G06) → 04_CHARTS\n" +
        "5. Sincronizar con animation_plan.md\n" +
        "6. Desactivar capas _PLACEHOLDER antes de render"
    );
    guide.name = "_GUIA_USUARIO — BORRAR ANTES DE RENDER";
    guide.enabled = false;
    return guide;
}

// ─── EJECUTAR SCRIPT ──────────────────────────────────────────────────────────

function buildProject() {
    if (!app.project) {
        alert("Error: no hay un proyecto abierto en After Effects. Crea o abre un proyecto primero.");
        return;
    }

    app.beginUndoGroup("Build " + PROJECT_SLUG);

    try {
        var folders = setupFolders();
        var masterComp = createMasterComp(folders);
        var sceneComps = [];

        for (var i = 0; i < SCENES.length; i++) {
            var sd   = SCENES[i];
            var comp = createSceneComp(sd, folders);
            populateScene(sd, comp);
            addSceneToMaster(masterComp, comp, sd[2], sd[3]);
            sceneComps.push(comp);
        }

        addUserGuide(masterComp);
        masterComp.parentFolder = folders.comps;

        app.endUndoGroup();

        alert(
            "Proyecto creado exitosamente.\n\n" +
            "Composición maestra: " + masterComp.name + "\n" +
            "Escenas: " + sceneComps.length + "\n" +
            "Duración: " + Math.floor(TOTAL_SECONDS / 60) + ":" +
                padNum(TOTAL_SECONDS % 60, 2) + "\n\n" +
            "Siguiente paso: importar assets (WAV, SVG, PNG)\n" +
            "según animation_plan.md"
        );

    } catch (err) {
        app.endUndoGroup();
        alert("Error al construir el proyecto:\n" + err.message + "\nLínea: " + err.line);
    }
}

buildProject();
