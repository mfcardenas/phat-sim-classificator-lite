"""
    Class Action
    UCM
"""
import os

class saction:
    def __init__(self):
        """ Init class Action """
        self.activity = ''
        
    def toMedicament(self, predict, time, cgestcount, init_register, taction, filters):
        """ To Medicament set Notifications """
        results = str(predict).replace("[", "").replace("]", "").split(" ")
        
        for activity, number in filters.items():
            if 'drink' == activity:
                if number in results[-10:]:
                    cgestcount += 1
        
        if time - init_register > taction: 
            if cgestcount == 0:
                os.system(' python lib/smedicament.py &')
                init_register = time
                cgestcount = 0

        return cgestcount, init_register
    
    def toRunning(self, predict, time, cgestcount, init_register, taction):
        """ To Running set Notifications """
        results = str(predict).replace("[", "").replace("]", "").split(" ")
        
        