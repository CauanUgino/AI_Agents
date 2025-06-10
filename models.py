from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Enum, Boolean, ForeignKey, Date
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    tipo = Column(Enum('comum', 'moderador', 'administrador'), default='comum')

    verificacoes = relationship("Verificacao", back_populates="usuario")

class Agente(Base):
    __tablename__ = 'agentes'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    especialidade = Column(String(100))
    ativo = Column(Boolean, default=True)

    verificacoes = relationship("Verificacao", back_populates="agente")

class Tema(Base):
    __tablename__ = 'temas'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)
    descricao = Column(Text)

    verificacoes = relationship("Verificacao", back_populates="tema")

class Verificacao(Base):
    __tablename__ = 'verificacoes'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    agente_id = Column(Integer, ForeignKey('agentes.id'))
    tema_id = Column(Integer, ForeignKey('temas.id'))
    titulo = Column(Text, nullable=False)
    texto_original = Column(Text, nullable=False)
    data_verificacao = Column(Date)
    classificacao = Column(Enum('Verdadeiro', 'Falso', 'Parcialmente verdadeiro', 'Impreciso', 'Enganoso'), nullable=False)
    parecer = Column(Text)
    relatorio = Column(Text)

    usuario = relationship("Usuario", back_populates="verificacoes")
    agente = relationship("Agente", back_populates="verificacoes")
    tema = relationship("Tema", back_populates="verificacoes")
    fontes = relationship("Fonte", back_populates="verificacao", cascade="all, delete-orphan")

class Fonte(Base):
    __tablename__ = 'fontes'

    id = Column(Integer, primary_key=True)
    verificacao_id = Column(Integer, ForeignKey('verificacoes.id'), nullable=False)
    url = Column(Text, nullable=False)
    descricao = Column(Text)

    verificacao = relationship("Verificacao", back_populates="fontes")
