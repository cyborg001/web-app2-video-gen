# 🎬 Manual de Usuario - AI Video Gen (EXE Edition)

¡Bienvenido a la herramienta definitiva para creación de contenido con IA! Esta versión ejecutable está diseñada para ser **portátil e independiente**.

> [!IMPORTANT]
> **No necesitas instalar Python ni ninguna dependencia técnica.** El archivo `AI_Video_Generator.exe` contiene todo lo necesario para funcionar por sí solo.

---

## ⚡ Estructura del Software

Esta aplicación se divide en dos grandes "cerebros":
1.  **AI Hub (Researcher)**: El lugar donde investigas noticias, tendencias y gestionas fuentes de información.
2.  **Generador de Video**: Donde transformas esos guiones en piezas audiovisuales con voz, música e imágenes.

---

## 🛠️ Modos de Uso

Dependiendo de tus necesidades y configuración, puedes usar la app de dos formas:

### 1. Modo Normal (Sin APIs externas)
Ideal para usuarios que ya tienen sus propios guiones y recursos.
*   **Qué puedes hacer**:
    *   Crear proyectos subiendo tus propios guiones en formato `TÍTULO | imagen.png | Texto`.
    *   Subir tu propia música de fondo.
    *   Generar narraciones usando el motor gratuito (Edge TTS).
    *   Gestionar y previsualizar tus videos generados.
    *   No hay limites en el video, depende del tamano del guion.
*   **Requerimientos**: Ninguno. Funciona "out of the box".

### 2. Modo Power User (Con IA habilitada)
Desbloquea todo el potencial de la automatización configurando una `GEMINI_API_KEY` en el archivo `.env`.
*   **Qué puedes hacer**:
    *   **Investigación Inteligente**: La IA lee noticias por ti y resume lo más importante.
    *   **Generador de Guiones Automático**: Transforma una noticia en un script de YouTube Shorts/TikTok con un solo clic.(El sistema esta configurado para generar guiones para shorts o Reels de dos minutos)
    *   **Prompts Sugeridos**: La IA te dice qué imágenes necesitas para cada escena.
    *   **Subida a YouTube**: Automatiza la publicación de tus videos terminados.
*   **Requerimientos**: Configurar el archivo `.env` (instrucciones abajo).

---

## ⚙️ Configuración del archivo `.env`

Si quieres ser un **Power User**, abre o crea el archivo `.env` en la carpeta de la aplicación y añade estas líneas:

| Variable | Descripción | Valor sugerido |
| :--- | :--- | :--- |
| **GEMINI_API_KEY** | Habilita el cerebro de IA para guiones e investigación. | Tu clave de [Google AI Studio](https://aistudio.google.com/). |
| **ELEVENLABS_API_KEY** | Habilita voces ultra-realistas (opcional). | Tu clave de ElevenLabs. |
| **MYMEMORY_EMAIL** | Mejora la traducción de noticias internacionales. | Tu correo personal. |

---

## 🚀 Guía de Funciones

### 📡 AI Hub & Smart Research
Ubicado en la pestaña **AI Hub**.
-   **Actualizar Hub**: Conecta con las mejores fuentes de noticias del mundo.
-   **Fuentes**: Puedes añadir tus propios links de noticias o feeds RSS.
-   **Generar Guion**: Una vez que encuentras una noticia interesante, dale al botón de "Generar Guion". El sistema usará la IA para redactar un script dinámico y guardarlo listo para producción. (El sistema esta configurado para generar guiones para videos de 2 minutos)

### 🎬 Generador de Video (Crear Nuevo)
Aquí es donde ocurre la magia.
-   **Script**: Pega tu guion. Si lo generaste en el Hub, aparecerá aquí solo.
-   **Motor de Voz**: Elige entre el motor gratuito (Edge) o el premium (ElevenLabs).
-   **Assets**: Asegúrate de que las imágenes mencionadas en el guion existan en tu carpeta de trabajo. Si no existen, el sistema usará una imagen por defecto para que el video no falle.

### 📂 Gestión de Assets y Música
-   Puedes subir archivos de fondo y música directamente desde la web. No es necesario que navegues por carpetas de Windows a menos que quieras organizar miles de archivos.

### 📺 Integración con YouTube
Si configuraste tu `client_secrets.json` (ID de cliente de OAuth), verás un botón de **"Subir a YouTube"** en los detalles de cada proyecto finalizado.

---

## ❓ Preguntas Frecuentes

**¿Dónde se guardan los videos finales?**
En la carpeta `media/videos/` dentro del directorio de la aplicación.

**¿Puedo usar mi propia voz grabada?**
Actualmente el sistema está optimizado para TTS (Texto a Voz) automático para maximizar la velocidad de producción.

**¿Qué pasa si una noticia da error al investigar?**
Algunos sitios web bloquean el acceso automatizado. Prueba con otra fuente o pega el texto manualmente en el creador de proyectos.

---
¡Disfruta de la potencia de la IA en tus manos! 🚀
