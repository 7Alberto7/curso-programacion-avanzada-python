import unittest
from app.modelos import Moderador

class TestModerador(unittest.TestCase):


    def test_moderador_nivel2_no_puede_borrar(self):
        m = Moderador("pepe","a@a.a",2)
        self.assertNotIn("borrar",m.permisos())
    
    def test_permisos_moderador(self):
        m1 = Moderador("pepe","a@a.a",1)
        m2 = Moderador("pepe","a@a.a",2)
        self.assertEqual(m1.permisos(),["borrar","leer"])
        self.assertEqual(m2.permisos(),["borrar","leer"])