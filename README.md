# 🎬 AI Video Generator Pro (v2.9.0)

**La solución definitiva para la creación automatizada de contenido audiovisual de alto impacto.**

AI Video Generator Pro es una potente aplicación web diseñada para transformar noticias, artículos o guiones de texto en videos profesionales optimizados para redes sociales (YouTube Shorts, TikTok, Reels). Utilizando una combinación de Django, MoviePy y las APIs más avanzadas de Inteligencia Artificial (Gemini, ElevenLabs, Edge TTS), este sistema permite pasar de una idea a un video renderizado en cuestión de minutos.

---

## 🔥 Características Principales

### 🎥 Engine de Video Cinematográfico
- **Ken Burns Pro (Quirúrgico)**: Control total del movimiento de cámara en imágenes fijas. Usa sintaxis direccional (`DER`, `IZQ`, `ABA`, `ARR`) o precisión por porcentajes (`DIR:START:END`) para un encuadre perfecto.
- **Dinamismo Automático**: Capacidad de alternar entre formatos 16:9 y 9:16 (Shorts) con re-encuadre inteligente.
- **CTA Integrado**: Generación automática de videos de cierre (Like/Suscripción) con animaciones fluidas.

### 🎧 Audio & Sonido Profesional
- **Intelligent Audio Ducking**: La música de fondo se atenúa automáticamente al 15% durante la voz y recupera el 100% en los silencios.
- **Smooth Fades**: Transiciones de volumen de 0.2s para una experiencia sonora limpia y sin ruidos bruscos.
- **Manual Pauses**: Control de silencios rítmicos mediante la etiqueta `[PAUSA:X]` directamente en el guion.
- **Dual TTS Engine**: Soporte para voces naturales de Microsoft Edge (Gratis) y voces ultra-realistas de ElevenLabs (Premium).

### 🧠 Inteligencia Artificial (AI Hub)
- **Smart Research**: Investigación automática de noticias y tendencias mediante Gemini AI.
- **Hook-First Scripting**: Generación de guiones optimizados para retención absoluta desde los primeros 2 segundos.
- **Prompts Visuales**: Sugerencias automáticas de imágenes para cada escena del video.

---

## 🛠️ Instalación y Configuración

1. **Clonar y Preparar**:
   ```bash
   git clone [TU_URL_DE_GITHUB]
   cd web-app2-video-gen/web_app
   pip install -r requirements.txt
   ```

2. **Variables de Entorno**:
   Crea un archivo `.env` en la raíz de `web_app/` con:
   ```env
   GEMINI_API_KEY=tu_clave
   ELEVENLABS_API_KEY=tu_clave
   EDGE_VOICE=es-DO-EmilioNeural
   PORT=8888
   ```

3. **Ejecutar**:
   ```bash
   python run_app.py
   ```

---

## 🎨 El Nuevo Formato de Guion (Pro)

El sistema utiliza un estándar de 4 columnas para un control total:
`TÍTULO | IMAGEN | DIRECCIÓN | TEXTO`

**Ejemplo de alto rendimiento:**
```text
HOOK | noticia.png | DER:10:60 | ¡90% de éxito! El 2025 marca el fin de lo incurable.
PAUSA | lab.jpg | | [PAUSA:1.5]
DETALLE | adn.png | ABA | La edición genética CRISPR ya es una realidad médica.
```

---

## 📈 Historial de Versiones
- **v2.9.0**: Independización de repositorio y estandarización Pro.
- **v2.8.0**: Control quirúrgico de Ken Burns por porcentajes.
- **v2.6.0**: Implementación de la Estrategia de Gancho (Hook-First).
- **v2.4.0**: Suavizado de Audio Ducking y Fades profesionales.

---

Desarrollado con ❤️ para la comunidad de creadores de contenido AI. 🚀
