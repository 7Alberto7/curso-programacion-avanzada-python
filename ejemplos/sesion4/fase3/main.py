# main.py
import argparse
from app.modelos import  Usuario

if __name__ == "__main__":
    # a = AdminFull("Root", "root@corp.com")
    # print(a.presentarse())           # debería loguear la llamada
    # a.activar()


    # a.enviar_email('hola','mensaje')                      # logs antes y después gracias al mixin

    # print("MRO AdminConLogger:", AdminConLogger.mro())


    m = Usuario("Root", "root@corp.com")

    m.activar()

    # m.log_evento('efasfa')
    

    # m.enviar_email('gsdgsd','gsdgsdg')

    # m.log_evento()
    # m.auditar('un evento')
    # m.auditar('otro evento')
    # m.auditar('tercer evento')


    # m.observar()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nombre", help="Nombre del usuario")
    args = parser.parse_args()

    u = Usuario(args.nombre,'asda@dasdas.es')
    print("Usuario creado:", u)

if __name__ == "__main__":
    main()