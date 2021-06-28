from models import engine, Session, Client, Pickup, Summary, Predict
import csv

class ImportInputFiles():
    def run(filename):
        print('importing ', filename)
        with open(f'C:\\users\\cflor\\BB\\inputFiles\\{filename}') as file:
            reader=csv.reader(file)
            for row in reader:
                print(row)
        return

class ProcessPickups():
    pass

class CreatePredictions():
    pass

class CreateExportFiles():
    pass