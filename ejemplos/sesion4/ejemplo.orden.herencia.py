# class A:
#     def accion(self):
#         print("A empieza")
#         print("A termina")

# class B(A):
#     def accion(self):
#         print("B empieza")
#         super().accion()
#         print("B termina")

# class C(A):
#     def accion(self):
#         print("C empieza")
#         super().accion()
#         print("C termina")

# class D(B, C):
#     def accion(self):
#         print("D empieza")
#         super().accion()
#         print("D termina")

# # ---- Ejecutamos ----
# d = D()
# d.accion()

# print("MRO:", D.mro())





class A: 
    def saludar(self): return "A"

class B(A): 
    def saludar(self): return "B"

class C(A): 
    def saludar(self): return "C"

class D(B, C): 
    pass

d = D()
print(d.saludar())     # "B" según el MRO
print(D.mro())         # [D, B, C, A, object]