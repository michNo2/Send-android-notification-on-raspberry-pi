#!/usr/bin/python
# -*- coding:Latin-1 -*-

# -- Les programmes threads boutons et notifications physiques sont regroupés dans le prog "gestion GPIO" --

#-------------------------------- FONCTION DU SCRIPT ------------------------------------------------------
#Ce programme permet d'activer une led rgb branché sur le raspberry lorsque une notification est reçu sur le téléphone.
#Ce programme tourne en simultané avec une config "automate" sur le téléphone.
#La led s'allume 2 secondes pour chauqe appli envoyant une notification puis s'éteint 4 secondes;
#Au démarrage de ce script la led clignote 5 fois (en blanc)
#Au démarrage de l'appli sur le téléphone, la led s'allume 5 secondes (en orange)
#lorsque le téléphone est connecté, toutes les 5 minutes (environ) la led s'allume en orange pdt 5 secondes.

#-------------------------------- DETAIL TECHNIQUE SUR LE SCRIPT (à lire avant toute modif notammenent sur les delay)--------------------------------------------
#L'application "automate" d'android est utilisé sur le téléphone pour envoyer des requêtes http à ce script
#Dans "automate :
# On vérifie si une application (messenger, sms, wattsap ou gmail) reçoit une notif                                                                 
# Si une appli recoit une notif :
#  On envoie une requête http au serveur python
#  On bloque le programme 4 secondes
# On vérifie l'appli suivante
# on reboucle
# A chaque boucle un compteur est incrémenté. au bout de 35 boucles (une boucle fait minimum 4 secondes), on envoie une requête http pour indiquer que le téléphone est connecté.
# Lorsqu'une application (messegener, sms, wattsap ou gmail recoit une notif), on envoie une requête http au serveur python. puis on bloque le programme pendant 4 secondes
#Le delay de 4 secondes permet d'éviter à l'appli automate de planter. Lorsqu'on allume une led pendant X secondes on bloque le programme python X secondes. Seulement l'appli automate continue de tourner pendant ces X secondes. Si elle envoie une requête pendant cette période elle ne voit pas de réponse du serveur et plante, en bloquant l'appli autoamte plus longtemps que X il n'y a pas de problème...
#La partie serveur provient d'une librairie toute faite

#Importe les librairies: 
import SimpleHTTPServer
import SocketServer
from gestionGPIO import * #J'ai fait une bibliotèque pour gérer la led RGB car elle me sert pour d'autres scripts...

#Déclaration des variables liées au serveur:
PORT = 46005 #Port utilisé par automate  pour accéder au serveu
ledGPIO = Gestion_LedRGB_GPIO()

#Classe du serveur :
class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
 
    #Réception du header:
    def do_GET(self):
        logging.error(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
    
    #Réception du post:
    def do_POST(self):
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)                 
        request_path = self.path        
        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0        
        pdata=self.rfile.read(length)
        b_postconnu=False
        #Réception d'une requpête de k'appli automate :
        if(pdata=="mail"):
            #Réception d'un mail, allume la led en violet" :
            ledGPIO.activeLed(1,0,1,2)
            b_postconnu=True
        if(pdata=="whatsapp"):
            #Réception d'une notif wattsap, active la led verte:
            ledGPIO.activeLed(0,1,0,2)  
            b_postconnu=True
        if(pdata=="messenger"):
            #Réception d'une notif messenger, active la led bleu clair:
            ledGPIO.activeLed(0,1,1,2)  
            b_postconnu=True
        if(pdata=="sms"):
            #Réception d'un sms, active la led violette::
            ledGPIO.activeLed(1,1,1,2)
            b_postconnu=True
        if(pdata=="verif"):
            #L'appli envoi une commande pour vérifier si le programme tourne,activation de la led en orange :
            ledGPIO.activeLedpwm(75,12,1,5)
            b_postconnu=True
        #Enregistrements des reqûetess inconnus dans un fichier de log :
        if b_postconnu==False:
            fichier = open("log_notif.txt","a")
            fichier.write("Réception d'un post inconnu :\n")
            fichier.write(str(request_headers)+str(request_path)+pdata+"\n\n")
            #fichier.write(str(request_path))
            fichier.close()
        #Eteint les leds :
        ledGPIO.activeLed(0,0,0,0.01)             

#Démarre le serveur
Handler = ServerHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
#Au debut du programme allume la led en blanc : 
for i in range(5):    
    ledGPIO.activeLed(1,1,1,0.2)
    ledGPIO.activeLed(0,0,0,0.05)
#Active la surveillance de requêtes sur le serveur
httpd.serve_forever()
