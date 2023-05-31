from neo4j import GraphDatabase
class Neo4jConnection:
    
    # Cuando inicia el programa se conecta con la base de datos.
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
        	#En caso de error se le notifica al usuario
            print("Failed to create the driver:", e)
        
    def close(self):
    	#Cuando finaliza el programa
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
    	#Cuando se realiza una solicitud a la base de datos.
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response