from busRules import ImportInputFiles, ProcessPickups, CreatePredictions, CreateExportFiles, ImportMergePurge
import os
from pathlib import Path



if __name__ == '__main__':

    importMergePurge=ImportMergePurge()
    importMergePurge.run()

    importInputFiles=ImportInputFiles()
    dirpath='C:\\users\\cflor\\BB\\inputFiles'
    paths = sorted(Path(dirpath).iterdir(), key=os.path.getmtime)

    #for file in os.scandir('C:\\users\\cflor\\BB\\inputFiles'):
    for file in paths:
        importInputFiles.run(file.name)

    processPickups=ProcessPickups()
    processPickups.run()

    createPredictions=CreatePredictions()
    createPredictions.run()

    createExportFiles=CreateExportFiles()
    createExportFiles.run()
