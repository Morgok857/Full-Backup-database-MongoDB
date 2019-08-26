## Descripcion

Script para realizar backups completos de una bases de datos en MongoDB. 

Se desarrollo y valido el script sobre Ubuntu 18.04 y Centos 7. No se requiere contar con permisos de administración para ejecutar este comando, pero si los permisos adecuados sobre los directorios temporales, de almacenamiento y dentro de la base de datos.

El script esta pensado para conectarse a una base de datos con autenticacion basica (Usuario y contraseña).

Version 0.01

## Requerimientos:

- Python 3 o superior
- Mongodump

## Instalacion

Clonar el repositorio con el comando:

```
$ git clone https://github.com/Morgok857/Full-Backup-database-MongoDB.git
```

Ingresamos al directorio con:
```
$ cd Full-Backup-database-MongoDB
```

Creamos el archivo de configuracion:

```
$ cp config.cfg.template config.cfg
```

Editamos el archivo de configuacion que creamos y modificamos los accesos a la base de datos.

Finalmente ejecutamos el script:

```
$ python3 main.py
```

Si queremos que se ejecute el script todos los días, podemos incluir en el crontab la ejecucion del script.

__Ej para cronear el script__

Si tenemos el script en el directorio "/var/lib/backup-mongodb" y queremos ejecutarlo todos los dias a las 01 hs, deberiamos incluir en el crontab la siguiente linea.

```
0 1 * * * /usr/bin/python /var/lib/backup-mongodb/main.py > /var/lib/backup-mongodb/backup.log 2>&1
```

## Archivo de configuracion
 El archivo "config.cfg" cuenta con 3 secciones:

- GENERAL <-- Configuracion relativa al funcionamiento y almacenamiento de los backups
- DB <-- Datos de conexion contra la base de datos
- LOG <-- Configuracion relacionada al archivo de logs

Es importante recordar que los valores ingresados dentro de la configuracion no deben llevar comillas o comillas dobles.

_Ej:_
```
Log_level=INFO
```

__GENERAL__

Configuracion relativa al funcionamiento y almacenamiento de los backups.

- Temp_dir=tmp  <-- Directorio donde se genera el backup antes de comprimirlo 
- Backup_dir=backup-mongodb <-- Directorio donde se almacenan los backups
- Default_bkp_name=mongodb <-- Prefijo que utiliza para generar el nombre del backup

__DB__ 

Datos de conexion contra la base de datos.
- DB_Host <-- IP o FQDN donde se encuentra la base de datos
- DB_Port <-- Puerto donde escucha la base de datos
- DB_Name <-- Nombre de la base de datos a resguardar
- DB_User <-- Usuario con el que debe conectarse a la base de datos para hacer el backup 
- DB_Password <-- Contraseña con el que debe conectarse a la base de datos para hacer el backup
- DB_AuthenticationDatabase <-- Base de datos contra la que debe autenticarse

__LOG__

Configuracion relacionada al archivo de logs

- Log_name <-- La ruta donde guardara el archivo de logs 
- Log_level <-- Nivel de detalle en los logs. 

Se pueden configurar los siguientes niveles de logs:
- INFO <-- Solo registra los pasos que va realizando
- DEBUG <-- Se registran los pasos que va realizando, las variables que toma el script y los comandos que va a ejecutar

__TEST MODE (Experimental)__ 

Adicionalmente, se puede habilitar un nivel extra de pruebas. El cual en lugar de ejecutar los comandos solo los imprime por pantalla.

Para habilitarlo se debe crear un archivo llamado "test.mode".

EJ:

Si tenemos clonado el repositorio en "/var/lib/backup-mongodb" debemos:

```
$ cd /var/lib/backup-mongodb

$ touch /var/lib/backup-mongodb/test.mode
```

## Rotación de archivos

Para realizar la rotación de backups podemos ayudarnos de la herramienta "find". A fin de expresar mejor la explicación, daremos por entendidoque los backups los estamos guardando en el directorio "/var/lib/mongo/backups/backup-mongodb".

El comando "find" nos permite buscar archivos por fecha de modificación. Asi que con el siguiente comando obtendremos los backups creados hace mas de 7 días: 

```
find /var/lib/mongo/backups/backup-mongodb -type f -ctime +7
```

Ahora si le agregamos el parámetro "-delete" el comando "find" procederá a eliminar los archivos  que encuentre

```
find /var/lib/mongo/backups/backup-mongodb -type f -ctime +7 -delete
```


Para rotar los backups debemos agregar una segunda linea en el crontab para que se borren los backups con fecha mayor a 7 días:

```
0 2 * * * /usr/bin/find /var/lib/mongo/backups/backup-mongodb -type f -ctime +7 -delete
```

## TODO
* Agregar rotación de backup
* Agregar soporte para multiples bases de datos dentro del mismo motor
* Mejorar el control de errores
* Adicionar comentarios
* Adicionar validaciones para que  si no existe el archivo de configuraciones o alguna configuración se tomen configuraciones por defecto
* Estandarizar el uso del sistema de logs
* Re-secuenciar y documentar los ERRORLEVEL que regresa
* Validar el "Test MODE"

