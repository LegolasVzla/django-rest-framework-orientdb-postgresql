from core.settings import DATABASES
import pyorient

def orientdbConnection():
	"""Orientdb client connection for destroy methods in api (not available 
	delete function in pyorient OGM yet
	"""
	client = None
	try:
		client = pyorient.OrientDB(DATABASES['orientdb']['HOST'], int(DATABASES['orientdb']['PORT']))
		session_id = client.connect( DATABASES['orientdb']['USER'], DATABASES['orientdb']['PASSWORD'] )
		if client.db_exists( DATABASES['orientdb']['NAME'], pyorient.STORAGE_TYPE_MEMORY ):
			#print("Database",DATABASES['orientdb']['NAME'],"exists")
			client.db_open( DATABASES['orientdb']['NAME'], DATABASES['orientdb']['USER'], DATABASES['orientdb']['PASSWORD'])
	except Exception as e:
		print ("[ ERROR ] Fail orientdb connection. Error: " + str(e))
	return client
