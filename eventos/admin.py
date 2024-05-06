from django.contrib import admin
from django.utils import timezone
from django.db.models import Count
from .models import Evento, Usuario, RegistroEvento
 
class EventosEsteMesFilter(admin.SimpleListFilter):
    title = 'Eventos Este Mes'
    parameter_name = 'eventos_del_mes'

    def lookups(self, request, model_admin):
        return (
            ('este_mes', 'Este mes'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'este_mes':
            current_month = timezone.now().month
            current_year = timezone.now().year
            return queryset.filter(fecha_inicio__month=current_month, fecha_inicio__year=current_year)
class RegistroEventoInline(admin.TabularInline):
    model = RegistroEvento
    extra = 0


class RegistroEventoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha_registro') 
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'ubicacion', 'capacidad_maxima', 'usuarios_registrados')
    inlines = [RegistroEventoInline]
    list_filter = [EventosEsteMesFilter]

    def usuarios_registrados(self, obj):
        return obj.registroevento_set.count()

    usuarios_registrados.short_description = 'Usuarios Registrados'
    
    
    
class UsuarioMasActivoFilter(admin.SimpleListFilter):
    title = 'Usuario Más Activo'
    parameter_name = 'usuario_mas_activo'

    def lookups(self, request, model_admin):
        return (
            ('todos', 'Los usuarios más activos'),
            ('uno', 'El usuario más activo'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'todos':
            return queryset.annotate(num_eventos=Count('registroevento')).order_by('-num_eventos')
        elif self.value() == 'uno':
            usuarios_mas_activos = queryset.annotate(num_eventos=Count('registroevento')).order_by('-num_eventos')
            if usuarios_mas_activos.exists():
                # Devolver solo el usuario más activo
                return queryset.filter(pk=usuarios_mas_activos.first().pk)
            else:
                return queryset.none()


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo_electronico', 'eventos_participados')

    def eventos_participados(self, obj):
        return obj.eventos.count()

    eventos_participados.short_description = 'Eventos Participados'
    list_filter = [UsuarioMasActivoFilter]



# Registra los modelos junto con sus clases de administración personalizadas
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(RegistroEvento, RegistroEventoAdmin)
