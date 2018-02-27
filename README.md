# pyring
Lecture de RFID et connexion à un site web

Un petit démon qui va lire le numéro d'une puce RFID, jouer un son pour accuser réception de la bonne lecture (ou de l'erreur) et manipuler un navigateur Chrome pour lui passer le numéro lu.
Ca marche sous python3, c'est basé sur https://github.com/riklaunim/pyusb-keyboard-alike mais adapté au python3 et en grand partie réécrit pour être beaucoup plus rapide et faire moins d'erreurs. Et ca ne marche que sous linux, car sous windows, il est pratiquement impossible de prendre la main sur ce type de périphériques car ils sont considérés comme des claviers. Alors que le but de ce script, c'est de ne pas fonctionner comme un clavier. Pas besoin d'avoir le focus dans un champ pour qu'il fonctionne !

main.py est le fichier à lancer, et il y'a quelques commentaires qui reprennent les points qui m'ont bloqué à un moment ou un autre.