#/usr/bin/python3

#Import Lib
import os
import logging
from ConfigParser import ConfigParser
from lib.logginginit import start_logging
from lib.function import *
#

#Get path script
diripath = os.path.dirname(os.path.realpath(__file__))
#

#Load config file
pathcfg = diripath + "/config.cfg"

try:
	config = ConfigParser()
	config.read(pathcfg)
except Exception as e:
	print("No se encuentra el archivo  de configuracion")
	exit(1)
#

#Config Logging
if config.has_option("LOG","Log_name"):
	log_file_name = config.get("LOG","Log_name")
else:
	log_file_name = "/backup.log"

if config.has_option("LOG","Log_level"):
	log_level = config.get("LOG","Log_level")
else:
	log_level = "DEBUG"

try:
	logdir = diripath + "/" + log_file_name
	if os.path.exists(diripath + "/test.mode"):
	        print("Log File: " + logdir)
	logger=start_logging(logdir,log_level)
	logger.inf("Log level: " + log_level)
except:
	print("Error al abrir el archivo de log.")
	exit(2)

### Create environment
## GENERAL Config
if config.has_option("GENERAL","Temp_dir") and not config.get("GENERAL","Temp_dir") == "" and not config.get("GENERAL","Temp_dir") == " ":
	temp_dir = config.get("GENERAL","Temp_dir")
elif config.get("GENERAL","Temp_dir") == "" or not config.get("GENERAL","Temp_dir") == " ":
	temp_dir = "/tmp/backup-mongodb"

if config.has_option("GENERAL","Backup_dir") and not config.get("GENERAL","Backup_dir") == "" and not config.get("GENERAL","Backup_dir") == " ":
	bkp_dir = config.get("GENERAL","Backup_dir")
elif config.get("GENERAL","Backup_dir") == "" or not config.get("GENERAL","Backup_dir") == " ":
	bkp_dir = diripath + "/backup"

if config.has_option("GENERAL","Default_bkp_name") and not config.get("GENERAL","Default_bkp_name") == "" and not config.get("GENERAL","Default_bkp_name") == " ":
	default_bkp_name = config.get("GENERAL","Default_bkp_name")
elif config.get("GENERAL","Default_bkp_name") == "" or not config.get("GENERAL","Default_bkp_name") == " ":
	 default_bkp_name = "bkp-mongodb"

if test_mode(logger):
	logger.inf("Modo test")
else:
	logger.inf("Modo ejecucion")
#

##Get DB Config
DB_CONFIG = {};
for config_item in config.items('DB'):
	DB_CONFIG.update({config_item[0]:config_item[1]})
##
#

## General Config
temp_dir = diripath + '/' + temp_dir
log_file_name = diripath + '/' + log_file_name
bkp_dir = diripath + '/' + bkp_dir
##
#

##Show env
logger.db('diripath: ' + diripath )
logger.db("bkp_dir: " + bkp_dir)
if config.get("LOG","Log_level") == 'DEBUG':
	for config_item in DB_CONFIG:
		logger.db(config_item + ': ' + DB_CONFIG[config_item])
logger.db("log_file_name: " + log_file_name)
logger.db("log_level:  "+ log_level)
logger.db("logdir:  "+ logdir)
logger.db("temp_dir: "+ temp_dir)
logger.db("default_bkp_name: " + default_bkp_name)
#


