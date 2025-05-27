from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[list["Favorites"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_year: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    favorites: Mapped[list["Favorites"]] = relationship(back_populates="people", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "birth_year":self.birth_year,
            "height": self.height
        }

class Vehicules(db.Model):
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    crew: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    passengers: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    favorites: Mapped[list["Favorites"]] = relationship(back_populates="vehicules", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "crew":self.crew,
            "passengers":self.passengers,
        }

class Planet(db.Model):
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    favorites: Mapped[list["Favorites"]] = relationship(back_populates="planet", cascade="all, delete-orphan")
    
    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "population":self.population,
        }


class Favorites(db.Model):
    id: Mapped[int]= mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)
    vehicules_id: Mapped[int] = mapped_column(ForeignKey("vehicules.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    people: Mapped["People"] = relationship(back_populates="favorites")
    vehicules: Mapped["Vehicules"] = relationship(back_populates="favorites")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id":self.id,
            "user_id": self.user.id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
            "vehicules_id": self.vehicules_id,
            
            "people": self.people.serialize() if self.people else None,
            "planet": self.planet.serialize() if self.planet else None,
            "vehicules": self.vehicules.serialize() if self.vehicules else None,
    } 
        
    