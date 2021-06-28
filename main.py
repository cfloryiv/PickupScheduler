from busRules import ImportInputFiles, ProcessPickups, CreatePredictions, CreateExportFiles


if __name__ == '__main__':
    ImportInputFiles.run('Lussier Wholesale Pickups.csv')
    processPickups=ProcessPickups()
    processPickups.run()
    createPredictions=CreatePredictions()
    createPredictions.run()
    createExportFiles=CreateExportFiles()
    createExportFiles.run()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
