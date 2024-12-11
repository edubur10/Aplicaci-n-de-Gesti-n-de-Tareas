from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///tareas.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class Tarea(Base):
    __tablename__ = "tareas"
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    completada = Column(Boolean, default=False)

    def __repr__(self):
        estado = "✔" if self.completada else "✘"
        return f"[{self.id}] {self.titulo} - {estado}"

Base.metadata.create_all(engine)
