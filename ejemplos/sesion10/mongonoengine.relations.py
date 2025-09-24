from mongoengine import Document, connect, StringField, IntField, ReferenceField, ListField


connect('mibasededatos')



class Libro(Document):
    autor = ReferenceField(Autor)


class Autor(Document):
    nombre = StringField(required=True)
    edad = IntField()
    libros = ListField(ReferenceField(Libro))







a = Autor(nombre='David').save()
l = Libro(autor=a).save()

a.nombre = 'pepe'

a.save()
