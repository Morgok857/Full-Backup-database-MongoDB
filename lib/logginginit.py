#/usr/bin/python
## Import Dependences
import logging
#

def start_logging(logdir,lvlbg):
	
	## Config logging object format
	formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

	if lvlbg == "INFO":
		logging.basicConfig(filename=logdir,format=formatter,level=logging.INFO)
	
	elif lvlbg == "DEBUG":
		logging.basicConfig(filename=logdir,format=formatter,level=logging.DEBUG)
	else:
		logging.basicConfig(filename=logdir,format=formatter,level=logging.INFO)
	#	


	## Create Class logging
	class logg ():
			def __init__(self):
					logging.info("Start process")

			def inf (self, message):
					logging.info(message)

			def db (self, message):
					logging.debug(message)
	#

	## Return Logging object
	return logg()
