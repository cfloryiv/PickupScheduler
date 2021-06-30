from models import engine, Session, Client, Pickup, Summary, Predict
from datetime import date, timedelta
import csv

class ImportInputFiles():

    def run(self, filename):

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
                # print(row)

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
                datex=IconvDate(row[0])
                pickup.date=datex.isoformat()
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
                    summary.lastDate=pickup.date
                    summary.lastProduct=pickup.product

                summary.numberPickups+=1
                if (pickup.date)>=(summary.lastDate):
                    summary.lastDate=pickup.date
                    summary.lastProduct=pickup.product
                if (pickup.date)<(summary.startDate):
                    summary.startDate=pickup.date
                session.add(summary);
                session.commit()

        session.query(Pickup).filter(Pickup.updated==False).update({Pickup.updated: True})
        session.commit()

            # update summary record

class CreatePredictions():

    def run(self):

        session=Session()

        # clear prediction file

        session.query(Predict).delete()
        session.commit()

        # select summary record

        for summary in session.query(Summary):

            # read in client record

            client_id=summary.client_id
            for client in session.query(Client).filter(Client.client_id==client_id):
                address=client.address

            # determine new predict date

            startDate=IconvDate(summary.startDate)
            endDate=IconvDate(summary.lastDate)
            aveDays=(endDate-startDate)/summary.numberPickups
            numberDays=endDate-startDate

            # wait at least 21 days until the next pickup

            minDays=timedelta(days=14)
            if aveDays<minDays:
                days=minDays
            else:
                days=aveDays
            predictDate=(endDate+days).isoformat()

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
            predict.days=days.days
            predict.numberDays=numberDays.days
            predict.aveDays=aveDays.days

            session.add(predict)
            session.commit()

def IconvDate(externalDate):

    dy = externalDate.split('/')
    if len(dy)==1:
        dy=externalDate.split('-')

    if len(dy[0])>2:
        endDate = date(int(dy[0]), int(dy[1]), int(dy[2]))
    else:
        endDate = date(int(dy[2]), int(dy[0]), int(dy[1]))

    return endDate

class CreateExportFiles():

    def run(self):
        filename='pickup.csv'
        with open(f'C:\\users\\cflor\\BB\\outputFiles\\{filename}', 'w', newline='') as csvfile:
            fieldnames = ['date', 'name', 'address', 'product', 'days', 'numberDays', 'aveDays']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            session=Session()

            # sort predict file by pickup region

            last_city_state=''


            for predict in session.query(Predict).order_by(Predict.city_state):

                if predict.city_state!=last_city_state:
                    writer.writerow({'date': predict.city_state})
                    last_city_state=predict.city_state

                name=''
                address=''

                for client in session.query(Client).filter(Client.client_id==predict.client_id):
                    address=client.address
                    name=client.name


                writer.writerow({'date': predict.date, 'name': name,
                                 'address': address, 'product': predict.product,
                                 'days': predict.days, 'numberDays': predict.numberDays,
                                 'aveDays': predict.aveDays})
            # create csv file