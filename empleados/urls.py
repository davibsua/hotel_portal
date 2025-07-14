from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Autenticación
    path('', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('panel/', views.panel_empleado, name='panel'),

    # Tablón de anuncios
    path('departamento/<int:departamento_id>/tablon/', views.tablon_departamento, name='tablon_departamento'),
    path('departamento/<int:departamento_id>/crear_post/', views.crear_post, name='crear_post'),

    # Chat privado
    path('hilos-chat/', views.lista_hilos_chat, name='hilos_chat'),

    path('chat/<int:hilo_id>/', views.hilo_chat, name='hilo_chat'),
    path('chat/iniciar/<int:usuario_id>/', views.iniciar_chat_privado, name='iniciar_chat'),
    path('borrar_post/<int:post_id>/', views.borrar_post, name='borrar_post'),
    path('subir-pdf/', views.subir_pdf, name='subir_pdf'),
    path('lista_pdfs/', views.lista_pdfs, name='lista_pdfs'),

]
