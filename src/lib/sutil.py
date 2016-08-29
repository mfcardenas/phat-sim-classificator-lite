"""
    Class Utilities
    UCM
"""
from scipy.stats import mode

class sutil:
    def __init__(self):
        """ Init class Utilities  """
        self.img_drink = '''                                                                                                          
                `++++++:         +++++++;        '+++      +++.    +++      ++++   `++++;
                .@@@@@@@@@       @@@@@@@@@@      #@@@      @@@@    @@@      @@@@   @@@@# 
                .@@@@@@@@@#      @@@@@@@@@@;     #@@@      @@@@@   @@@      @@@@  @@@@#  
                .@@@   @@@@      @@@#   @@@@     #@@@      @@@@@,  @@@      @@@@ @@@@#   
                .@@@   `@@@.     @@@#   @@@#     #@@@      @@@@@@  @@@      @@@@@@@@@    
                .@@@    @@@'     @@@@@@@@@@      #@@@      @@@@@@@ @@@      @@@@@@@@@    
                .@@@    @@@+     @@@@@@@@@`      #@@@      @@@`@@@;@@@      @@@@@@@@@`   
                .@@@    @@@'     @@@@+@@@#       #@@@      @@@`.@@@@@@      @@@@@@@@@@   
                .@@@   .@@@`     @@@# +@@@+      #@@@      @@@` @@@@@@      @@@@@ #@@@'  
                .@@@``;@@@@      @@@#  @@@@      #@@@      @@@`  @@@@@      @@@@   @@@@  
                .@@@@@@@@@,      @@@#  :@@@@     #@@@      @@@`  `@@@@      @@@@   #@@@@ 
                .@@@@@@@@.       @@@#   @@@@     #@@@      @@@`   @@@@      @@@@    @@@@`
                '''
        
        self.img_waveatten = ''''
                '+++   +++.  ,+++        ++++        +++'     +++'    ++++++++++
                .@@@   @@@@  @@@@       +@@@@        @@@@    .@@@     @@@@@@@@@@
                 @@@  #@@@@  @@@+       @@@@@@       :@@@    @@@@     @@@@@@@@@@
                 @@@. @@@@@  @@@`       @@@@@@        @@@'   @@@;     @@@@      
                 @@@# @@@@@' @@@       @@@;@@@.       @@@@   @@@      @@@@      
                 ;@@@,@@:@@@,@@@       @@@ +@@@       `@@@  #@@@      @@@@@@@@@@
                  @@@@@@ @@@#@@@      ,@@@  @@@        @@@: @@@.      @@@@@@@@@@
                  @@@@@@ +@@@@@:      @@@#  @@@'       #@@@ @@@       @@@@      
                  @@@@@@  @@@@@       @@@@@@@@@@        @@@+@@@       @@@@      
                  @@@@@`  @@@@@      +@@@@@@@@@@        @@@@@@        @@@@``````
                  .@@@@   @@@@@      @@@@````@@@#       ,@@@@@        @@@@@@@@@@
                   @@@@   ,@@@+      @@@`    @@@@        @@@@'        @@@@@@@@@@
                '''
        self.img_fall = '''                                                           
                   @@@@@@@@@`       :@@@@         @@@'          @@@@       
                   @@@@@@@@@`       @@@@@'        @@@'          @@@@       
                   @@@@             @@@@@@        @@@'          @@@@       
                   @@@@            +@@#@@@        @@@'          @@@@       
                   @@@@####'       @@@ @@@@       @@@'          @@@@       
                   @@@@@@@@+       @@@ `@@@       @@@'          @@@@       
                   @@@@@@@@+      @@@@  @@@.      @@@'          @@@@       
                   @@@@           @@@@@@@@@@      @@@'          @@@@       
                   @@@@          ,@@@@@@@@@@      @@@'          @@@@       
                   @@@@          @@@@@@@@@@@;     @@@@@@@@@     @@@@@@@@@@ 
                   @@@@          @@@:    @@@@     @@@@@@@@@     @@@@@@@@@@ 
                   @@@@         '@@@     +@@@     @@@@@@@@@     @@@@@@@@@@ 
                '''
        self.img_stop = '''
                     ,,`                            `,.                    
                  #@@@@@@@      @@@@@@@@@@@       @@@@@@@.       @@@@@@@@@ 
                 '@@@@@@@@+     @@@@@@@@@@@      @@@@@@@@@;      @@@@@@@@@@
                 @@@:  @@@@     @@@@@@@@@@@     @@@@' :@@@@      @@@@  #@@@
                 @@@@:             '@@@         @@@;    @@@;     @@@@   @@@
                 +@@@@@@@          '@@@        ;@@@     @@@@     @@@@  @@@@
                  #@@@@@@@;        '@@@        +@@@     @@@@     @@@@@@@@@@
                    ;@@@@@@        '@@@        '@@@     @@@@     @@@@@@@@@ 
                  .,   '@@@.       '@@@        .@@@     @@@#     @@@@      
                 @@@`   @@@        '@@@         @@@@   #@@@      @@@@      
                 @@@@':@@@@        '@@@         +@@@@@@@@@@      @@@@      
                  @@@@@@@@`        '@@@          #@@@@@@@@       @@@@      
                   +@@@@'          '@@@            #@@@@`        @@@@      
                '''
        
        self.img_none = '''
                            `,.           .,            ,,           `,.       
                  #@@@@@@       @@@@@@,      `@@@@@@       #@@@@@@     
                 :@@@@@@@#     @@@@@@@@      @@@@@@@@     :@@@@@@@#    
                 @@@+ ;@@@     @@@  @@@+    '@@@  @@@     @@@+ ;@@@    
                 :+@  '@@@     ;#@  @@@'    .'@:  @@@     :+@  '@@@    
                     +@@@.         @@@@         `@@@@         +@@@.    
                    #@@@,         @@@@         `@@@@         #@@@,     
                    @@@          '@@@          @@@+          @@@       
                    @@@          @@@,          @@@           @@@       

                   ,@@@          @@@'          @@@          ,@@@       
                   ,@@@          @@@'          @@@          ,@@@       
                   ,@@@          @@@'          @@@          ,@@@       
                    '''
        
        self.img_walk = '''
                '+++   +++.  ,+++        ++++         +++:          ++++   `++++;
                .@@@   @@@@  @@@@       +@@@@         @@@'          @@@@   @@@@#
                 @@@  #@@@@  @@@+       @@@@@@        @@@'          @@@@  @@@@# 
                 @@@. @@@@@  @@@`       @@@@@@        @@@'          @@@@ @@@@#  
                 @@@# @@@@@' @@@       @@@;@@@.       @@@'          @@@@@@@@@   
                 ;@@@,@@:@@@,@@@       @@@ +@@@       @@@'          @@@@@@@@@   
                  @@@@@@ @@@#@@@      ,@@@  @@@       @@@'          @@@@@@@@@`  
                  @@@@@@ +@@@@@:      @@@#  @@@'      @@@'          @@@@@@@@@@  
                  @@@@@@  @@@@@       @@@@@@@@@@      @@@'          @@@@@ #@@@' 
                  @@@@@`  @@@@@      +@@@@@@@@@@      @@@@#####     @@@@   @@@@ 
                  .@@@@   @@@@@      @@@@````@@@#     @@@@@@@@@     @@@@   #@@@@
                   @@@@   ,@@@+      @@@`    @@@@     @@@@@@@@@     @@@@    @@@@`
                '''
        
    def get_str_img(self, activity):
        """ Get string Image  """
        if activity == 'stop':
            return self.img_stop
        
        if activity == 'fall':
            return self.img_fall
        
        if activity == 'drink':
            return self.img_drink
        
        if activity == 'waveattention':
            return self.img_waveatten
        
        if activity == 'walk':
            return self.img_walk
        
        return self.img_none;
        
    
    def get_img(self, predict, filters, sizewin):
        """ Get Image  """
        text_img = self.img_none
        results = str(predict).replace("[", "").replace("]", "").split(" ")
        mode_ = int(mode(results[-sizewin:])[0][0])
        for activity, number in filters.items():
            if number == mode_:
                text_img = self.get_str_img(activity)
        return text_img