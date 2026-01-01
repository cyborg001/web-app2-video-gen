from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Asset, VideoProject, YouTubeToken, Music
from .utils import generate_video_process
from .youtube_utils import get_flow, get_youtube_client, upload_video
import threading
import os
import logging

logger = logging.getLogger(__name__)

def browse_script(request):
    try:
        import tkinter as tk
        from tkinter import filedialog
        # Create a hidden root window
        root = tk.Tk()
        root.withdraw() # Hide it
        root.attributes('-topmost', True) # Bring to front
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de guion",
            filetypes=[("Text/Markdown", "*.txt *.md"), ("All files", "*.*")]
        )
        
        root.destroy()
        
        if file_path:
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            
            # Read content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            return JsonResponse({
                'status': 'success',
                'path': directory,
                'filename': filename,
                'content': content
            })
        return JsonResponse({'status': 'cancel'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def home(request):
    search_query = request.GET.get('q', '')
    projects_list = VideoProject.objects.all().order_by('-created_at')

    if search_query:
        projects_list = projects_list.filter(title__icontains=search_query)

    paginator = Paginator(projects_list, 9)  # 9 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'generator/home.html', {
        'page_obj': page_obj, 
        'search_query': search_query
    })

def delete_project(request, project_id):
    project = get_object_or_404(VideoProject, id=project_id)
    if request.method == 'POST':
        project.delete()
    return redirect('generator:home')

def create_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        script = request.POST.get('script')
        engine = request.POST.get('engine')
        voice_id = request.POST.get('voice_id', '').strip()
        aspect_ratio = request.POST.get('aspect_ratio', 'landscape')
        source_path = request.POST.get('source_path', '').strip()
        script_file = request.POST.get('script_file', '').strip()
        music_id = request.POST.get('background_music')
        music_volume = request.POST.get('music_volume', '0.15')
        
        background_music = None
        if music_id:
            background_music = Music.objects.get(id=music_id)
        
        # If script is empty but source path and script file are provided, try to load it
        if not script and source_path and script_file:
            import os
            try:
                full_path = os.path.join(source_path, script_file)
                if os.path.exists(full_path):
                    with open(full_path, 'r', encoding='utf-8') as f:
                        script = f.read()
            except Exception as e:
                # If loading fails, we proceed with empty/default script, logic will fail later or user sees empty
                pass
 
        visual_prompts = request.POST.get('visual_prompts', '')

        # dynamic_pan removed as it's now controlled by the script (DIR)

        project = VideoProject.objects.create(
            title=title,
            script_text=script,
            engine=engine,
            aspect_ratio=aspect_ratio,
            voice_id=voice_id,
            source_path=source_path,
            background_music=background_music,
            music_volume=float(music_volume),
            visual_prompts=visual_prompts
        )
        
        # Start generation in background
        thread = threading.Thread(target=generate_video_process, args=(project,))
        thread.daemon = True
        thread.start()
        
        return redirect('generator:project_detail', project_id=project.id)
        
    # Default script template with advanced features examples
    default_script = """INTRO | black_hole.png | DER | ¡Bienvenidos! Hoy exploraremos los secretos del cosmos.
TRANSICION | nebulosa.jpg | IZQ | Mira cómo se mueven las estrellas con el efecto Ken Burns.
PAUSA | espacio.jpg | | [PAUSA:3.0]
CIERRE | galaxia.png | ARR | Suscríbete para más ciencia. El volumen de la música subió en la pausa anterior."""

    # If news_id is provided, use AI to generate script
    news_id = request.GET.get('news_id')
    ai_generated_script = ""
    ai_visual_prompts = ""
    initial_title = ""
    
    if news_id:
        from researcher.models import NewsItem
        from .utils import generate_script_ai
        news_item = get_object_or_404(NewsItem, id=news_id)
        initial_title = news_item.title[:200]
        
        script, prompts, music_suggestion = generate_script_ai(news_item)
        if script:
            ai_generated_script = script
            if isinstance(prompts, list):
                formatted_prompts = []
                for p in prompts:
                    if isinstance(p, dict) and 'file' in p and 'prompt' in p:
                        formatted_prompts.append(f"ARCHIVO: {p['file']}\nPROMPT: {p['prompt']}\n")
                    else:
                        formatted_prompts.append(f"- {p}")
                ai_visual_prompts = "\n".join(formatted_prompts)
            else:
                ai_visual_prompts = str(prompts)
            
            # Format music suggestion
            if music_suggestion:
                ai_visual_prompts = f"🎵 SUGERENCIA MUSICAL:\n{music_suggestion}\n\n" + ai_visual_prompts

            messages.success(request, "¡Guion generado con éxito por la IA!")
        else:
            messages.warning(request, f"No se pudo generar el guion con IA: {prompts}. Usando plantilla por defecto.")
            ai_generated_script = default_script

    music_list = Music.objects.all().order_by('name')
    return render(request, 'generator/create.html', {
        'default_script': ai_generated_script or default_script,
        'ai_visual_prompts': ai_visual_prompts,
        'initial_title': initial_title,
        'music_list': music_list
    })

def project_detail(request, project_id):
    project = get_object_or_404(VideoProject, id=project_id)
    return render(request, 'generator/detail.html', {'project': project})

def delete_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        asset_name = asset.name
        file_path = asset.file.path if asset.file else None
        asset.delete()
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        messages.success(request, f"Asset '{asset_name}' eliminado.")
    return redirect('generator:asset_list')

def asset_list(request):
    # Reconcile physical folder with database
    media_assets_path = os.path.join(settings.MEDIA_ROOT, 'assets')
    if not os.path.exists(media_assets_path):
        os.makedirs(media_assets_path)
    
    # Get all files in the assets folder
    try:
        files_in_folder = os.listdir(media_assets_path)
        for filename in files_in_folder:
            asset_rel_path = f'assets/{filename}'
            if not Asset.objects.filter(file=asset_rel_path).exists():
                Asset.objects.create(file=asset_rel_path, name=filename)
    except Exception as e:
        pass

    assets = Asset.objects.all().order_by('-uploaded_at')
    return render(request, 'generator/assets.html', {'assets': assets})

def youtube_authorize(request):
    if settings.DEBUG:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    flow = get_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def youtube_callback(request):
    if settings.DEBUG:
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    state = request.session.get('oauth_state')
    flow = get_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    
    credentials = flow.credentials
    token_data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    
    # Save or update token
    YouTubeToken.objects.all().delete() # We only keep one for now
    YouTubeToken.objects.create(token=token_data)
    
    return redirect('generator:home')

def upload_to_youtube_view(request, project_id):
    project = get_object_or_404(VideoProject, id=project_id)
    youtube = get_youtube_client()
    
    if not youtube:
        return redirect('generator:youtube_authorize')
    
    if not project.output_video:
        return JsonResponse({'status': 'error', 'message': 'El video aún no se ha generado.'})

    try:
        video_path = project.output_video.path
        title = project.title
        description = f"Video generado automáticamente por notiaci.\n\nGuion:\n{project.script_text}"
        
        upload_video(youtube, video_path, title, description)
        
        project.log_output += f"\n[YouTube] Video subido con éxito: {title}"
        project.save()
        
        return redirect('generator:project_detail', project_id=project.id)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def music_list(request):
    # We maintain the catalog in DB. 
    # Removed auto-sync to avoid re-adding files that the user intentionally deleted but are still locked by the OS.
    music_items = Music.objects.all().order_by('-uploaded_at')
    return render(request, 'generator/music_list.html', {'music_items': music_items})

def upload_music(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for f in files:
            Music.objects.create(file=f)
        return redirect('generator:music_list')
    return render(request, 'generator/upload_music.html')

def delete_music(request, music_id):
    music = get_object_or_404(Music, id=music_id)
    if request.method == 'POST':
        music_name = music.name
        file_path = music.file.path if music.file else None
        
        # Delete from DB first so it disappears from UI immediately
        music.delete()
        
        # Try to delete from disk
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                messages.success(request, f"Música '{music_name}' eliminada correctamente.")
            except PermissionError:
                messages.warning(request, f"La pista '{music_name}' se quitó de la biblioteca, pero el archivo está bloqueado por el sistema. Se borrará automáticamente más tarde.")
            except Exception as e:
                messages.warning(request, f"Quitado de la biblioteca. Nota: No se pudo borrar el archivo: {e}")
        else:
            messages.success(request, f"Música '{music_name}' eliminada de la biblioteca.")
            
    return redirect('generator:music_list')

def upload_asset(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        for f in files:
            Asset.objects.create(file=f)
        return redirect('generator:asset_list')
    return render(request, 'generator/upload_asset.html')
