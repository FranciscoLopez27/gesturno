# GesTurno

Sistema web para la gestión de turnos, días libres, vacaciones y permisos de equipos de trabajo.

Proyecto del ramo **Taller de Desarrollo Web y Móvil (APTC106)**. Construido a partir del ejemplo de CRUD entregado en clases, adaptado a la propuesta GesTurno.

## Funcionalidades del mínimo viable

**Trabajadores** (desde el sitio):
- Iniciar y cerrar sesión.
- Crear, ver, editar y cancelar sus solicitudes (vacaciones, permisos médicos, matrimonio, nacimiento y días administrativos).
- Ver solo sus propias solicitudes; no pueden ver ni modificar las de otros.
- Editar o cancelar solicitudes solo mientras están pendientes.
- Consultar sus próximos turnos.

**Jefatura o administración** (desde el panel de administración):
- Configurar los tipos de solicitud y sus reglas.
- Aprobar o rechazar solicitudes.
- Asignar turnos.
- Registrar el saldo de vacaciones de cada trabajador.

**Reglas de negocio:**
- La fecha de término no puede ser anterior a la de inicio.
- No se pueden crear solicitudes con fecha de inicio en el pasado.
- Cada tipo puede tener un máximo de días hábiles por solicitud.
- Algunos tipos exigen adjuntar un documento de respaldo.
- Las vacaciones no pueden superar el saldo disponible, y se descuentan del saldo al ser aprobadas.

## Requisitos

- Python 3.12 o superior
- Git

## Instalación

```bash
git clone https://github.com/FranciscoLopez27/gesturno.git
cd gesturno
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

En Windows, si `venv\Scripts\activate` muestra un error de permisos, ejecutar una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Ejecución

```bash
venv\Scripts\activate
python manage.py runserver
```

- Sitio: http://127.0.0.1:8000/
- Panel de administración: http://127.0.0.1:8000/admin/

## Datos iniciales

La base de datos no se incluye en el repositorio. Después de instalar, desde el panel de administración:

1. Crear los **tipos de solicitud** (por ejemplo: Vacaciones, Médico, Matrimonio, Nacimiento y Día administrativo) con sus reglas.
2. Crear un **perfil** para cada usuario, con sus días de vacaciones disponibles.
3. Crear **turnos** para los trabajadores.

## Estructura del proyecto

```
gesturno/
├── crud/                    Configuración del proyecto (settings y URLs principales)
├── apps/solicitudes/        Aplicación principal
│   ├── models.py            Modelos: TipoSolicitud, Solicitud, Turno y Perfil
│   ├── forms.py             Formularios de solicitud y de inicio de sesión
│   ├── views.py             Vistas (controladores)
│   ├── urls.py              Rutas de la aplicación
│   ├── admin.py             Configuración del panel de administración
│   └── templates/           Plantillas HTML
├── manage.py
└── requirements.txt
```

## Limitaciones conocidas

- Si una solicitud de vacaciones aprobada se cambia después a rechazada, los días no se devuelven al saldo.
- Los días hábiles se cuentan de lunes a viernes, sin considerar feriados.
- El saldo de vacaciones se ingresa manualmente; no se calcula a partir de la fecha de ingreso.