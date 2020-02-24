from django.shortcuts import render
from django.http import HttpResponse
#librerias para imagenes
from random import sample
import matplotlib.pyplot as plt 
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
#librerias para analisis
import tweepy
import pandas as pd
import numpy as np
import statistics as st

# Create your views here.

def index(request):
    #template= loader.get_template('modulopolls/index.html')
    p='casa en el arbol'
    context ={
        'prueba': p,
        'r': request
    }
    #cargarUsuario()

    #return HttpResponse(template.render(context, request))
    return render(request, 'analisis/index.html', context )

#def prueba(request, question_id):
def prueba(request):
    return HttpResponse("You're looking at question " )

def imagen(request):
    # Creamos los datos para representar en el gráfico
    x = range(1,11)
    y = sample(range(20), len(x))

    # Creamos una figura y le dibujamos el gráfico
    f = plt.figure()

    # Creamos los ejes
    axes = f.add_axes([0.15, 0.15, 0.75, 0.75]) # [left, bottom, width, height]
    axes.plot(x, y)
    axes.set_xlabel("Eje X")
    axes.set_ylabel("Eje Y")
    axes.set_title("Mi gráfico dinámico")

    # Como enviaremos la imagen en bytes la guardaremos en un buffer
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    # Creamos la respuesta enviando los bytes en tipo imagen png
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    # Limpiamos la figura para liberar memoria
    f.clear()

    # Añadimos la cabecera de longitud de fichero para más estabilidad
    response['Content-Length'] = str(len(response.content))

    # Devolvemos la response
    return response

def imagenn(f):
    # Como enviaremos la imagen en bytes la guardaremos en un buffer
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    # Creamos la respuesta enviando los bytes en tipo imagen png
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    # Limpiamos la figura para liberar memoria
    f.clear()

    # Añadimos la cabecera de longitud de fichero para más estabilidad
    response['Content-Length'] = str(len(response.content))

    # Devolvemos la response
    return response



def cargarUsuario():
    consumer_key = "CJVtZ2a5ELNTxARuwaV2DXrsX"
    consumer_secret = 'CBriIKv8M6pHW2cITIgSkPuSDJLgdY1Azz0mdc54lBEVnvxkC7'
    access_token = '1227756341973921794-J10AVvaG5bRXVF13j78ejO6srGvGc6'
    access_token_secret = 'il2tYCcQfHjJfcb80DxyNi0lSQQcKVgDGmguhgGZjgmU5'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    try:
        api
    except :
        api= tweepy.API(auth)
    
    if not autenticarCredenciales(api):
        print('las credenciales no sirven')
        api= tweepy.API(auth)
    return api
    


def autenticarCredenciales(ap):
    try:
        print('Autenticando Credenciales...')
        ap.verify_credentials()
        print("Credenciales correctas")
        return True
    except:
        print("Las credenciales no se han validado correctamente")
        return False


def buscarTrendings(ap, query):
    lista = []
    tweets = ap.search(q=query, lang="es")
    for tweet in tweets:
        lista.append(tweet._json)
    return lista


def dictToDataframe(jsonData):
    dataFrame = pd.DataFrame.from_dict(jsonData)
    return dataFrame


def bajarDatos(ap, hashtags):
    df = pd.DataFrame()
    for linea in hashtags:
        prueba = buscarTrendings(ap, linea)
        for i in prueba:
            aux = dictToDataframe(i)
            try:
                df = df.append(aux, ignore_index=True)
            except:
                print("No se ha podido agregar el Dataframe: ",i)


    return df

def filtrarColumna(datos, columna):
    return datos[datos[columna] != 'nan']

def contarTweets(datos, columna):
    suma = datos.pivot_table(index=[columna], aggfunc='size')
    return suma

def graficarBarras(datos, y_pos, x_pos, columna, titulo, label_x, size):
    f = plt.figure(figsize=(size, size))
    ax = f.add_axes([0.15, 0.15, 0.75, 0.75]) # [left, bottom, width, height]
    ax.barh(y_pos, datos[x_pos], align='center')    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(datos[columna])
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(label_x)
    ax.set_title(titulo)
    #fig.show()
        # Como enviaremos la imagen en bytes la guardaremos en un buffer
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    # Creamos la respuesta enviando los bytes en tipo imagen png
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    # Limpiamos la figura para liberar memoria
    f.clear()

    # Añadimos la cabecera de longitud de fichero para más estabilidad
    response['Content-Length'] = str(len(response.content))

    # Devolvemos la response
    return response

#    return f

    
def graficaBarrasHorizontal(x_label, y_pos, datos, columna, y_label, titulo):
    plt.bar(y_pos, datos[columna], align='center')
    plt.xticks(y_pos, datos[x_label], rotation=90)
    plt.ylabel(y_label)
    plt.title(titulo)

def hallarMedia(columna):
    return columna.mean()

def hallarModa(columna):
    return st.mode(columna)


def analisis(request, eleccion):
            
    api= cargarUsuario()    
    datosTwitter = bajarInfo(api)

  
    is_truncated = datosTwitter['truncated'].value_counts()
    is_truncated = is_truncated.reset_index()
    img1= graficarBarras(is_truncated, np.arange(len(is_truncated)), 'truncated','index', 'Número de Tweets truncados', 'Cantidad Truncados', 10)

    lugar = datosTwitter['place'].value_counts()

    datosTwitter.replace(to_replace=[None], value='nan', inplace=True)
    lugares = filtrarColumna(datosTwitter, 'place')
    usuarios = filtrarColumna(datosTwitter, 'user')

    retweets = contarTweets(usuarios, 'text')
    retweets = retweets.reset_index()
    retweets['text'] = retweets['text'].str[:30]

    modaRetweets = hallarModa(retweets[0])
    mediaRetweets = hallarMedia(retweets[0])
    graficaModaRetweets = retweets[retweets[0] > modaRetweets]
    img2=graficarBarras(graficaModaRetweets, np.arange(len(graficaModaRetweets)), 0, 'text', 'Número de Retweets', 'Retweets que superan la moda', 20)

    graficaMediaRetweets = retweets[retweets[0] > mediaRetweets]
    img3=graficarBarras(graficaMediaRetweets, np.arange(len(graficaMediaRetweets)), 0, 'text', 'Número de Retweets', 'Retweets que superan la media', 20)
    if eleccion ==1 :
        x=img1
    elif eleccion==2:
        x=img2
    elif eleccion ==3 :
        x=img3
    else:
         x="dato invalido"
    return x

def bajarInfo(api):
    datosTwitter = pd.DataFrame()
    palabras = ["#uberColombia"]
    #palabras = ["#UberOTaxi"]
    for i in palabras:
        datosTwitter = datosTwitter.append(bajarDatos(api, i))
    return datosTwitter


