from models import engine, Session, Client, Pickup, Summary, Predict
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
    pass

class CreatePredictions():
    pass

class CreateExportFiles():
    pass