import threading
import time
from playsound import playsound
import serial
from pyfirmata import Arduino, util
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from random import randint
import numpy as np
from functools import partial


class MedicalScenario(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint=(0.6,0.7)
        self.window.pos_hint={"center_x":0.5,"center_y":0.5}
        
        self.connectArduino
        self.board = Arduino("COM8")
        self.states = ['crying','screaming','whining','dead'] 
        self.scenario = "neutral"
        self.guess ="nothing"
        self.connectguard = True
        # image widget
        self.window.add_widget(Image(source="bacon.png"))

        #label widget
        self.greeting = Label(
            text="What do you see?",
            font_size = 18,
            color='#00FFCE'
            )
        self.window.add_widget(self.greeting)

        #text input widget
        # self.user = TextInput(
        #     multiline = False,
        #     padding_y = (20,20),
        #     size_hint = (1,0.5)
        #     )
        # self.window.add_widget(self.user)
        
        #button widgets
        
        self.buttonScenario = Button(
            text="Start Scenario",
            size_hint = (1,0.5),
            bold = True,
            background_color = "#0000FF"
            )
        self.buttonScenario.bind(on_press=self.ledOn)
        self.window.add_widget(self.buttonScenario)

        self.buttonScreaming = Button(
            text = "Screaming",
            size_hint = (1,0.5),
            bold = True,
            background_color = "#00FFCE"
            )
        self.buttonScreaming.bind(on_press=partial(self.changeState,bvalue='screaming'))
        self.window.add_widget(self.buttonScreaming)
        
        self.buttonCrying = Button(
            text="Crying",
            size_hint = (1,0.5),
            bold = True,
            background_color = "#00FFCE"
            )
        self.buttonCrying.bind(on_press=partial(self.changeState, bvalue ='crying'))
        self.window.add_widget(self.buttonCrying)

        self.buttonWhining = Button(
            text="Whining",
            size_hint = (1,0.5),
            bold = True,
            background_color = "#00FFCE"
            )
        self.buttonWhining.bind(on_press=partial(self.changeState, bvalue ='whining'))
        self.window.add_widget(self.buttonWhining)
        
        self.buttonDead = Button(
            text="Dead",
            size_hint = (1,0.5),
            bold = True,
            background_color = "#00FFCE"
            )
        self.buttonDead.bind(on_press=partial(self.changeState, bvalue ='dead'))
        self.window.add_widget(self.buttonDead)

        return self.window
    
    def startLedShow(self,instance):
        board = Arduino("COM8")
        iterator = util.Iterator(board)
        iterator.start()
        valve_pin8 = board.get_pin("d:9:p")
        while True:
            board.digital[9].write(1)
            time.sleep(4)
            board.digital[9].write(0)
            time.sleep(1)
    
    def ledOn(self,instance):
        self.scenario = np.random.choice(self.states,size=1)
        print(self.scenario)
        if self.scenario == "crying":
            self.board.digital[8].write(1)
            self.board.digital[9].write(0)
            self.board.digital[10].write(0)
            playsound('C:/Users/NOMKO3/Random_scripts/PythonApp/ScenarioApp/tunes/crying.mp3')
        if self.scenario == "screaming":
            self.board.digital[9].write(1)
            self.board.digital[10].write(0)     
            self.board.digital[8].write(0)
            playsound('C:/Users/NOMKO3/Random_scripts/PythonApp/ScenarioApp/tunes/screaming.mp3')
        if self.scenario == "whining":
            self.board.digital[8].write(0)
            self.board.digital[9].write(0)
            self.board.digital[10].write(1)
            playsound('C:/Users/NOMKO3/Random_scripts/PythonApp/ScenarioApp/tunes/whining.mp3')
    
    def ledClear(self,instance):
        self.board.digital[8].write(0)
        self.board.digital[9].write(0)
        self.board.digital[10].write(0)
    
    def connectArduino():
            board = Arduino("COM8")
            iterator = util.Iterator(board)
            iterator.start()
            ledPin3 = board.get_pin("d:10:o")
            ledPin2 = board.get_pin("d:9:o")
            ledPin1 = board.get_pin("d:8:o")

    def callback(self,instance):
        self.greeting.text = "Hello " + self.user.text + "!",
        print(self.scenario)
    def changeState(self,instance,bvalue):
        if bvalue == "dead":
            self.guess="dead"
            print(self.guess)
        if bvalue == "screaming":
            self.guess="screaming"
            print(self.guess)
        if bvalue == "whining":
            self.guess="whining"
            print(self.guess)
        if bvalue == "crying":
            self.guess="crying"
            print(self.guess)
        
        checkAnswer =self.answerGuess()
        if checkAnswer:
            self.correctCallBack()
        else:
            self.wrongCallBack()



    def  answerGuess(self):
        guess = self.guess
        checkAnswer = self.scenario
        print('test')
        if guess == checkAnswer:
            return True
        else:
            return False

    def correctCallBack(self):
        self.greeting.color='#00FFCE'
        self.greeting.text = "Correct!"

    def wrongCallBack(self):
        self.greeting.color='#FF0000'
        self.greeting.text = "Wrong!"
if __name__ == "__main__":
    MedicalScenario().run()

## unbind all in scenario button
# import time
# from pyfirmata import Arduino, util

# board = Arduino("COM10")

# iterator = util.Iterator(board)
# iterator.start()

# valve_pin8 = board.get_pin("d:9:p")

# while True:
#     board.digital[9].write(1)
#     #valve_pin8.write(1)
#     time.sleep(4)
#     board.digital[9].write(0)
#     #valve_pin8.write(0)
#     time.sleep(1)

"""
Based on the 1s-pulse.py. See python-EK-M-015-main/1s-pulse.py for explaination of serial functions.
To use this with an Arduino Uno, you must first upload the StandardFirmata sketch from Arduino.
This can be found in File -> Examples -> Firmata.
"""

# import threading
# import time
# import serial
# import time
# from playsound import playsound
# from pyfirmata import Arduino, util

# rapid_breath = True

# board = Arduino("COM9")

# iterator = util.Iterator(board)
# iterator.start()

# valve_pin7 = board.get_pin("d:7:o")
# valve_pin8 = board.get_pin("d:8:o")
# motor_pin2 = board.get_pin("d:2:o")
# motor_pin3 = board.get_pin("d:3:o")

# ventus_port = serial.Serial(port="COM8",
#                             baudrate=115200,
#                             bytesize=8,
#                             timeout=2,
#                             stopbits=serial.STOPBITS_ONE)
# ventus_port.write(b"#W2,0\n")
# ventus_port.write(b"#W0,0\n")
# ventus_port.write(b"#W10,0\n")
# ventus_port.write(b"#W11,0\n")

# if rapid_breath:
#     ventus_port.write(b"#W23,1000\n")
# else:
#     ventus_port.write(b"#W23,100\n")

# def digitalWrite(pin, value):
#     if pin == 8:
#         valve_pin8.write(value)
#     elif pin == 7:
#         valve_pin7.write(value)
#     elif pin == 3:
#         motor_pin3.write(value)
#     elif pin == 2:
#         motor_pin2.write(value)

# def write_pump(value):
#     if value == 1:
#         ventus_port.write(b"#W0,1\n")
#     else:
#         ventus_port.write(b"#W0,0\n")

# def play_sound(filepath):
#     playsound(filepath)

# while True:
#     if rapid_breath:
#         breath_path = "C:\\Users\\NOLEL1\\Documents\\LaerdalSkinRetractions\\breathing_sounds\\08INNpust.mp3"
#         #valve_8_inhale = threading.Thread(target=digitalWrite,args=(8,1,))
#         valve_7_inhale = threading.Thread(target=digitalWrite,args=(7,1,))
#         #motor_3_inhale = threading.Thread(target=digitalWrite,args=(3,1))
#         #motor_2_inhale = threading.Thread(target=digitalWrite,args=(2,0))
#         pump_inhale = threading.Thread(target=write_pump,args=(1,))
#         sound_inhale = threading.Thread(target=play_sound,args=(breath_path,))

#         #valve_8_inhale.start()
#         valve_7_inhale.start()
#         #motor_3_inhale.start()
#         #motor_2_inhale.start()
#         pump_inhale.start()
#         sound_inhale.start()

#         time.sleep(1.1)
#         #valve_8_inhale.join()
#         valve_7_inhale.join()
#         #motor_3_inhale.join()
#         #motor_2_inhale.join()
#         pump_inhale.join()
#         sound_inhale.join()

#         breath_path = "C:\\Users\\NOLEL1\\Documents\\LaerdalSkinRetractions\\breathing_sounds\\08UTpust.mp3"
        
#         valve_8_exhale = threading.Thread(target=digitalWrite,args=(8,0,))
#         valve_7_exhale = threading.Thread(target=digitalWrite,args=(7,0,))
#         #motor_3_exhale = threading.Thread(target=digitalWrite,args=(3,0))
#         #motor_2_exhale = threading.Thread(target=digitalWrite,args=(2,1))
#         pump_exhale = threading.Thread(target=write_pump,args=(0,))
#         sound_exhale = threading.Thread(target=play_sound,args=(breath_path,))

#         #valve_8_exhale.start()
#         valve_7_exhale.start()
#         #motor_3_exhale.start()
#         #motor_2_exhale.start()
#         pump_exhale.start()
#         sound_exhale.start()

#         time.sleep(0.9)
#         #valve_8_exhale.join()
#         valve_7_exhale.join()
#         #motor_3_exhale.join()
#         #motor_2_exhale.join()
#         pump_exhale.join()
#         sound_exhale.join()

#     else:
#         breath_path = "C:\\Users\\NOLEL1\\Documents\\LaerdalSkinRetractions\\breathing_sounds\\12INNpust.mp3"
#         #valve_8_inhale = threading.Thread(target=digitalWrite,args=(8,1,))
#         valve_7_inhale = threading.Thread(target=digitalWrite,args=(7,1,))
#         #motor_3_inhale = threading.Thread(target=digitalWrite,args=(3,1))
#         #motor_2_inhale = threading.Thread(target=digitalWrite,args=(2,0))
#         pump_inhale = threading.Thread(target=write_pump,args=(1,))
#         sound_inhale = threading.Thread(target=play_sound,args=(breath_path,))

#         #valve_8_inhale.start()
#         valve_7_inhale.start()
#         #motor_3_inhale.start()
#         #motor_2_inhale.start()
#         pump_inhale.start()
#         sound_inhale.start()

#         time.sleep(2)
#         #valve_8_inhale.join()
#         valve_7_inhale.join()
#         #motor_3_inhale.join()
#         #motor_2_inhale.join()
#         pump_inhale.join()
#         sound_inhale.join()

#         breath_path = "C:\\Users\\NOLEL1\\Documents\\LaerdalSkinRetractions\\breathing_sounds\\12Utpust.mp3"
        
#         #valve_8_exhale = threading.Thread(target=digitalWrite,args=(8,0,))
#         valve_7_exhale = threading.Thread(target=digitalWrite,args=(7,0,))
#         #motor_3_exhale = threading.Thread(target=digitalWrite,args=(3,0))
#         #motor_2_exhale = threading.Thread(target=digitalWrite,args=(2,1))
#         pump_exhale = threading.Thread(target=write_pump,args=(0,))
#         sound_exhale = threading.Thread(target=play_sound,args=(breath_path,))

#         #valve_8_exhale.start()
#         valve_7_exhale.start()
#         #motor_3_exhale.start()
#         #motor_2_exhale.start()
#         pump_exhale.start()
#         sound_exhale.start()

#         time.sleep(2)
#         #valve_8_exhale.join()
#         valve_7_exhale.join()
#         #motor_3_exhale.join()
#         #motor_2_exhale.join()
#         pump_exhale.join()
#         sound_exhale.join()