# servidor/modelos.py
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Tabla para almacenar resultados de N reinas
class ResultadoNReinas(Base):
    __tablename__ = 'n_reinas'
    id = Column(Integer, primary_key=True)
    n = Column(Integer)
    resuelto = Column(Boolean)
    pasos = Column(Integer)

# Tabla para el Recorrido del Caballo
class ResultadoCaballo(Base):
    __tablename__ = 'caballo'
    id = Column(Integer, primary_key=True)
    posicion_inicial = Column(String)
    movimientos = Column(Integer)
    completado = Column(Boolean)

# Tabla para Torres de Hanói
class ResultadoHanoi(Base):
    __tablename__ = 'hanoi'
    id = Column(Integer, primary_key=True)
    discos = Column(Integer)
    movimientos = Column(Integer)
    resuelto = Column(Boolean)

# Crear engine y sesión
engine = create_engine("sqlite:///servidor/resultados.db")
Session = sessionmaker(bind=engine)

def inicializar_bd():
    Base.metadata.create_all(engine)
