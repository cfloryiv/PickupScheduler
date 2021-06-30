from busRules import ImportInputFiles, ProcessPickups, CreatePredictions, CreateExportFiles
import os

if __name__ == '__main__':
    importInputFiles=ImportInputFiles()
    for file in os.scandir('C:\\users\\cflor\\BB\\inputFiles'):
        importInputFiles.run(file.name)

    processPickups=ProcessPickups()
    processPickups.run()

    createPredictions=CreatePredictions()
    createPredictions.run()

    createExportFiles=CreateExportFiles()
    createExportFiles.run()
