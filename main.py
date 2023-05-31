from neo4j import GraphDatabase
from connection import *
import random


contra="Computologo"

"""
agregar: 
una opcion para agregar mas componentes al grafo. En esta opcion
el usuario ingresa la informacion de la cancion que esta agregando
"""
def agregar(connection, db):
    #Se le solicita al usuario que ingrese una contrasena
    palabra=input("Por favor ingrese la palabra clave \n")
    if palabra == contra:
        # Se le solicita al usuario que ingrese los datos
        cancion=input("Ingrese el nombre de la cancion a agregar a la base de datos \n >")
        datos = {"Artista":"", "Genero":"","EstadoDeAnimo":"","Estrellas":""}
        # El ciclo FOR recorre el diccionario datos y guarda la informacion que el usuario ingrese.
        for keys in datos:
            print("Seleccione la opcion con la que se siente más identificado según "+keys )
            dictionary = elementos(connection, db, keys)
            elec = eleccion(dictionary)
            datos[keys] = elec
        # Se le asigna un ranking de 0 porque al ser un dato nuevo, no se le ha recomendado a nadie
        datos["Ranking"]=0
        # Primer query para crear la cancion
        query = '''
            CREATE (p:Cancion{cancion:"%s", ranking:'0'})
        '''%(cancion)
        connection.query(query, db)
        # Se envia otro query uniendo a la cancion con sus caracteristicas. Se envia en estructura del codigo de cypher para que la plataforma entienda el query.
        query='''MATCH (p:Cancion) WHERE p.cancion = '%s'
                MATCH (p1:Artista) WHERE p1.artista = '%s' 
                MERGE (p) -[:Artista]-> (p1) WITH p
                MATCH (p2:Genero) WHERE p2.genero = '%s'
                MERGE (p) -[:Genero]->(p2) WITH p
                MATCH (p3:EstadoDeAnimo) WHERE p3.estadoDeAnimo = '%s' 
                MERGE (p) -[:EstadoDeAmimo]->(p3) WITH p
                MATCH (p4:Estrellas) WHERE p4.estrellas = '%s' 
                MERGE (p) -[:Estrellas]->(p4) WITH p
            '''%(cancion,datos['Artista'],datos['Genero'],datos['EstadoDeAmimo'],datos['Estrellas'])
        connection.query(query, db)
    else:
        #contrasena es incorrecta
        print("Palabra clave incorrecta, Esta opción es unicamente para personal calificado")


"""
quitar:  eliminar comparando el nombre
que se ingreso con las canciones almacenadas.
"""
def quitar(connection, db):
    #Se le solicita al usuario que ingrese una contrasena
    palabra=input("Por favor ingrese la palabra clave\n")
    if palabra == contra:
        condicion=True
        query = 'MATCH (n:Cancion) return n.cancion'
        temp = connection.query(query, db)
        i = 1
        dictionary = {}
        # Se hace un ciclo while para imprimir todos las canciones del grafo y luego devolver la cancion que el usuario haya ingresado
        while condicion:
            for elements in temp:
                dictionary[i] = elements['n.cancion']
                print(f"{i}) {dictionary[i]}")
                i = i+1
            cancion= input("Ingrese el numero de la cancion que desea eliminar")
            try:
                cancion = int(cancion)
                if cancion<len(dictionary)+1:
                    query= 'MATCH (p:Cancion{cancion:"%s"}) detach delete p'%(dictionary[cancion])
                    temp = connection.query(query, db)
                    condicion=False
                else:
                    #En caso que no se encuentre la cancion
                    print("La opcion ingresada no existe")
            except:
                #En caso que no haya ingresado un numero
                print("Ingresar unicamente números")
    else:
        # En caso que haya ingresado una contrasena incorrecta
        print("Contrasena incorrecta")
        

"""
query ranking Esta Funcion devuelve la cancion con mayor ranking del grafo.

"""
def query_ranking(connection, query_result):
    canciones = {}
    #Se almacena en un diccionario cada cancion encontrada con su ranking
    for element in query_result:
        canciones[element['p.cancion']] = int(element['p.ranking'])

    #Se hace un sort para encontrar el ranking mas grande y su cancion. 
    #El primer elemento de sort_dic es la cancion con mayor ranking.
    sort_dict = dict(sorted(canciones.items(), key=lambda item: item[1], reverse=True))
    first_key = list(sort_dict.keys())[0]
    first_value = list(sort_dict.values())[0]
    if TYC:
        first_value = first_value + 1
    query = '''
        MATCH (p:Cancion {cancion: '%s'}) SET p.ranking = '%s' RETURN p
    '''%(first_key, str(first_value))
    connection.query(query, db)
    return first_key


"""
elementos Esta Funcion devuelve un diccionario con los elementos segun
el tipo y el diferenciador que el usuario ingrese
"""
def elementos(connection, db, tipo):
    diferenciador = tipo[0:1].lower() + "" + tipo[1:len(tipo)]
    # Se envia el query a neo4j con los datos que ingreso el usuario
    query = f'MATCH (p:{tipo}) return p.{diferenciador}'
    temp = connection.query(query, db)
    i = 1
    dictionary = {}
    # Por cada elemento recibido, se agrega un valor al diccionario.
    for elements in temp:
        dictionary[i] = elements[f'p.{diferenciador}']
        i = i+1
    return dictionary


def eleccion(dic):
    bandera=True
    while bandera:
        i = 1
        for keys in dic:
            print(str(i) + " " + dic[keys])
            i = i + 1
        elecop=input("\nLa opcion con la que mas me identifico es la numero:\n>")
        try:
            elecop= int(elecop)
            if elecop > len(dic):
                print(f"La opcion {elecop} no se encuentra entre las opciones")   
            else:
                return dic[elecop]
                bandera=False
        except ValueError:
            print("Porfavor ingrese la opción en formato de numero")



"""
Esta Funcion aumenta el ranking de la cancion recomendada cada vez
que se muestra al usuario.
"""
def aumentar_ranking(cancion):
    query ='''
            MATCH (p:Cancion{cancion:"%s"}) return p.ranking'''%(cancion)
    #result = 


"""
Esta Funcion muestra al usuario el resultado obtenido por
la busqueda.
"""
def resultado(query):
    canciones = []
    for elements in query:
        canciones.append(elements['p.cancion'])

    i = random.randint(0,len(canciones)-1)
    return canciones[i]
    

"""
Esta Funcion solicita al usuario las caracteristicas que 
desea que el su cancion tenga, en base a esto se hace un query a
la base de datos de Neo4J y se le da una respuesta.
"""
def ConsultaUsuario(connection, db):
    datos = {"Artista":"", "Genero":"","EstadoDeAnimo":"","Estrellas":""}
    # Se solicita al usuario la opcion que desee segun la caracteristica
    for keys in datos:
        print("Seleccione la opcion con la que se siente más identificado según "+keys)
        dictionary = elementos(connection, db, keys)
        elec = eleccion(dictionary)
        datos[keys] = elec
    recomendacion = ""
    # Se le envia a la base de datos el query con las caracteristicas que selecciono el usuario
    query ='''
            MATCH (p:Cancion)-[:Artista]->(p1:Artista{artista:"%s"}),
            (p)-[:Artista]-> (p4:Artista{artista:"%s"}),
            (p)-[:EstadoDeAnimo]-> (p5:EstadoDeAnimo{estadoDeAnimo:"%s"}),
            (p)-[:Estrellas]-> (p11:Estrellas{estrellas:"%s"}) return p.cancion, p.ranking
           '''%(datos['Artista'],datos['Genero'],datos['EstadoDeAnimo'],datos['Estrellas'])
    query_result = connection.query(query, db)
    #Si se encuentra entonces se muestra al usuario.
    if query_result:
        recomendacion = query_ranking(connection, query_result)
    #En caso que no se encuentren, entonces se realiza un query con menos opciones
    elif not query_result:
        query ='''MATCH (p:Cancion)-[:Artista]->(p5:Artista{artista:"%s"}),
            (p)-[:EstadoDeAnimo]-> (p2:EstadoDeAnimo{estadoDeAnimo:"%s"}),
            (p)-[:Estrellas]-> (p3:Estrellas{estrellas:"%s"}) return p.cancion, p.ranking
            '''%(datos['Artista'],datos['EstadoDeAnimo'],datos['Estrellas'])
        query_result = connection.query(query, db)
        if query_result:
            recomendacion = query_ranking(connection, query_result)
        #En caso que no se encuentre de nuevo, se vuelve a hacer un query solo con el Artista.
        elif not query_result:
            query ='''MATCH (p:Cancion)-[:Artista]->(p5:Artista{artista:"%s"})  return p.cancion, p.ranking
                '''%(datos['Artista'])
            query_result = connection.query(query, db)
            recomendacion = query_ranking(connection, query_result)
    
    return recomendacion



def TerminosYCondiciones():
    respuesta=""
    while respuesta=="":
        print("""----------------Terminos y Condicioness--------------- \n
        Este sistema de recomendación, requiere de información porporcionada por usted,
        esta sirve unicamente con el proposito de brindarle una recomendación acertada. Los datos
        que se obtiene son totalmente privados. El sistema de recomendación desea pedirle permiso 
        para utilizar el resultado de la cancion que se le recomienda para agregarlo a un ranking y asi 
        mejorar las recomendaciones \n ¿Acepta?        
        """)
        respuesta=input("Si/No \n")
        if respuesta.lower()=="si" or respuesta.lower()=="no":
            if respuesta.lower()=="si":
                return True
            elif respuesta.lower()=="si":
                return False
        else:
            respuesta=""



#Conexiones a base de datos.
conn = Neo4jConnection(uri="bolt://localhost:####", user="neo4j", pwd="12345678")
db = 'neo4j'

#-----------------------Inicio del menu--------------------------------
print("¡Bienvenidos al sistema de recomendación de canciones!")

continuar=True
TYC=TerminosYCondiciones()
while(continuar):
    print("\n1)Realizar recomendación")
    print("2)Agregar a la base de datos")
    print("3)Eliminar de la base de datos")
    print("4)Salir\n")
    op1=input("¿Que opción desea realizar?\n>")
    try:
        op1=int (op1)
        
    except ValueError:
        print("Opcion no valida")

    if op1==1:
        RecomendacionExitosa=ConsultaUsuario(conn, db)
        print(f"Se le recomienda escuchar la cancion: {RecomendacionExitosa}")
        print(cancion)
    elif op1==2:#Agregar a la base de datos
        agregar(conn,db)
    elif op1==3:#Quitar de la base de datos
        quitar(conn,db)
    elif op1==4:
        continuar=False
        print("Muchas gracias por utilizar el sistema de recomendacion") 