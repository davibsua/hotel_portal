from django.contrib.auth.models import AbstractUser
from django.db import models


# ───────────────────────────────
# 1.  Estructura organizativa
# ───────────────────────────────
class Departamento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    jefe = models.OneToOneField(
        "Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dirige",
        help_text="Usuario con rol 'jefe' asignado como responsable",
    )

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    ROL_CHOICES = (
        ("empleado", "Empleado"),
        ("jefe", "Jefe de departamento"),
    )
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="miembros",
    )

    def __str__(self):
        return self.username


# ───────────────────────────────
# 2.  Mensajería clásica 1 → 1
# ───────────────────────────────
class Mensaje(models.Model):
    remitente = models.ForeignKey(
        Usuario, related_name="enviados", on_delete=models.CASCADE
    )
    destinatario = models.ForeignKey(
        Usuario, related_name="recibidos", on_delete=models.CASCADE
    )
    asunto = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.asunto} → {self.destinatario}"


# ───────────────────────────────
# 3.  Horarios
# ───────────────────────────────
class Horario(models.Model):
    empleado = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    dia = models.CharField(max_length=10)
    entrada = models.TimeField()
    salida = models.TimeField()

    def __str__(self):
        return f"{self.empleado} {self.dia}: {self.entrada}-{self.salida}"


# ───────────────────────────────
# 4.  Tablón de anuncios
# ───────────────────────────────
class PostTablon(models.Model):
    departamento = models.ForeignKey(
        Departamento, related_name="posts", on_delete=models.CASCADE
    )
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=120)
    cuerpo = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return f"[{self.departamento}] {self.titulo}"


# ───────────────────────────────
# 5.  Chat privado
# ───────────────────────────────
class HiloChat(models.Model):
    participantes = models.ManyToManyField(Usuario, related_name="hilos")
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        usuarios = ", ".join(self.participantes.values_list("username", flat=True))
        return f"Hilo #{self.id} ({usuarios})"

    @property
    def ultimo_mensaje(self):
        return self.mensajes.order_by("-enviado").first()


class MensajeChat(models.Model):
    hilo = models.ForeignKey(
        HiloChat, related_name="mensajes", on_delete=models.CASCADE
    )
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    enviado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["enviado"]

    def __str__(self):
        return f"{self.remitente}: {self.texto[:30]}..."


