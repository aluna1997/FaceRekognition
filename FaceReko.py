#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import ClientError

def obtener_bytes_imagen(ruta_imagen):
    with open(ruta_imagen, "rb") as imagen:
        return imagen.read()

def comparar_rostros(ruta_imagen1,ruta_imagen2):
    bytes_1 = obtener_bytes_imagen(ruta_imagen1)
    bytes_2 = obtener_bytes_imagen(ruta_imagen2)

    cliente = boto3.client('rekognition')
    try:
        respuesta = cliente.compare_faces(SourceImage = {'Bytes' : bytes_1}, 
                                          TargetImage = {'Bytes': bytes_2},
                                          SimilarityThreshold = 60,
                                          QualityFilter = 'NONE')
        
        #QUALITY FILTER: NONE'|'AUTO'|'LOW'|'MEDIUM'|'HIGH'

    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)

    if respuesta and respuesta.get('ResponseMetadata').get('HTTPStatusCode') == 200:
        # UnmatchedFaces
        for i in respuesta['UnmatchedFaces']:
            print(i)
            print('\n')

        # FaceMatches
        for i in respuesta['FaceMatches']:

            # FACE
            print('BoundingBoxWidth: ',i['Face']['BoundingBox']['Width'])
            print('BoundingBoxHeight: ',i['Face']['BoundingBox']['Height'])

            # QUALITY
            print('QualityBrightness: ',i['Face']['Quality']['Brightness'])
            print('QualitySharpness: ',i['Face']['Quality']['Sharpness'])
            
            # SIMILARITY
            print('Similarity: ', i['Similarity'])
            
def crear_coleccion(nombre_coleccion):
    cliente = boto3.client('rekognition')
    try:
        respuesta = cliente.create_collection(CollectionId=nombre_coleccion)
        print(respuesta)
    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)

def listar_colecciones():
    cliente = boto3.client('rekognition')
    try:
        response = cliente.list_collections()
        while True:
            collections = response['CollectionIds']
            for collection in collections:
                print(collection)
            if 'NextToken' in response:
                nextToken = response['NextToken']
                response = cliente.list_collections(NextToken=nextToken)
            else:
                break
    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)

def agregar_rostro_coleccion(nombre_coleccion,ruta_imagen):
    cliente = boto3.client('rekognition')
    bytes_1 = obtener_bytes_imagen(ruta_imagen)
    nombre_imagen = ruta_imagen.split('/')[-1]
    try:
        response = cliente.index_faces(CollectionId = nombre_coleccion,
                                       Image = {'Bytes':bytes_1},
                                       ExternalImageId = nombre_imagen,
                                       MaxFaces = 1,
                                       QualityFilter = "AUTO")
        
        for agregadas in response['FaceRecords']:
            print('Caras agregadas a la coleccion: ' + '\n')
            print('Identificador personal: ' + agregadas['Face']['ExternalImageId'])
            print('Identificador AWS: ' + agregadas['Face']['FaceId'])
            
        for noAgregadas in response['UnindexedFaces']:
            print('Razones:' + '\n')
            for razon in noAgregadas['Reasons']:
                print('   ' + razon + '\n')
    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)

def eliminar_rostro_coleccion(nombre_coleccion,face_id_aws):
    cliente = boto3.client('rekognition')
    try:
        response = cliente.delete_faces(CollectionId = nombre_coleccion,FaceIds = [face_id_aws])
        print('Rostros eliminados: ' + str(response['DeletedFaces']))
    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)


def listar_rostros_coleccion(nombre_coleccion):
    cliente = boto3.client('rekognition')
    try:
        response = cliente.list_faces(CollectionId = nombre_coleccion)
        tokens = True
        while tokens:
            faces = response['Faces']
    
            for face in faces:
                print('Identificador AWS: ', face['FaceId'])
                print('Identificador personal: ' + face['ExternalImageId'])
            if 'NextToken' in response:
                nextToken = response['NextToken']
                response = cliente.list_faces(CollectionId = nombre_coleccion,NextToken = nextToken)
            else:
                tokens = False
    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)


def comparar_rostro_coleccion(nombre_coleccion,ruta_imagen):
    cliente = boto3.client('rekognition')
    bytes_1 = obtener_bytes_imagen(ruta_imagen)
    try:
        response = cliente.search_faces_by_image(CollectionId = nombre_coleccion,
                                                 Image = {'Bytes':bytes_1},
                                                 FaceMatchThreshold = 85)
        rostrosCoincidentes = response['FaceMatches']
        for i in rostrosCoincidentes:
            print('Similarity: ' + str(i['Similarity']))
            print('Identificador AWS: ' + i['Face']['FaceId'])
            print('Identificador personal: ' + i['Face']['ExternalImageId'])

    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)

def eliminar_colleccion(nombre_coleccion):
    cliente = boto3.client('rekognition')
    try:
        response = cliente.delete_collection(CollectionId = nombre_coleccion)
        statusCode = response['StatusCode']
        if statusCode == 200:
            print('Se elimino la colleccion: ' + nombre_coleccion + ' correctamente')
    except ClientError as error:
        print("Ocurrio un error al llamar a la API:",error)



if __name__ == "__main__":
    #comparar_rostros('/home/falv/Imágenes/Uno.jpg','/home/falv/Imágenes/Cuatro.jpg')
    #crear_coleccion('MoonCodeTeam')
    #listar_colecciones()
    #agregar_rostro_coleccion('MoonCodeTeam','/home/falv/Imágenes/Uno.jpg')
    #eliminar_rostro_coleccion('MoonCodeTeam','0d1f6e9e-9a74-4a57-87b9-721766f433ae')
    #listar_rostros_coleccion('MoonCodeTeam')
    #comparar_rostro_coleccion('MoonCodeTeam','/home/falv/Imágenes/Uno.jpg')
    eliminar_colleccion('MoonCodeTeam')