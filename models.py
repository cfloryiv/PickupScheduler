from sqlalchemy import create_engine, Column, String, Integer, DECIMAL, ForeignKey, Boolean
from sqlalchemy.orm import session, sessionmaker
import os
try:
   os.remove('C:\\Users\\cflor\\BB\\Strips.db')
except:
   print('Database could not be found to be deleted')

engine = create_engine('sqlite:///C:\\Users\\cflor\\BB\\Strips.db', echo = False)
Session = sessionmaker(bind=engine)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class ListMaint(Base):

   __tablename__='ListMaint'

   lm_id=Column(Integer, primary_key=True)
   name=Column(String)
   oldAddress=Column(String)
   newAddress=Column(String)
   action=Column(String)
   newName=Column(String)


class Pickup(Base):

   __tablename__ = 'Pickup'

   pickup_id = Column(Integer, primary_key=True)
   date =Column(String)
   client_id = Column(Integer, ForeignKey('Client.client_id'))
   product=Column(String)
   updated=Column(Boolean)
   dollars=Column(Integer)
   name=Column(String)
   address=Column(String)
   city_state=Column(String)

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