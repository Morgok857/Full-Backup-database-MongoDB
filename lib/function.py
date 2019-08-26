#/usr/bin/python
## Se importan las dependencias
import os
import logging
import shlex
from subprocess import Popen, PIPE
#

## Se obtiene el path base del script y se almacena para posteriores referencias
diripath = os.path.dirname(os.path.realpath(__file__))
#

## Se valida si el archivo "test.mode" existe, si existe regresa "True". Abstacion para la validacion del "TEST MODE"
def test_mode():
	test_f = diripath + "/../test.mode"
	if os.path.exists(test_f):
		return True
	return False
#

## Funcion para ejecutar comandos sobre la Shell del sistema. 
# Recibe como parametros:
# - command <-- String con el comando a ejecutar
# - OBLog <-- Objeto del tipo "logging" para acceder al sistema de logs
##
# Si falla al ejecutar el comando, realiza las siguientes acciones:
# - Registra el error en los logs. Si esta en modo DEBUG registra el error
# - Finaliza el script.
##
# Si pude ejecutar el commando en el SHELL regresa el ERRROLEVEL de la ejecucion. 
# Si el comando se ejecuta sobre la SHELL pero este tiene algun problema o no existe igual se regresa el ERRROLEVEL
def run_command(command,OBLog):
		# Si el log esta habilitado a nivel DEBUG registra el comando antes de ejecutarlo
        OBLog.db("Run command: " + command)
        try:
                process = Popen(shlex.split(command), stdout=PIPE)
        except OSError as err:
                OBLog.inf("Error al ejecutar el comando")
                OBLog.db("Error: " + str(err))
                print("Error. Saliendo ...")
                exit(4)
        exit_code = process.wait()
        return exit_code
#

## Se valida que el directorio temporal exista, si no existe lo crea.
# Recibe como parametros:
# - folder <-- String con el PATH del directorio temporal
# - OBLog <-- Objeto del tipo "logging" para acceder al sistema de logs
##
# Regresa True si pudo crear el directorio o si ya existe
def create_folder_tmp(folder,OBLog):
	logger = OBLog
	if not os.path.exists(folder):
		logger.db("Directorio no existe y se va a crear " + folder)
		try:
			os.makedirs(folder)	
			logger.inf("Se creo el directorio " + folder)
			return True
		except OSError as e:
			logger.inf("Error al crear el directorio " + folder + " " + str(e))
			print("Error al crear el directorio. Saliendo ...")
			exit(4)
	return True
#

## remueve el contenido del directorio que se le indique
# Recibe como parametros:
# - folder <-- String con el PATH del directorio a eliminar
# - OBLog <-- Objeto del tipo "logging" para acceder al sistema de logs
def clean_folder(folder,OBLog):	
		logger = OBLog
		command = "rm -rf " + folder + "/*"

		if test_mode() == True:
			print(command)
			return True
		else:
			command = "rm -rf " + folder + "/*"
			logger.db(command)
			## The command "rm" not running correctly in subprocess module
			os.system(command)
			#
			logger.db("Listar dir: ")
#


## Genera el DUMP de la base de datos
# Recibe como parametros:
# - DB_CONFIG <-- Objeto con los datos de conexion a la base de datos
# - temp_dir <-- String con el PATH del directorio temporal
# - OBLog <-- Objeto del tipo "logging" para acceder al sistema de logs
def db_dump(DB_CONFIG,temp_dir,OBLog):
	logger = OBLog
	# Crea el string de conexion contra la base de datos
	command = "mongodump --host " + DB_CONFIG['db_host'] + " --port " + DB_CONFIG['db_port'] + " --db " + DB_CONFIG['db_name'] + " --gzip --out " + temp_dir + "/ -u \"" + DB_CONFIG['db_user'] + "\" -p \"" + DB_CONFIG['db_password'] + "\" --authenticationDatabase \"" + DB_CONFIG['db_authenticationdatabase'] + "\""
	logger.db(command)

	# Si existe esta en "TEST MODE " solo registra el comando
	if test_mode() == True:
        	print(command)
			logger.inf("Dump Command: " + command)
	else:
		## The command "mongodump" not running correctly in subprocess module. Used os.popen
		process = os.popen(command)
		logger.db("DB Status: " + process.read())	
#


## Comprime el contenido del directorio temporal
# Recibe como parametros:
# - origin <-- String con el PATH del directorio temporal
# - destiny <-- String con el PATH del directorio donde guardara el archivo comprimido resultante
# - tar_name <-- Prefijo que utiliza para generar el nombre del backup
# - OBLog <-- Objeto del tipo "logging" para acceder al sistema de logs

def archive_backup(origin,destiny,tar_name,OBLog):
	try:
		# Importa el modulo time para obtener el timestamp para generar el nombre del backup
		import time
		timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
	except:
		OBLog.db("No se pudo obtener el timestamp")
		timestr = ""

	try:
		# Importa el modulo tarfile para genera el archivo comprimido. Si no puede importarlo lo registra en el log 
		# y finaliza la ejecucion del script
		import tarfile
	except:	
		OBLog.db("No se puede importar la libreria para comprimir archivos")
		exit(2)

	#Genera el nombre el archivo de destino
	filename = destiny + "/" + tar_name + "_" + timestr + ".tar.gz"
	

	if os.path.exists(filename):
		# Si el achivo en destino existe finaliza el programa para eviar sobre escribirlo
		OBLog.inf("El archivo " + filename + " ya existe y no se puede continuar")
		exit(4)
	
	# Registra los path de los directorios de origen y destino si esta en modo DEBUG
	OBLog.db("Backup Destiny: " + filename)
	OBLog.db("Backup Origin: " + origin)

	# Intenta crear el archivo de destino con el contenido del directorio temporal. 
	# Si falla registra el error en el log y sale
	try:
		tar = tarfile.open(filename, "w:gz")
		if test_mode() == True:
			print("Creando archivo comprimido...")
			OLBLog.inf("Creando archivo comprimido...")
		else:
			tar.add(origin, arcname=origin)
		tar.close()
	except TarError as err:
		OLBLog.inf("No se pudo comprimir el directorio temporal")
		OLBLog.db("Error: " + err)
		exit(4)
#
