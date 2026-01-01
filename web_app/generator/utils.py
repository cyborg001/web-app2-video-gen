import requests
import os
import numpy as np
import random
import asyncio
import json
from django.conf import settings
# from moviepy import ImageClip, AudioFileClip, ... (Moved to function level)
# import edge_tts (Moved to function level)
# from elevenlabs.client import ElevenLabs (Moved to function level)
# from elevenlabs import save (Moved to function level)
from django.utils.text import slugify

def generate_script_ai(news_item):
    """
    Generates a high-impact script and visual prompts for a news item using Gemini API.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None, "Error: No se encontró GEMINI_API_KEY en las variables de entorno.", None

    prompt = f"""
Eres un director y guionista experto en YouTube Shorts para el canal "Noticias de IA y ciencias".
Tu objetivo es transformar la noticia adjunta en un guion CINEMATOGRÁFICO de alto impacto (máx 2.5 min).

REGLAS CRÍTICAS DE FORMATO (PRO):
1. El guion debe usar exactamente 4 columnas: TITULO | IMAGEN | DIRECCION | TEXTO
2. El separador debe ser " | " (tubo con espacios).
3. Columna DIRECCION: Usa 'DER', 'IZQ', 'ABA', 'ARR' para efecto Ken Burns, o déjalo vacío para imagen estática. Sé creativo con el movimiento.
4. Columna TEXTO: 
   - NO uses tablas, negritas, corchetes o llaves (excepto la etiqueta de pausa).
   - Inserte pausas estratégicas usando [PAUSA:X] (ej: [PAUSA:2.0]) en líneas dedicadas para crear silencios de producción y subir la música.
5. Las imágenes deben tener nombres descriptivos técnicos (ej: 'nanobots_medicina.png').

ESTRATEGIA DE CONTENIDO (HOOK-FIRST):
- El Hook (0-2s): Empieza con un gancho ultra-impactante basado en el dato más loco de la noticia. No saludes al principio, ve directo al grano.
- Ritmo: Cambia de imagen o de dirección cada 3-5 segundos.
- Conclusión Profunda: Antes del cierre, aporta una reflexión filosófica o técnica de alto nivel.
- Cierre: Una pregunta provocadora para generar comentarios + Call to action.

DATOS DE LA NOTICIA:
Título: {news_item.title}
Resumen: {news_item.summary}
Fuente: {news_item.source.name}

RESPUESTA REQUERIDA (Formato JSON):
Responde con un objeto JSON con:
1. "script": El guion en formato TITULO | imagen.png | DIR | Texto (incluyendo etiquetas [PAUSA:X] en líneas nuevas cuando sea dramáticamente necesario).
2. "prompts": Lista de objetos con "file" y "prompt" (descripción detallada para generar la imagen).
3. "music_suggestion": Estilo de música ideal.

Responde ÚNICAMENTE el JSON.
"""

    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            # Extract JSON from markdown code blocks if present
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            elif '```' in content:
                # Remove any code fences
                content = re.sub(r'```\w*\n?', '', content)
            
            import json
            data = json.loads(content.strip())
            return data.get('script'), data.get('prompts'), data.get('music_suggestion')
        else:
            human_msg = "No se pudo conectar con la IA. Por favor, asegúrate de que tu 'GEMINI_API_KEY' en el archivo '.env' sea válida y que tengas saldo en tu cuenta de Google AI Studio."
            return None, f"⚠️ {human_msg} (Error {response.status_code})", None
    except Exception as e:
        human_msg = "Parece que hay un problema de conexión o configuración. Revisa que tu internet funcione correctamente y que el nombre del modelo en el archivo '.env' sea el correcto."
        return None, f"🛑 {human_msg} (Detalle: {str(e)})", None

class ProjectLogger:
    def __init__(self, project):
        self.project = project
        self.log_buffer = []

    def log(self, message):
        print(f"[Project {self.project.id}] {message}")
        self.log_buffer.append(message)
        self.project.log_output = "\n".join(self.log_buffer)
        self.project.save(update_fields=['log_output'])

async def generate_audio_edge(text, output_path, voice="es-ES-AlvaroNeural"):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def apply_dynamic_pan(image_path, target_size, duration, direction=None):
    """
    Applies Ken Burns effect following user-defined rules:
    - Scale smaller image dimension to match corresponding player dimension.
    - If direction is provided (DER, IZQ, ABA, ARR), force that movement.
    - If no direction, follow default logic (L-R or B-T based on format).
    """
    from moviepy import ImageClip, CompositeVideoClip
    
    img_clip = ImageClip(image_path).with_duration(duration)
    w_target, h_target = target_size
    w_img, h_img = img_clip.size
    
    is_short = w_target < h_target
    is_square = abs(w_img - h_img) / max(w_img, h_img) < 0.05
    
    # Parse advanced direction syntax: DIR:START:END (e.g., DER:10:45)
    base_dir = direction
    start_pct = 0.0
    end_pct = 100.0
    
    if direction and ':' in direction:
        dir_parts = direction.split(':')
        base_dir = dir_parts[0].strip()
        try:
            if len(dir_parts) >= 2:
                start_pct = max(0.0, min(100.0, float(dir_parts[1])))
            if len(dir_parts) >= 3:
                end_pct = max(0.0, min(100.0, float(dir_parts[2])))
        except ValueError:
            pass # Fallback to 0-100 if invalid numbers

    # MANUAL DIRECTION LOGIC (Highest Priority)
    if base_dir in ['DER', 'IZQ', 'ABA', 'ARR']:
        if base_dir in ['DER', 'IZQ']:
            # Horizontal movement: scale height to match target height
            img_clip = img_clip.resized(height=h_target)
            w_new, h_new = img_clip.size
            excess = w_new - w_target
            if excess <=0:
                 img_clip = img_clip.resized(width=w_target + 100)
                 w_new, h_new = img_clip.size
                 excess = w_new - w_target
            
            # Sub-movement calculations
            if base_dir == 'DER': # Movement to the Right (starts left-offset)
                p_start = -excess + (start_pct / 100.0) * excess
                p_end = -excess + (end_pct / 100.0) * excess
            else: # IZQ: Movement to the Left (starts at 0)
                p_start = -(start_pct / 100.0) * excess
                p_end = -(end_pct / 100.0) * excess
                
            img_clip = img_clip.with_position(lambda t: (int(p_start + (t / duration) * (p_end - p_start)), 'center'))
        
        else: # ABA, ARR
            # Vertical movement: scale width to match target width
            img_clip = img_clip.resized(width=w_target)
            w_new, h_new = img_clip.size
            excess = h_new - h_target
            if excess <= 0:
                img_clip = img_clip.resized(height=h_target + 100)
                w_new, h_new = img_clip.size
                excess = h_new - h_target
            
            if base_dir == 'ARR': # Movement to Top (starts bottom-offset)
                p_start = -excess + (start_pct / 100.0) * excess
                p_end = -excess + (end_pct / 100.0) * excess
            else: # ABA: Movement to Bottom (starts at 0)
                p_start = -(start_pct / 100.0) * excess
                p_end = -(end_pct / 100.0) * excess

            img_clip = img_clip.with_position(lambda t: ('center', int(p_start + (t / duration) * (p_end - p_start))))

    # DEFAULT LOGIC (If no manual direction provided)
    else:
        # CASE: Square Image
        if is_square:
            if is_short:
                img_clip = img_clip.resized(height=h_target)
                w_new, h_new = img_clip.size
                excess = w_new - w_target
                img_clip = img_clip.with_position(lambda t: (int(-excess + (t / duration) * excess), 'center'))
            else:
                img_clip = img_clip.resized(width=w_target)
                w_new, h_new = img_clip.size
                excess = h_new - h_target
                img_clip = img_clip.with_position(lambda t: ('center', int(-excess + (t / duration) * excess)))
        # CASE: Non-Square Image
        else:
            if h_img > w_img:
                img_clip = img_clip.resized(width=w_target)
                w_new, h_new = img_clip.size
                excess = h_new - h_target
                if excess <= 0:
                    img_clip = img_clip.resized(height=h_target + 100)
                    w_new, h_new = img_clip.size
                    excess = h_new - h_target
                img_clip = img_clip.with_position(lambda t: ('center', int(-excess + (t / duration) * excess)))
            else:
                img_clip = img_clip.resized(height=h_target)
                w_new, h_new = img_clip.size
                excess = w_new - w_target
                if excess <= 0:
                    img_clip = img_clip.resized(width=w_target + 100)
                    w_new, h_new = img_clip.size
                    excess = w_new - w_target
                img_clip = img_clip.with_position(lambda t: (int(-excess + (t / duration) * excess), 'center'))

    return CompositeVideoClip([img_clip], size=target_size).with_duration(duration)

def generate_video_process(project):
    from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, VideoFileClip, CompositeAudioClip, afx
    logger = ProjectLogger(project)
    logger.log(f"Starting generation for project: {project.title}")
    
    project.status = 'processing'
    project.save(update_fields=['status'])
    
    try:
        # Determine voice
        voice_to_use = project.voice_id
        if project.engine == 'edge':
            if not voice_to_use:
                voice_to_use = os.getenv("EDGE_VOICE", "es-DO-EmilioNeural")
        else:
            if not voice_to_use:
                voice_to_use = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")

        # Parse Script
        sections = []
        lines = project.script_text.strip().split('\n')
        
        for line in lines:
            if not line.strip():
                continue
            parts = line.strip().split('|')
            if len(parts) >= 3:
                image_name = parts[1].strip()
                # Check assets folder
                image_path = os.path.join(settings.MEDIA_ROOT, 'assets', image_name)
                
                # If source path is defined, prioritize it
                if project.source_path and os.path.exists(project.source_path):
                    local_path = os.path.join(project.source_path, image_name)
                    if os.path.exists(local_path):
                        image_path = local_path
                
                # Improved DIR and Image Parsing
                direction = None
                text = ""
                if len(parts) == 4:
                    direction = parts[2].strip()
                    text = parts[3].strip()
                else:
                    text = parts[2].strip()

                # Robust direction validation (supports DER:10:50)
                accepted_direction = None
                if direction:
                    base_dir = direction.split(':')[0].strip()
                    if base_dir in ['DER', 'IZQ', 'ABA', 'ARR']:
                        accepted_direction = direction

                # Robust image name cleaning (removes :coord if halluciated by IA)
                if ':' in image_name and not os.path.exists(image_path):
                    image_name = image_name.split(':')[0].strip()
                    # Recalculate path with cleaned name
                    image_path = os.path.join(settings.MEDIA_ROOT, 'assets', image_name)
                    if project.source_path and os.path.exists(project.source_path):
                        local_path = os.path.join(project.source_path, image_name)
                        if os.path.exists(local_path):
                            image_path = local_path

                sections.append({
                    "title": parts[0].strip(),
                    "image": image_path,
                    "text": text,
                    "direction": accepted_direction,
                    "original_image_name": image_name 
                })
        
        if not sections:
            raise Exception("No valid sections found in script")

        clips = []
        temp_audio_dir = os.path.join(settings.MEDIA_ROOT, 'temp_audio')
        os.makedirs(temp_audio_dir, exist_ok=True)
        
        # Get fallback images
        available_images = []
        
        # Add local path images to fallback if available
        if project.source_path and os.path.exists(project.source_path):
             available_images.extend([
                os.path.join(project.source_path, f) 
                for f in os.listdir(project.source_path) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4', '.mov', '.avi'))
            ])
            
        assets_dir = os.path.join(settings.MEDIA_ROOT, 'assets')
        if os.path.exists(assets_dir):
            available_images.extend([
                os.path.join(assets_dir, f) 
                for f in os.listdir(assets_dir) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4', '.mov', '.avi'))
            ])

        # Track voice intervals for ducking
        voice_intervals = []
        current_time = 0

        for i, section in enumerate(sections):
            logger.log(f"Processing section {i+1}: {section['title']}")
            
            # Audio
            audio_path = os.path.join(temp_audio_dir, f"{project.id}_audio_{i}.mp3")
            
            # Check for silence tag [PAUSA:X.X]
            import re
            pause_match = re.search(r'\[PAUSA:(\d+\.?\d*)\]', section['text'])
            is_pause = bool(pause_match)
            pause_duration = float(pause_match.group(1)) if is_pause else 0

            if is_pause:
                logger.log(f"Pause detected: {pause_duration}s")
                from moviepy import AudioClip
                # Create silent clip directly in memory (Stereo [0,0] for compatibility)
                audio_clip = AudioClip(lambda t: [0, 0], duration=pause_duration)
            elif project.engine == 'edge':
                # Run async in sync context safely
                try:
                    asyncio.run(generate_audio_edge(section['text'], audio_path, voice_to_use))
                except RuntimeError:
                    # Fallback if there is already a running loop in this thread
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(generate_audio_edge(section['text'], audio_path, voice_to_use))
                    loop.close()
            else:
                from elevenlabs.client import ElevenLabs
                from elevenlabs import save
                api_key = os.getenv("ELEVENLABS_API_KEY")
                if not api_key:
                    raise Exception("ElevenLabs API Key not found")
                client = ElevenLabs(api_key=api_key)
                audio_gen = client.text_to_speech.convert(
                    text=section['text'],
                    voice_id=voice_to_use,
                    model_id="eleven_multilingual_v2"
                )
                save(audio_gen, audio_path)
            
            # Load audio for non-pause sections
            if not is_pause:
                if not os.path.exists(audio_path):
                    logger.log("Audio not generated. Skipping.")
                    continue
                try:
                    audio_clip = AudioFileClip(audio_path)
                except Exception as e:
                    logger.log(f"Error loading audio: {e}")
                    continue

            real_voice_duration = audio_clip.duration
            duration = real_voice_duration + (0.5 if not is_pause else 0)
                
            # Store interval where voice is active for ducking (ONLY if it's not a manual pause)
            if not is_pause:
                voice_intervals.append((current_time, current_time + real_voice_duration))
            
            if not hasattr(audio_clip, 'rate') and hasattr(audio_clip, 'fps'):
                audio_clip.rate = audio_clip.fps
            
            # Update current_time for next section's start
            current_time += duration


            # Image/Video Asset
            asset_path = section['image']
            used_fallback = False
            
            if not os.path.exists(asset_path):
                logger.log(f"Asset not found: {section['original_image_name']}")
                if available_images:
                    asset_path = random.choice(available_images)
                    used_fallback = True
                    logger.log(f"Using fallback: {os.path.basename(asset_path)}")
                else:
                    logger.log("No fallback available. Skipping.")
                    continue
            
            # Create Clip
            try:
                # Set dynamic resolution
                if project.aspect_ratio == 'portrait':
                    TARGET_SIZE = (1080, 1920)
                else:
                    TARGET_SIZE = (1920, 1080)
                
                is_video = asset_path.lower().endswith(('.mp4', '.mov', '.avi', '.webm'))
                if is_video:
                    video_clip = VideoFileClip(asset_path).resized(TARGET_SIZE)
                    if video_clip.duration < duration:
                        loops = int(duration / video_clip.duration) + 1
                        val_clip = concatenate_videoclips([video_clip] * loops, method="chain")
                        video_clip = val_clip.subclipped(0, duration)
                    else:
                        video_clip = video_clip.subclipped(0, duration)
                    final_clip = video_clip.with_audio(audio_clip)
                else:
                    # Logic: Use manual direction if present. 
                    if section.get('direction'):
                        final_clip = apply_dynamic_pan(asset_path, TARGET_SIZE, duration, direction=section['direction']).with_audio(audio_clip)
                    else:
                        final_clip = ImageClip(asset_path).resized(TARGET_SIZE).with_duration(duration).with_audio(audio_clip)
                
                clips.append(final_clip)
            except Exception as e:
                logger.log(f"Error creating clip: {e}")
        
        if clips:
            logger.log("Concatenating clips with optimized method...")
            # Use method="chain" which is MUCH faster than "compose"
            final_video = concatenate_videoclips(clips, method="chain")
            
            # --- Background Music Integration with Ducking ---
            if project.background_music:
                try:
                    logger.log(f"Adding background music with Ducking: {project.background_music.name}")
                    bg_music_path = project.background_music.file.path
                    if os.path.exists(bg_music_path):
                        bg_audio = AudioFileClip(bg_music_path)
                        
                        # Loop music
                        loops = int(final_video.duration / bg_audio.duration) + 1
                        bg_audio_looped = bg_audio.with_effects([afx.AudioLoop(n_loops=loops)]).with_duration(final_video.duration)
                        
                        # DUCKING LOGIC
                        # music_volume is the peak level (no voice)
                        peak_vol = project.music_volume
                        duck_vol = peak_vol * 0.15 # Ducking to 15% of user preference
                        
                        fade_t = 0.2 # Duration of volume transition

                        def volume_ducking(t):
                            if isinstance(t, np.ndarray):
                                # Optimized vector processing for arrays
                                vol = np.full(t.shape, peak_vol)
                                for start, end in voice_intervals:
                                    # Ducking core
                                    vol[(t >= start) & (t <= end)] = duck_vol
                                    
                                    # Fade-out (Peak to Duck)
                                    mask_fade_out = (t >= (start - fade_t)) & (t < start)
                                    if np.any(mask_fade_out):
                                        # Simple linear interpolation: from peak to duck
                                        progress = (t[mask_fade_out] - (start - fade_t)) / fade_t
                                        vol[mask_fade_out] = peak_vol - (progress * (peak_vol - duck_vol))
                                    
                                    # Fade-in (Duck to Peak)
                                    mask_fade_in = (t > end) & (t <= (end + fade_t))
                                    if np.any(mask_fade_in):
                                        # Simple linear interpolation: from duck to peak
                                        progress = (t[mask_fade_in] - end) / fade_t
                                        vol[mask_fade_in] = duck_vol + (progress * (peak_vol - duck_vol))
                                return vol.reshape(-1, 1)
                            else:
                                # Standard scalar processing
                                for start, end in voice_intervals:
                                    if start <= t <= end:
                                        return duck_vol
                                    if (start - fade_t) <= t < start:
                                        progress = (t - (start - fade_t)) / fade_t
                                        return peak_vol - (progress * (peak_vol - duck_vol))
                                    if end < t <= (end + fade_t):
                                        progress = (t - end) / fade_t
                                        return duck_vol + (progress * (peak_vol - duck_vol))
                                return peak_vol

                        # Apply dynamic volume transformation
                        bg_audio_final = bg_audio_looped.transform(lambda get_f, t: get_f(t) * volume_ducking(t))
                        
                        # Mix tracks
                        final_audio = CompositeAudioClip([final_video.audio, bg_audio_final])
                        final_video = final_video.with_audio(final_audio)
                except Exception as music_err:
                    logger.log(f"Warning: Failed to add background music: {music_err}")
            # ------------------------------------
            
            safe_title = slugify(project.title) or f"video_{project.id}"
            output_filename = f"{safe_title}.mp4"
            output_rel_path = f"videos/{output_filename}"
            output_full_path = os.path.join(settings.MEDIA_ROOT, 'videos', output_filename)
            os.makedirs(os.path.dirname(output_full_path), exist_ok=True)
            
            logger.log("Writing final video file with multi-threading...")
            import multiprocessing
            n_threads = multiprocessing.cpu_count()
            
            final_video.write_videofile(
                output_full_path, 
                fps=24, 
                logger=None, 
                threads=n_threads,
                preset="superfast",
                codec="libx264",
                audio_codec="aac"
            )
            
            # Thumbnail
            try:
                thumb_filename = f"{safe_title}_thumb.png"
                thumb_rel_path = f"thumbnails/{thumb_filename}"
                thumb_full_path = os.path.join(settings.MEDIA_ROOT, 'thumbnails', thumb_filename)
                os.makedirs(os.path.dirname(thumb_full_path), exist_ok=True)
                final_video.save_frame(thumb_full_path, t=1.0)
                project.thumbnail.name = thumb_rel_path
            except:
                pass # processing err
            
            project.output_video.name = output_rel_path
            project.status = 'completed'
            logger.log("Video generation successful!")
        else:
            project.status = 'failed'
            logger.log("No clips were generated.")

    except Exception as e:
        logger.log(f"Critical Error: {str(e)}")
        import traceback
        logger.log(traceback.format_exc())
        project.status = 'failed'
    
    # Selective save to protect Title from accidental mutations
    project.save(update_fields=['status', 'output_video', 'thumbnail', 'log_output'])
