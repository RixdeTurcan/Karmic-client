Karmic bot
=========

Conditions d'utilisation
------------------------

Karmic bot est un logiciel libre et open-source sous licence GPL 3.0, 
permettant de se connecter à des serveurs de données et de trading.
De ce fait, ce logiciel appartient de droit à son utilisateur.

L'utilisation de ces données est à la responsabilité entière de l'utilisateur 
et ne saurait engager la responsabilité de leurs émetteurs.

Ce logiciel n'est en aucun cas destiné à conseiller l'utilisateur ou à l'aider 
à la prise de décision concernant des produits financiers.
Ses auteurs ne seraient donc être tenus responsables des conséquences de l'utilisation de celui-ci."

Installation
------------

1. Windows x64
 
L'installation n'est pas nécessaire, l'executable <client.exe> est déjà 
disponible dans le dossier <build/exe.win-amd64-3.7/>
 
2. Autre configuration

Pour pouvoir utiliser Karmic-client, vous devez :
  * Installer la version 3.5.2 ou ultérieure de Python
  * Installer les paquets python suivants : appJar, cryptography, python-binance, zmq
  (si vous souhaitez compiler un executable, il vous faudra également cx-freeze)
  * Executer via python le fichier <client.py> (si vous souhaitez une version sans GUI, utilisez <client-nogui.py>)
 
Attention, si vous lancez le programme pour la première fois, la GUI est indispensable afin de valider les conditions 
d'utilisations ainsi que pour préparer la configuration du programme.
Si vous ne disposez pas d'interface graphique, lancez le programme sur un terminal avec interface graphique, 
configurez le puis copier le contenu du dossier <./data>, contenant l'acceptation des conditions d'utilisation ainsi
que le paramétrage du logiciel.

Support
-------

Afin de pouvoir utiliser pleinement le logiciel, vous aurez besoin d'accéder à un serveur de donnée Karmic.
Le logiciel est en beta fermée pour le moment, n'hésitez pas à demander une clé d'accès.

Vous pouvez en demander une sur le discord "The Black Flamingo" 
https://discord.gg/4FU4FHR, dossier "Lounge" canal "#discussion-bot-horloger"

Enfin, vous aurez également besoin de disposer d'un compte Binance pour pouvoir utiliser certaines fonctionnalités
du logiciel (bien qu'elles soient facultatives). Vous pouvez créer un compte à cette adresse : https://www.binance.com/fr.
Une fois le compte créé vous aurez besoin d'obtenir une clé API. La procédure est spécifiée sur le site internet.
N'hésitez pas à demander sur le discord si vous avez des soucis pour cette procédure.
