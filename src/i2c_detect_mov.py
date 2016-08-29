"""
    PHAT-SIM detect activities for sensor Accelerometer
    
    Detect and recognize activity from data collected from sensors.
    I2C_DETECT_MOV: recognizes activities from accelerometer data I2C port BEAGLEBONE
    
    Parameter:
    
        - model: Exist model generate for prediction. Use " -model t "
        - activities: Activities to predict with PHAT-SIM classificator. Use " -activities walking,running,stop "
        - taction: Time for to send notifications to user or patient.
        - train: Path for data training.
        - test: Path for data test.
        - sizewin: time window to determine an activity at each instant of prediction.
        
    UCM
    
"""
import time, sys
import argparse
import textwrap

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib

from lib.readi2c import ReadI2CPort as rsp
from lib.sfile import sfile
from lib.sfile import dataset
from lib.smodel import smodel
from lib.sutil import sutil
from lib.saction import saction 

parser = argparse.ArgumentParser(
    formatter_class = argparse.RawDescriptionHelpFormatter, 
    description = textwrap.dedent('''\
        PHAT-SIM detect activities for sensor Accelerometer
        --------------------------------
        Detect and recognize activity from data collected from sensors.
            - I2C_DETECT_MOV: recognizes activities from accelerometer data I2C port BEAGLEBONE
        '''),
    epilog='''UCM ColoSAAL project 2016'''
)
parser.add_argument('-model','--model', help='exist model generate for prediction (-model t)', required=False)
parser.add_argument('-activities','--activities', help='activities to predict with PHAT-SIM classificator. e.g: walking,drink,run,wait ', required=False)
parser.add_argument('-taction','--taction', help='time for to send notifications to user or patient ', required=False)
parser.add_argument('-train','--train', help='path for data training ', required=False)
parser.add_argument('-test','--test', help='path for data test ', required=False)
parser.add_argument('-sizewin','--sizewin', help='time window to determine an activity at each instant of prediction  ', required=False)
parser.add_argument('-delay','--delay', help='delay time, wait between read data from i2c port, default 1 miliseconds ', required=False)
args = parser.parse_args()

def showErrorException(infoError):
    """ Imprimir errores generados """
    print ("---> Error::: ", infoError[0])
    print ("---> Error Type::: ", infoError[1])
    
if __name__ == '__main__':
    print("---> INIT PHAT-SIM BeagleBone Detect ")
    action = saction()
    util = sutil()
    
    #################################################
    #size windows
    sizewin = 9
    if args.sizewin != None:
        sizewin = int(args.sizewin)
    print("---> Set size windows [sizewin=" + str(sizewin)  + "]")
    
    #################################################
    #path for data train/test
    path_train = "../data/train"
    path_test = "../data/test"
    delay = 0
    
    if args.train != None:
        path_train = args.train
        
    if args.test != None:
        path_test = args.test
        
    if args.delay != None:
        delay = float(args.delay)

    print("---> Set path file data train/test [train=" + path_train  + ", test= " + path_test  + ", delay=" + str(delay) + "]")
    
    #################################################
    #time to send notifications to user or patient
    taction = 20000
    tdefault = "default"
    if args.taction != None:
        try:
            taction = int(args.taction)*1000
            tdefault = ""
        except:
            out = ""
    print("---> Set time action " + tdefault + "=" + str(taction))
    
    
    #################################################
    # SELF activities base from classificator
    if args.activities == None:
        filters = {'fall':3,'drink':2,'waveattention':1,'stop':0}
        print("---> Activities self: ", filters)
    else:
        filters = {}
        activities = args.activities.split(",")
        numer_activity = 0
        for activity in activities:
            filters.update({str(activity):int(numer_activity)})
            numer_activity += 1
    
    
    #################################################
    # definition and selection of model for training
    if args.model == 't':
        # Se recupera el entrenamiento ya generado, el cual persiste en un fichero fisico
        clf = joblib.load('../models/model_fit-vRF001-mcb.pkl')
    else:
        # Se entrena y se define el modelo con los mejores parametros encontrados
        training = dataset(path_train, filters)
        sm = smodel(training.data, training.target)
        clf = sm.get_model("KNN")
        
        # Se guarda el modelo generado para futuro uso sin fase de entrenamiento previa
        joblib.dump(clf, '../models/model_fit-vRF001-mcb.pkl')
        print (clf)
        
    # Se testea el modelo creado con los datos de test
    validation = dataset(path_test, filters)
    predicted = clf.predict(validation.data)
    truedata = list(map(lambda x: filters[x], validation.activities))
    precision = precision_score(truedata, predicted, average='macro')
    recall = recall_score(truedata, predicted, average='macro')
    
    print("---> Param Test Predict [predicted = ", predicted, " truedata  = ", truedata, " macro precision = ", precision , " macro recall = ", recall, "]")

    # OPTIONAL::::: write the fit precision to a file.
    ts = time.time()
    record = str(ts) + ", " +  str(precision) + ", " +  str(recall) + "\n"
    with open("../logs/precision-fit.csv", "a") as myfile:
        myfile.write(record)

    # OPTIONAL:::: Matrix confusion
    cm = confusion_matrix(truedata, predicted)
    print("---> Matrix Confusion ===>: ")
    print(cm)

    print("---> Best Parameter Classification [", 'best parameter: ', clf.best_estimator_, ", best params: ",clf.best_params_, "]")
    
    #################################################
    print ("---> Read Accelerometer")
    # OPTIONAL::: se controla la actividad del sensor (connect or unconnet)
    sw_rsp = True
    
    # READ SENSOR OF BEAGLEBONE::: read data accelerometer 
    try:
        i2c_rsp = rsp()
    except:
        print("---> [Err initial] No read data from beaglebone...")
        showErrorException(sys.exc_info())
        sw_rsp = False
    
    while True:
        try:
            if sw_rsp == False:
                print("---> Reconnect to I2C Port BBx...")
                try:
                    i2c_rsp = rsp()
                    sw_rsp = True
                except:
                    print("---> [Err] No read data from port I2C from beaglebone")
                    showErrorException(sys.exc_info())
                    sw_rsp = False
            else:
                print( "---> Read Data i2c from beaglebone...")
                readData = []
                classifiedSoFar=[]
                readDataFromSocket = []
                init_register = int(time.time()*1000)
                cgestcount = 0

                while True:
                    data = i2c_rsp.getAxes(True)
                    if data != None:
                        readDataFromSocket = []
                        readDataFromSocket.append(int(time.time()*1000))
                        readDataFromSocket.append(float(data["x"]))
                        readDataFromSocket.append(float(data["y"]))
                        readDataFromSocket.append(float(data["z"]))
                        readData.append(readDataFromSocket)
                    if (len(readData) > 200):
                        # 200 lineas de datos se utilizan para analizar y clasificar. 
                        # Se crea instancia de la clase sample_file pero con el objeto buffer
                        sample = sfile(None, readData)
                        sample.keep_last_lines(50)
                        samples = sample.get_samples()
                        pr = clf.predict(samples)
                        text_img = util.get_img(pr, filters, sizewin)
                        print(text_img)
                        print (pr)
                        cgestcount, init_register = action.toMedicament(pr,int(time.time()*1000), cgestcount, init_register, taction, filters)
                    time.sleep(delay)
                        
        except:
            showErrorException(sys.exc_info())
            sw_rsp = False

        time.sleep(1)



