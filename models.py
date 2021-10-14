from sqlalchemy import create_engine, Column, String, Integer, DECIMAL, ForeignKey, Boolean
from sqlalchemy.orm import session, sessionmaker
import os

os.remove('C:\\Users\\cflor\\BB\\Strips.db')
engine = create_engine('sqlite:///C:\\Users\\cflor\\BB\\Strips.db', echo = False)
Session = sessionmaker(bind=engine)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Pickup(Base):

   __tablename__ = 'Pickup'

   pickup_id = Column(Integer, primary_key=True)
   date =Column(String)
   client_id = Column(Integer, ForeignKey('Client.client_id'))
   product=Column(String)
   updated=Column(Boolean)

class Client(Base):

   __tablename__='Client'

   client_id=Column(Integer, primary_key=True)
   name=Column(String)
   address=Column(String)

class Predict(Base):

   __tablename__='Predict'

   predict_id=Column(Integer, primary_key=True)
   date=Column(String)
   product=Column(String)
   client_id=Column(Integer, ForeignKey('Client.client_id'))
   city_state=Column(String)
   days=Column(Integer)
   numberDays=Column(Integer)
   aveDays=Column(Integer)

class Summary(Base):

   __tablename__='Summary'

   summary_id=Column(Integer, primary_key=True)
   startDate=Column(String)
   numberPickups=Column(Integer)
   lastDate=Column(String)
   lastProduct=Column(String)
   client_id = Column(Integer, ForeignKey('Client.client_id'))


Base.metadata.create_all(engine)