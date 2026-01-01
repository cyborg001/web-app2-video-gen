# AI Video Generator - Manual de Usuario

## 📋 Requisitos del Sistema

- **Sistema Operativo**: Windows 10/11
- **Python**: 3.10 o superior
- **FFmpeg**: Instalado y en el PATH del sistema
- **Conexión a Internet**: Para APIs de IA y TTS

## 🚀 Instalación

### 1. Instalar Python

Si no tienes Python instalado:
1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, **marca la opción "Add Python to PATH"**
3. Verifica la instalación abriendo CMD y ejecutando: `python --version`

### 2. Instalar FFmpeg

FFmpeg es necesario para el procesamiento de video:
1. Descarga FFmpeg desde [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extrae el archivo ZIP
3. Agrega la carpeta `bin` de FFmpeg al PATH del sistema
4. Verifica ejecutando en CMD: `ffmpeg -version`

### 3. Instalar Dependencias

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará todas las librerías necesarias (Django, MoviePy, ElevenLabs, etc.)

### 4. Configurar Variables de Entorno

Crea o edita el archivo `.env` en la carpeta `web_app` con tus claves API:

```env
GEMINI_API_KEY=tu_clave_api_de_gemini
ELEVENLABS_API_KEY=tu_clave_api_de_elevenlabs
MYMEMORY_EMAIL=tu_email@ejemplo.com
EDGE_VOICE=es-ES-AlvaroNeural
GEMINI_MODEL_NAME=gemini-flash-latest
```

**Obtener las claves API:**
- **Gemini API**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **ElevenLabs API**: [ElevenLabs](https://elevenlabs.io/) (opcional, puedes usar Edge TTS gratis)

## ▶️ Iniciar la Aplicación

### Opción 1: Usar el archivo BAT (Recomendado)

Simplemente haz doble clic en `Start_App.bat`

### Opción 2: Línea de comandos

```bash
cd web_app
python run_app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://127.0.0.1:8888`

## 📖 Guía de Uso

### 1. Crear un Nuevo Proyecto

1. Haz clic en **"+ Nuevo Proyecto"**
2. Ingresa un título para tu video
3. Escribe o pega tu guion en el formato:
   ```
   TÍTULO | imagen.png | DIR | Texto a locutar
   ```
4. Selecciona el motor de voz (Edge TTS o ElevenLabs)
5. Elige la relación de aspecto (Horizontal o Vertical/Portrait)
6. Opcionalmente, agrega música de fondo (con **Audio Ducking** profesional incluido)
7. Haz clic en **"Generar Video"**

### 2. Gestionar Assets

- **Subir Assets**: Ve a "Assets" → "Subir Assets" para agregar imágenes y videos
- **Ver Assets**: Todos tus assets se muestran en la página de Assets
- **Eliminar Assets**: Usa el botón de eliminar junto a cada asset

### 3. Gestionar Música

- **Subir Música**: Ve a "Música" → "Subir Música" para agregar archivos MP3/WAV
- **Usar en Videos**: Selecciona la música al crear un proyecto
- **Ajustar Volumen**: Usa el control deslizante de volumen de música

### 4. AI Hub (Investigación de Noticias)

1. Ve a **"AI Hub"**
2. Haz clic en **"Refrescar Noticias"** para obtener las últimas noticias de IA
3. Selecciona una noticia
4. Haz clic en **"Generar Script"** para crear automáticamente un guion
5. El guion generado se abrirá en la página de creación de proyecto

### 5. Subir a YouTube

1. Ve al detalle de un proyecto completado
2. Haz clic en **"Autorizar YouTube"** (solo la primera vez)
3. Haz clic en **"Subir a YouTube"**
4. El video se subirá automáticamente a tu canal

## 🎨 Formato del Guion Profesional (V2)

El guion debe seguir este formato de 4 columnas:

```
TITULO | archivo_visual.png | DIRECCIÓN | Texto que se locutará
```

**Parámetros de DIRECCIÓN (Efecto Ken Burns):**
- **DER**: Derecha a Izquierda.
- **IZQ**: Izquierda a Derecha.
- **ABA**: Arriba hacia Abajo.
- **ARR**: Abajo hacia Arriba.
- *Vacío*: Imagen estática.

**Etiquetas Especiales:**
- **`[PAUSA:X]`**: Inserta un silencio de X segundos (la música subirá automáticamente durante la pausa).

## 🎵 Música de Fondo y Audio Ducking

- **Audio Ducking**: La música baja automáticamente al 15% durante la voz y sube al 100% en silencios.
- **Fade Transitions**: Todas las transiciones de audio tienen un suavizado de 0.2s para evitar ruidos.
- Sube archivos MP3 o WAV a la biblioteca de música.
- Selecciona la música al crear un proyecto.
- Ajusta el volumen maestro con el control deslizante (0.0 a 1.0).

## 🔧 Solución de Problemas

### La aplicación no inicia
- Verifica que Python esté instalado: `python --version`
- Verifica que las dependencias estén instaladas: `pip list`
- Revisa el archivo `.env` para asegurarte de que las claves API sean correctas

### Error de FFmpeg
- Verifica que FFmpeg esté instalado: `ffmpeg -version`
- Asegúrate de que FFmpeg esté en el PATH del sistema

### Video no se genera
- Revisa los logs en la página de detalle del proyecto
- Verifica que todos los assets referenciados en el guion existan
- Asegúrate de que el formato del guion sea correcto

### Error de API
- Verifica que tus claves API sean válidas
- Para Gemini: [Google AI Studio](https://makersuite.google.com/app/apikey)
- Para ElevenLabs: [ElevenLabs Dashboard](https://elevenlabs.io/)

## 📝 Notas Importantes

- **Base de Datos**: Se crea automáticamente en `web_app/db.sqlite3`
- **Media**: Los archivos se guardan en `web_app/media/`
- **Logs**: Los logs de generación se muestran en tiempo real en la página de detalle del proyecto
- **Puerto**: La aplicación usa el puerto 8888 por defecto

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs en la consola donde ejecutaste la aplicación
2. Verifica que todas las dependencias estén instaladas correctamente
3. Asegúrate de que FFmpeg esté funcionando
4. Revisa el archivo `.env` para configuración correcta

## 📄 Licencia

Este software se proporciona "tal cual" sin garantías de ningún tipo.
