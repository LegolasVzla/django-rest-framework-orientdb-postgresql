from core.settings import ORIENTDB
import pyorient

def orientdbConnection():
	"""Orientdb client connection for destroy methods in api (not available 
	delete function in pyorient OGM yet
	"""
	client = None
	try:
		client = pyorient.OrientDB(ORIENTDB['HOST'], int(ORIENTDB['PORT']))
		session_id = client.connect( ORIENTDB['USER'], ORIENTDB['PASSWORD'] )
		if client.db_exists( ORIENTDB['NAME'], pyorient.STORAGE_TYPE_MEMORY ):
			#print("Database",ORIENTDB['NAME'],"exists")
			client.db_open( ORIENTDB['NAME'], ORIENTDB['USER'], ORIENTDB['PASSWORD'])
	except Exception as e:
		print ("[ ERROR ] Fail orientdb connection. Error: " + str(e))
	return client
