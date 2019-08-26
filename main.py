#/usr/bin/python3

## Se importan las librerias base
import os
from settings import *
#

## Se valida que el directorio temporal y el de backups existan. Si no estan se crean
logger.inf("Validando los directorios de trabajo ...")
create_folder_tmp(temp_dir,logger)
create_folder_tmp(bkp_dir,logger)
#

## Antesde iniciar las tareas se limpia el directorio temporal a fin de evitar rescuardar 
# datos invalidos de ejecuciones anteriores.
logger.inf("Limpiando directorio temporal")
clean_folder(temp_dir,logger)
#

## Se gerena el Dump de la base de datos
logger.inf("Generando dump ...")
db_dump(DB_CONFIG,temp_dir,logger)
#

## Se comprime le Dump generado
logger.inf("Generando el Tar con los datos recolectados")
archive_backup(temp_dir,bkp_dir,default_bkp_name,logger)
#

## Se registra la hora de finalización del scrip en el log.
logger.inf("Stop scritp ..")
