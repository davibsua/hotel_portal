from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import DocumentoPDFForm
from .models import DocumentoPDF

# formularios
from .forms import RegistroUsuarioForm, PostTablonForm, MensajeChatForm
# modelos propios
from .models import (
    Horario,
    Mensaje,
    Departamento,
    HiloChat,
    Usuario,
    PostTablon
)


@login_required
def borrar_post(request, post_id):
    post = get_object_or_404(PostTablon, id=post_id) #crea variable post/publicacion en la vista  y la obtiene con un post
    if request.user == post.departamento.jefe: #mira si el usuario es exactamente el jefe del departamento
        departamento_id = post.departamento.id #crea la variable departamento id(1-4) y lo coge de la api con el post
        post.delete()  #borra la publicacion
        return redirect('tablon_departamento', departamento_id=departamento_id) #si el usuario es el jefe te devuelve al tablon sin el mensaje

    return redirect('tablon_departamento', departamento_id=post.departamento.id) #el usuario no es el jefe y no borra el mensaje

# ────────────────────────────────────
# 1. Tablón de anuncios por departamento
# ────────────────────────────────────
@login_required
def tablon_departamento(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id) #crea la variable departamento y obtiene que departamento es de la api


    # El usuario debe pertenecer al mismo departamento si no lo es no da acceso
    if request.user.departamento != departamento:
        return HttpResponseForbidden("No tienes permiso para ver este tablón.")

    posts = departamento.posts.all()  #
    user = request.user
    return render(
        request,
        "empleados/foro/tablon.html",
        {"departamento": departamento, "posts": posts, "user": user},

    )


@login_required
def crear_post(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)

    # Solo el jefe puede publicar
    if request.user != departamento.jefe:
        return HttpResponseForbidden("Solo el jefe puede crear posts.")

    form = PostTablonForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.departamento = departamento
        post.autor = request.user
        post.save()
        return redirect("tablon_departamento", departamento_id=departamento.id)

    return render(
        request,
        "empleados/foro/crear_post.html",
        {"form": form, "departamento": departamento},
    )


# ────────────────────────────────────
# 2. Chat privado
# ────────────────────────────────────
@login_required
def lista_hilos_chat(request):
    hilos = HiloChat.objects.filter(participantes=request.user)
    return render(request, "empleados/foro/hilos_chat.html", {"hilos": hilos})


@login_required
def hilo_chat(request, hilo_id):
    hilo = get_object_or_404(HiloChat, id=hilo_id)

    if request.user not in hilo.participantes.all():
        return HttpResponseForbidden("No tienes acceso a este chat.")

    mensajes = hilo.mensajes.all()  # Meta.ordering=['enviado']
    form = MensajeChatForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        mensaje = form.save(commit=False)
        mensaje.hilo = hilo
        mensaje.remitente = request.user
        mensaje.save()
        return redirect("hilo_chat", hilo_id=hilo.id)

    return render(
        request,
        "empleados/foro/hilo_chat.html",
        {"hilo": hilo, "mensajes": mensajes, "form": form},
    )


@login_required
def iniciar_chat_privado(request, usuario_id):
    otro_usuario = get_object_or_404(Usuario, id=usuario_id)

    # Busca si ya existe un hilo con EXACTAMENTE esos dos usuarios
    hilo = (
        HiloChat.objects.filter(participantes=request.user)
        .filter(participantes=otro_usuario)
        .first()
    )
    if not hilo:
        hilo = HiloChat.objects.create()
        hilo.participantes.add(request.user, otro_usuario)

    return redirect("hilo_chat", hilo_id=hilo.id)


# ────────────────────────────────────
# 3. Autenticación y panel actual
# ────────────────────────────────────
def login_view(request):
    #
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("panel")
    return render(request, "empleados/login.html", {"form": form})


@login_required
def panel_empleado(request):
    usuario = request.user
    horarios = Horario.objects.filter(empleado=usuario)
    mensajes = Mensaje.objects.filter(destinatario=usuario)
    return render(
        request,
        "empleados/panel.html",
        {"usuario": request.user, "horarios": horarios, "mensajes": mensajes},
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def registro_view(request):
    form = RegistroUsuarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()  # Esto guarda todos los campos directamente
        return redirect("login")
    return render(request, "empleados/registro.html", {"form": form})


@login_required
def subir_pdf(request):
    if request.method == "POST":
        form = DocumentoPDFForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.save()
            return redirect("lista_pdfs")
    else:
        form = DocumentoPDFForm()

    return render(request, 'empleados/subir_pdf.html', {'form': form})

@login_required
def lista_pdfs(request):
    documentos = DocumentoPDF.objects.all()
    return render(request, 'empleados/lista_pdfs.html',{'documentos': documentos})