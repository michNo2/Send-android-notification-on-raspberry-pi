# Send-android-notification-on-raspberry-pi
Active une led RGB sur un raspberry pi lors de la réception d'un message sur votre téléphone 


- FONCTION DU SCRIPT :
Ce programme permet d'activer une led rgb branché sur le raspberry lorsque une notification est reçu sur le téléphone.
Il y a deux parties :
 Un script python qui tourne sur le raspberrt
 Une configuration de l'application qui tourne sur le téléphone
 
La led s'allume 2 secondes pour chauqe appli envoyant une notification puis s'éteint 4 secondes;
Au démarrage de ce script la led clignote 5 fois (en blanc)
Au démarrage de l'appli sur le téléphone, la led s'allume 5 secondes (en orange)
lorsque le téléphone est connecté, toutes les 5 minutes (environ) la led s'allume en orange pdt 5 secondes.

- DETAIL TECHNIQUE SUR LE SCRIPT :
L'application "automate" d'android est utilisé sur le téléphone pour envoyer des requêtes http à ce script
Dans "automate :
On vérifie si une application (messenger, sms, wattsap ou gmail) reçoit une notif                                                                 
Si une appli recoit une notif :
  On envoie une requête http au serveur python
  On bloque le programme 4 secondes
  On vérifie l'appli suivante
  on reboucle
A chaque boucle un compteur est incrémenté. au bout de 35 boucles (une boucle fait minimum 4 secondes), on envoie une requête http pour indiquer que le téléphone est connecté.
Lorsqu'une application (messegener, sms, wattsap ou gmail recoit une notif), on envoie une requête http au serveur python. puis on bloque le programme pendant 4 secondes
Le delay de 4 secondes permet d'éviter à l'appli automate de planter. Lorsqu'on allume une led pendant X secondes on bloque le programme python X secondes. Seulement l'appli automate continue de tourner pendant ces X secondes. Si elle envoie une requête pendant cette période elle ne voit pas de réponse du serveur et plante, en bloquant l'appli autoamte plus longtemps que X il n'y a pas de problème...
La partie serveur provient de la libraiire simpleHTTPServer

**********************************************************************
SCRIPT FUNCTION :

Allows you to activate a rgb led connected to the raspberry when a notification is received on the phone.
There are two parts to this program.
  A python script that runs on the raspberry
  A configuration of the "automate" application running on an android phone.

The led lights up 2 seconds for each app sending a notification then goes off for 4 seconds;
At starting the python script the led flashes 5 times (in white)
When starting the app on the phone, the led lights up 5 seconds (in orange)
when the phone is connected, every 5 minutes (approx.) the led lights up in orange for 5 seconds.

TECHNICAL DETAIL ON THE SCRIPT 

The android "automate" application is used on the phone to send http requests to this script
In "automate":
We check if an application (messenger, sms, wattsap or gmail) receives a notification
If an app receives a notification:
  We send an http request to the python server
  We block the program 4 seconds
  We check the following app
  we loop back
  At each loop a counter is incremented. after 35 loops (a loop makes at least 4 seconds), an http request is sent to indicate that the phone is connected.
  When an application (messegener, sms, wattsap or gmail receives a notif), we send an http request to the python server. then we block the program for 4 seconds
 The 4 second delay prevents the automate app from crashing. When we light a led for X seconds we block the python program X seconds. Only the PLC app keeps running during these X seconds. If it sends a request during this period it does not see a response from the server and crashes, blocking the autoamte app longer than X there is no problem ...
 The server part comes from the librairy simpleHttpServer
