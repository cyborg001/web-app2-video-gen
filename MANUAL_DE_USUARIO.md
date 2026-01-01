# 🎬 Manual de Usuario - AI Video Gen (Versión Profesional)

¡Bienvenido a la herramienta definitiva para creación de contenido con IA! Esta versión está diseñada para ofrecer resultados de nivel de estudio de forma automatizada.

---

## ⚡ Estructura del Software

Esta aplicación se divide en dos grandes "cerebros":
1.  **AI Hub (Researcher)**: Investiga noticias, tendencias y gestiona fuentes.
2.  **Generador de Video**: Transforma guiones en piezas audiovisuales con voz, música dinámica e imágenes con movimiento.

---

## 🛠️ Modos de Uso

### 1. Modo Normal (Sin APIs externas)
Ideal para usuarios con guiones propios.
*   **Qué puedes hacer**:
    *   Crear proyectos usando el **Formato Pro** de 4 columnas.
    *   Generar narraciones con el motor gratuito (Edge TTS).
    *   Aplicar efectos Ken Burns manuales.
    *   Subir música y gestionar el **Audio Ducking** automático.

### 2. Modo Power User (IA Full)
Configura tu `GEMINI_API_KEY` en el archivo `.env`.
*   **Investigación Inteligente**: La IA resume noticias por ti.
*   **Generador de Guiones Automático**: Crea scripts de 2 min con un clic.
*   **Estrategia Hook-First**: Guiones optimizados para retención de 2 segundos.

---

## 🎬 Formato de Guion Profesional (V2.0)

El sistema ahora soporta 4 columnas separadas por tubos (` | `). 

**Estructura**: `TÍTULO | IMAGEN | DIRECCIÓN | TEXTO`

### 1. El Efecto Ken Burns (Columna DIRECCIÓN)
Controla el movimiento de tus imágenes fijas:
- **DER / IZQ / ABA / ARR**: Direcciones básicas (0% a 100%).
- **Advanced Control**: Usa `DIR:START:END` (Ej: `DER:10:45`).
    - Indica qué porcentaje de la imagen quieres recorrer. Útil para encuadres quirúrgicos.
- *Vacío*: La imagen se queda estática.

### 2. Pausas y Silencios de Producción
Si quieres que el locutor se calle para que la música suba de volumen, usa la etiqueta:
**`[PAUSA:segundos]`** (Ej: `[PAUSA:3.5]`) en la columna de Texto.

---

## 🎧 Audio Ducking Inteligente

La aplicación incluye un sistema de mezcla profesional:
- **Atenuación Automática**: La música baja de volumen cuando hay voz (15%) y sube al 100% durante los silencios.
- **Transiciones Suaves (Fades)**: Cambios de volumen de 0.2s para evitar ruidos o chasquidos.

---

## ⚙️ Configuración del archivo `.env`

Abre el archivo `.env` para personalizar tu experiencia:
- **GEMINI_API_KEY**: Cerebro de IA para guiones e investigación.
- **ELEVENLABS_API_KEY**: Habilita voces ultra-realistas (opcional).
- **EDGE_VOICE**: Voz por defecto (Ej: `es-DO-EmilioNeural`).
- **PORT**: Puerto donde se lanzará la app (Por defecto: `8888`).
- **MYMEMORY_EMAIL**: Para mejorar la traducción de noticias internacionales.

---

## 🚀 Estrategia de Contenido (Ley del Gancho)
Para maximizar tus visualizaciones en redes sociales:
1. **Hook (0-2s)**: Empieza con un dato impactante, no con saludos.
2. **Cuerpo**: Cambia de imagen o dirección de Ken Burns cada 3-5 segundos.
3. **Conclusión Profunda**: Aporta un valor reflexivo antes de terminar.
4. **CTA**: Haz una pregunta para generar comentarios.

---
¡Disfruta de la potencia de la producción automatizada! 🚀
