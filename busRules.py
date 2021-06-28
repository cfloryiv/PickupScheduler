from models import engine, Session, Client, Pickup, Summary, Predict
from datetime import date
import csv

class ImportInputFiles():
    def run(filename):
        print('importing ', filename)
        count=0
        with open(f'C:\\users\\cflor\\BB\\inputFiles\\{filename}') as file:
            reader=csv.reader(file)
            for row in reader:
                count+=1
                if count==1:
                    continue
                if row[0]=='':
                    continue
                print(row)
                # create pickup record
                session=Session()
                # lookup client record
                client=Client()
                client.name=row[1]
                client.address=row[2]
                #
                client_id=None
                for clientx in session.query(Client).filter(Client.name==client.name and Client.address==client.address):
                    client_id=clientx.client_id
                if client_id==None:
                    session.add(client)
                    session.commit()
                    client_id=client.client_id

                pickup=Pickup()
                pickup.client_id=client_id
                pickup.date=row[0]
                pickup.product=row[3]
                pickup.updated=False
                #
                session.add(pickup);
                session.commit()
        return

class ProcessPickups():
    def run(self):
        session=Session()
        # select new pickup records
        for pickup in session.query(Pickup).filter(Pickup.updated==False):
            # locate summary record, otherwise create new record
                summary_id=None
                for summary in session.query(Summary).filter(Summary.client_id==pickup.client_id):
                    summary_id=summary.summary_id
                if summary_id==None:
                    summary=Summary()
                    summary.client_id=pickup.client_id
                    summary.startDate=pickup.date
                    summary.numberPickups=0
                    summary.lastDate=""
                    summary.lastProduct=""
                summary.numberPickups+=1
                if IconvDate(pickup.date)>=IconvDate(summary.lastDate):
                    summary.lastDate=pickup.date
                    summary.lastProduct=pickup.product
                session.add(summary);
                session.commit()
        session.query(Pickup).filter(Pickup.updated==False).update({Pickup.updated: True})
        session.commit()

            # update summary record

class CreatePredictions():
    def run(self):
        session=Session()
        # select summary record
        for summary in session.query(Summary):
            # read in client record
            client_id=summary.client_id
            for client in session.query(Client).filter(Client.client_id==client_id):
                address=client.address
            # determine new predict date
            startDate=IconvDate(summary.startDate)
            endDate=IconvDate(summary.lastDate)
            days=endDate-startDate
            predictDate=(startDate+days).isoformat()
            # create city_state variable
            ax=address.split(',')
            state=ax[len(ax)-1]
            if len(ax)==2:
                ay=ax[0].split(' ')
                city=ay[len(ay)-1]
            else:
                city=ax[1]
            city_state=city+','+state
        # create predict record
            predict=Predict()
            predict.date=predictDate
            predict.product=summary.lastProduct
            predict.client_id=client_id
            predict.city_state=city_state

            session.add(predict)
            session.commit()

def IconvDate(externalDate):
    dy = externalDate.split('/')
    if len(dy[0])>2:
        endDate = date(int(dy[0]), int(dy[1]), int(dy[2]))
    else:
        endDate = date(int(dy[2]), int(dy[0]), int(dy[1]))
    return endDate

class CreateExportFiles():
    def run(self):
        session=Session()
        # sort predict file by pickup region
        last_city_state=''
        print('date', 'customer', 'address', 'product')
        for predict in session.query(Predict).order_by(Predict.city_state):
            if predict.city_state!=last_city_state:
                if last_city_state!='':
                    print(predict.city_state)
                last_city_state=predict.city_state
            name=''
            address=''
            for client in session.query(Client).filter(Client.client_id==predict.client_id):
                address=client.address
                name=client.name
            print(predict.date, name, address, predict.product)

        # create csv file