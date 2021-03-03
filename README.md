# encuestas-app


Aplicacion WEB para realizar encuestas con preguntas y respuestas.

# Instrucciones:

- Descargar o clonar proyecto del repositorio

- Crear entorno virtual en la carpeta: 
    - python3 -m venv venv
    
- Activar entorno virtual: 
    - .\venv\Scripts\activate (windows)
    - source ./venv/bin/activate (ubuntu)

- Instalar los requerimientos para la app:
    - pip3 install -r requirements.txt
    
- Crear base de datos: 
    - python manage.py makemigrations
    - python manage.py migrate

- Crear super usuario:
    - python manage.py createsuperuser 
  
- Arrancar el servidor web:
    - python manage.py runserver
    
- Acceder a APP-Encuestas en el navegador por medio de http://localhost:8000


# La APP:

- Sin estar logueado se pueden visualizar las encuestas ya creadas por usuarios y también votar.
- Al loguarse con el usuario creado como superuser o bien al registrarse y crear uno nuevo, se puede:
    - crear encuestas
    - darles un plazo de vencimiento para que se pueda votar
    - modificar las encuestas
    - crear etiquetas o rubros de encuestas
    - visualizar los totales de las respuestas de cada encuesta
    - ver reportes de las encuestas por usuario y por etiquetas (rubros)
