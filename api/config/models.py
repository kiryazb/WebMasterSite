from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class GroupConfigAssociation(Base):
    __tablename__ = 'group_config_association'

    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)
    config_id = Column(Integer, ForeignKey('config.id'), primary_key=True)


class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    database_name = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    host_id = Column(String, nullable=False)

    # Используем строку для связи с Group
    groups = relationship("Group", secondary='group_config_association', back_populates="configs")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)

    # Используем строку для связи с Config и User
    configs = relationship("Config",
                           secondary='group_config_association',
                           back_populates="groups",
                           lazy="selectin"
                           )
    users = relationship("User",
                         secondary='group_user_association', back_populates="groups",
                         lazy="selectin"
                         )

class List(Base):
    __tablename__ = "list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    author = Column(Integer,ForeignKey("user.id"), nullable=False)
    group = Column(Integer, ForeignKey("group.id"), nullable=False)
    config = Column(Integer, ForeignKey("config.id"), nullable=False)
    is_public = Column(Boolean, nullable=False, default=False)

    uris = relationship("ListURI", back_populates="list")

class ListURI(Base):
    __tablename__ = "list_uri"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uri = Column(String, nullable=False)
    list_id = Column(Integer, ForeignKey("list.id"), nullable=False)

    # Связь с List
    list = relationship("List", back_populates="uris")
