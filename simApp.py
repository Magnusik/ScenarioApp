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
import threading


class MedicalScenario(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint=(0.6,0.7)
        self.window.pos_hint={"center_x":0.5,"center_y":0.5}
        
        self.connectArduino
        self.board = Arduino("COM8")
        self.states = ['crying','screaming','whining'] 
        self.scenario = "neutral"
        self.guess ="nothing"
        self.connectguard = True
        # image widget
        self.window.add_widget(Image(source="Laerdal_logo.png"))

        #label widget
        self.greeting = Label(
            text="What do you see?",
            font_size = 18,
            color='#00FFCE'
            )
        self.window.add_widget(self.greeting)
        
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

        return self.window
    
    def ledOn(self,instance):
        new_scenario = self.states.copy()
        if self.scenario == 'neutral':
            self.scenario = np.random.choice(self.states,size=1)
        else:
            new_scenario.remove(self.scenario)
            self.scenario = np.random.choice(new_scenario,size=1)
        
        print(self.scenario)
        if self.scenario == "crying":
            self.board.digital[8].write(1)
            self.board.digital[9].write(0)
            self.board.digital[10].write(0)
            cry_th = threading.Thread(target=self.sound,args=('crying',))
            cry_th.start()
        if self.scenario == "screaming":
            self.board.digital[9].write(1)
            self.board.digital[10].write(0)     
            self.board.digital[8].write(0)
            scream_th = threading.Thread(target=self.sound,args=('screaming',))
            scream_th.start()
        if self.scenario == "whining":
            self.board.digital[8].write(0)
            self.board.digital[9].write(0)
            self.board.digital[10].write(1)
            whining_th = threading.Thread(target=self.sound,args=('whining',))
            whining_th.start()
    
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
    def sound(self,sound):
        if sound == 'crying':
            playsound('C:/Users/NOMKO3/Random_scripts/PythonApp/ScenarioApp/tunes/crying.mp3')
        if sound == 'whining':
            playsound('C:/Users/NOMKO3/Random_scripts/PythonApp/ScenarioApp/tunes/whining.mp3')
        if sound == 'screaming':
            playsound('C:/Users/NOMKO3/Random_scripts/PythonApp/ScenarioApp/tunes/screaming.mp3')
        else: return 0

if __name__ == "__main__":
    MedicalScenario().run()   