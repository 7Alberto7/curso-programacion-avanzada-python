from sqlalchemy import Integer, String, Column, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Autor(Base):
    __tablename__ = "autores"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    # relacion uno a muchos ... un autor muchos libros
    libros = relationship('Libro', back_populates='autor')
    


class Libro(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True)
    titulo = Column(String)
    #clave necesaria
    autor_id = Column(Integer, ForeignKey('autores.id'))
    # relacion inversa
    autor = relationship("Autor", back_populates="autor")


estuduante_curso = Table('estudiante_curso',
      Base.metadata,
      Column('estudiante_id', Integer, ForeignKey('estudiantes.id')),
      Column('curso_id', Integer, ForeignKey('cursos.id'))       
)


# many to many
class Estudiante(Base):
    __tablename__ = "estudiantes"
    id = Column(Integer, primary_key=True)
    cursos = relationship("Curso", back_populates="estudiantes", secondary=estuduante_curso)

class Curso(Base):
    __tablename__ = "cursos"
    id = Column(Integer, primary_key=True) 
    estudiantes = relationship("Estudiante", back_populates="cursos", secondary=estuduante_curso)