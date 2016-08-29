"""
    PHAT-SIM detect activities for sensor Accelerometer
    
    Detect and recognize activity from data collected from sensors.
    SK_DETECT_MOV: recognizes activities from accelerometer data PHAT-SIM
    
    Parameter:
    
        - model: Exist model generate for prediction. Use " -model t "
        - host: host connect to socket client for data sensor read.
        - port: port connect to socket client for data sensor read.
        - activities: Activities to predict with PHAT-SIM classificator. Use " -activities walking,running,stop "
        - taction: Time for to send notifications to user or patient.
        - train: Path for data training.
        - test: Path for data test.
        - sizewin: time window to determine an activity at each instant of prediction.
        
    UCM
    
"""
import time
import sys
import socket as sk
import argparse
import textwrap

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib

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
            - SK_DETECT_MOV: recognizes activities from accelerometer data PHAT-SIM
        '''),
    epilog='''UCM ColoSAAL project 2016'''
)
#parser.add_argument('-normalize','--normalize', help='normalize sample for file ', required=False)
#parser.add_argument('-bestmodel','--bestmodel', help='use best parameter for generate model of prediction ', required=False)
parser.add_argument('-model', '--model', help='exist model generate for prediction (-model t)', required=False)
parser.add_argument('-classificator', '--classificator', help='model of classification applique to prediction of activity (-class AB/RF/KNN/SVC/GB)', required=False)
parser.add_argument('-host', '--host', help='host connect to socket client for data sensor read ', required=False)
parser.add_argument('-port', '--port', help='port connect to socket client for data sensor read ', required=False)
parser.add_argument('-activities', '--activities', help='activities to predict with PHAT-SIM classificator. e.g: walking,drink,run,wait ', required=False)
parser.add_argument('-taction', '--taction', help='time for to send notifications to user or patient ', required=False)
parser.add_argument('-train', '--train', help='path for data training ', required=False)
parser.add_argument('-test', '--test', help='path for data test ', required=False)
parser.add_argument('-sizewin', '--sizewin', help='time window to determine an activity at each instant of prediction  ', required=False)
args = parser.parse_args()

def showErrorException(infoError):
    """ Imprimir errores generados  """
    print ("---> Error::: ", infoError[0])
    print ("---> Error Type::: ", infoError[1])

if __name__ == '__main__':
    print("---> INIT PHAT-SIM Detect ")
    action = saction()
    util = sutil()
    
    #################################################
    #size windows
    sizewin = 9
    if args.sizewin != None:
        sizewin = int(args.sizewin)
    print("---> Set size windows [sizewin=" + str(sizewin) + "]")
    
    #################################################
    #path for data train/test
    path_train = "../data/train"
    path_test = "../data/test"
    
    if args.train != None:
        path_train = args.train
        
    if args.test != None:
        path_test = args.test
    
    print("---> Set path file data train/test [train=" + path_train + ", test= " + path_test + "]")
    
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
        filters = {'drink': 2, 'waveattention': 1, 'stop': 0}
        print("---> Activities self: ", filters)
    else:
        filters = {}
        activities = args.activities.split(",")
        numer_activity = 0
        for activity in activities:
            filters.update({str(activity):int(numer_activity)})
            numer_activity += 1

    #################################################
    # CLASSIFICATION METHOD AB/GB/KNN/SVC/RF
    classificator = "BEST-KNN"
    if args.classificator != None:
        if args.classificator in ['RF', 'KNN', 'GB', 'AB', 'SVC', 'EX']:
            classificator = args.classificator

    #################################################
    # definition and selection of model for training
    if args.model == 't':
        # Se recupera el entrenamiento ya generado, el cual persiste en un fichero fisico
        clf = joblib.load('../models/model_fit-v' + classificator + '001-mcb.pkl')
    else:
        # Se entrena y se define el modelo con los mejores parametros encontrados
        training = dataset(path_train, filters)
        sm = smodel(training.data, training.target)
        clf = sm.get_model(classificator)

        # Se guarda el modelo generado para futuro uso sin fase de entrenamiento previa
        joblib.dump(clf, '../models/model_fit-v' + classificator + '001-mcb.pkl', compress=1)
        print(clf)
        
    # Se testea el modelo creado con los datos de test
    validation = dataset(path_test, filters)
    predicted = clf.predict(validation.data)
    truedata = list(map(lambda x: filters[x], validation.activities))
    precision = precision_score(truedata, predicted, average='macro')
    recall = recall_score(truedata, predicted, average='macro')
    
    print("---> Param Test Predict: Precision = ", precision , ",  Macro recall = ", recall)

    # OPTIONAL::::: write the fit precision to a file.
    ts = time.time()
    record = str(ts) + ", " +  str(precision) + ", " + str(recall) + "\n"
    with open("../logs/precision-fit.csv", "a") as myfile:
        myfile.write(record)

    # OPTIONAL:::: Matrix confusion
    cm = confusion_matrix(truedata, predicted)
    print("---> Matrix Confusion ===>: ")
    print(cm)

    print("---> Best Parameter Classification [", 'best parameter: ', clf.best_estimator_, ", best params: ",clf.best_params_, "]")
    
    #################################################
    # Se lee del Socket los datos del sensor
    host = "localhost"
    port = 60001
    
    if args.host != None:
        host = args.host
        
    if args.port != None:
        port = args.port
    
    print("---> Set parameter socket: [host:'" + host + "', port:" + str(port) + "]")
    ADDR = (str(host), int(port))
    sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    
    #################################################
    # OPTIONAL::: se controla la actividad del sensor (connect or unconnet)
    sw = True

    try:
        sock.connect(ADDR)
    except:
        print("---> [Err initial] No read data from Socket")
        showErrorException(sys.exc_info())
        sw = False

    while True:
        try:
            if sw == False:
                print("---> Reconnect to Socket PHAT-SIM...")
                try:
                    sock.connect(ADDR)
                    sw = True
                except:
                    print ("---> ...Wait Sensor Accelerometer of PHAT-SIM")
                    sw = False
            else:
                print("---> Read Data Sensor...")
                readData = []
                readDataFromSocket = []
                init_register = int(time.time()*1000)
                cgestcount = 0
                
                for data in sock.makefile('r'):
                    if len(data.split(";")) == 7:
                        # Se caupturan los datos del sensor, y se crea un (list:list) con el conjunto de ellos
                        datatmp = data.replace("\n", "")
                        readDataFromSocket = []
                        readDataFromSocket.append(int(time.time()*1000))
                        readDataFromSocket.append(float(data.split(";")[4]))
                        readDataFromSocket.append(float(data.split(";")[5]))
                        readDataFromSocket.append(float(data.split(";")[6]))
                        readData.append(readDataFromSocket)
                    if len(readData) > 102:
                        # 200 lineas de datos se utilizan para analizar y clasificar. 
                        # Se crea instancia de la clase sample_file pero con el objeto buffer
                        sample = sfile(None, readData)
                        sample.keep_last_lines(100)
                        samples = sample.get_samples()
                        pr = clf.predict(samples)
                        text_img = util.get_img(pr, filters, sizewin)
                        print(text_img)
                        print(pr)
                        
                        
        except:
            showErrorException(sys.exc_info())
            sw = False

        time.sleep(1)



