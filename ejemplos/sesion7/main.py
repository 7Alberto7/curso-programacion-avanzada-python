import threading

ruta_archivo = "/var/www/log"


def descargar_url_y_procesar(url):  # usa ruta_archivo

    hilo_procesar = threading.Thread()

    hilo_procesar.start()
    hilo_procesar.join()
    pass


def procesar_archivo(ruta): #usa ruta archivo
    pass



if __name__ == "__main__":


    hilo_web = threading.Thread(target=descargar_url, args=('https://loquesea'))



    # iniciar los hilos

    hilo_web.start()
    







    # esperamos a que acaben

    hilo_web.join()


    hilo_archivo = threading.Thread(target=procesar_archivo,args=(''))
    hilo_archivo.start()

    # hilo_archivo.join()

    print("tareas completadas")
