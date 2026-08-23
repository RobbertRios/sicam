### Dependencias ###

- pip install django
- pip install djangorestframework
- pip install django-cors-headers
- pip install psycopg2

### Iniciar Django ###

### Si no tienes creado la carpeta de backend  (desde la carpetra raiz, para crear la carpeta backend con todo) ####
django-admin startproject backend
cd backend
python manage.py startapp api

### Si ya creaste la carpeta de backend (dentro de esa carpeta correr el comando) ####
django-admin startproject config .

### correr Django ###
python manage.py runserver

### Si hay un "error" que tenga que ver con la base de datos ###
CONTROL + C (para detener la ejecucion)
python manage.py migrate
python manage.py runserver

### despues de verificar, ahora crearemos el API ###
python manage.py startapp api


/// BASE DE DATOS /////

### Intalar Dependencias ###
pip install psycopg2-binary

/// Para las Imagenes usamos ImageField /////
## hay que instalar una Dependencia ##
pip install Pillow

// OTRAS Dependencias para el Framework en caso de no tenerlas //
pip install djangorestframework django-cors-headers





///  PARTE DE BASE DE DATOS (postgres) ////

se crearon algunos indices, pensando a futuro, especificamente con la busqueda de los arhcivos

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'analisis_archivos';

indice GIN sobre contenido_json (CRITICO)

CREATE INDEX idx_analisis_archivos_contenido_json
ON analisis_archivos
USING GIN (contenido_json);


Índice en Foreign Key (id_analisis_fk_id)

CREATE INDEX idx_analisis_archivos_analisis_fk
ON analisis_archivos (id_analisis_fk_id);


indice compuesto para version activa (MUY RECOMENDADO)

CREATE INDEX idx_analisis_archivos_activo
ON analisis_archivos (id_analisis_fk_id, activo)
WHERE activo = true;


indice por version (Opcional, pero si)

CREATE INDEX idx_analisis_archivos_version
ON analisis_archivos (id_analisis_fk_id, version);


verificar creacion

SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'analisis_archivos';

mas dependencias para el LOG-IN

pip install djangorestframework-simplejwt