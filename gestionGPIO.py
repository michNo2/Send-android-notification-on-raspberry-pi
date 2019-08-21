#!/usr/bin/python
# -*- coding:Latin-1 -*-

#Ajoute les bibliotèques :
import RPi.GPIO as GPIO
import time


class Gestion_LedRGB_GPIO():
    def __init__(self):
        #Déclare les variables liés au port GPIO, j'utilise la numérotation BOARD (=>électronique) :
        self.r = 18
        self.g = 12
        self.b = 13
        GPIO.setwarnings(False) #Evite d'avoire des warning dans la console lors de l'activation d'une sortie :
        GPIO.setmode(GPIO.BCM) #Mettre board pour utiliser la nuémrotation physique
        #Configure les entrées sorties. Initialise également à l'état bas les sorties
        GPIO.setup(self.r,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.g,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.b,GPIO.OUT,initial=GPIO.LOW)

    #Fonction permetttant d'activer la led RGB. Metrte les différents paramètres à 1 pour activer les différentes couleurs (r->rouge, g->vert, b->bleu)
    #A 0 pour désactiver les couleurs
    #le délay permet d'indiquer combien de temps laissre la led allumé; 
    def activeLed(self,r,g,b,_delay):
        GPIO.output(self.r,r)
        GPIO.output(self.g,g)
        GPIO.output(self.b,b)
        time.sleep(_delay)

    #Fonction permettant de piloter la led RGB en pwm. Les paramètres r,g,b correspondent au rapport cyclique pour piloter chaque couleur
    #A la fin de la fonction la led s'éteint. 
    #Le paramètre _delay permet d'indiquer combien de temps la led reste allumer.
    def activeLedpwm(self,r,g,b,_delay):
        pwm_r=GPIO.PWM(self.r,1000)
        pwm_g=GPIO.PWM(self.g,1000)
        pwm_b=GPIO.PWM(self.b,1000)
        pwm_r.start(r)
        pwm_g.start(g)
        pwm_b.start(b)
        time.sleep(_delay)
        pwm_r.stop()
        pwm_g.stop()
        pwm_b.stop()

    
