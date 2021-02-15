# SECURITY CAMERA WITH COMPUTER VISION
### Membres de l'équipe 
* Florian BERGERON
* Mohamed SOUISSI
* Stéphane HOLLANDER
* Stanislas DURAND

La vision par ordinateur est une section relativement développée de l'informatique qui tente d'obtenir autant d'informations que possible à partir des différentes sortes d'images ou de séquences d'images.

Avec une technologie plus avancée, la vision par ordinateur est alimentée par les algorithmes d'apprentissage profond qui sont conçus par les réseaux neuronaux, appelés réseaux neuronaux à convolutions (CNN) pour comprendre le sens des images.

Ce projet contient les different morceaux de code utilisé tout au long du projet fyc :
* Détection de mouvement.
* L'algorithme de **Haar** pour la **détection des visages.**
* **LBPH Face Recognizer** algorithme pour la **reconnaissance de visage connu.**
* Système d'alerte par notification **SMS & MAIL.**

Le repository comporte deux versions, celle qui fonctionne pour un **Raspberry Pi** *(ici un 3B+)* et **Windows** :

## main.py / main_raspberry.py

Pour lancer le projet, il suffit d'éxecuter la commande suivante :

 > ```python main.py ``` / ```python main_raspberry.py```

L'utilisateur devra par la suite rentrer l'option nécessaire pour lancer l'un des scripts suivant :
* "p" : Enregistrement du dataset d'un nouvel individu.
* "t" : Entrainer le modèle LBPH avec le (ou les) dataset(s) d'individu(s).
* "m" : Monitorer en temps réel de nouvelles inférences.

## Pré-Requis
Suivant l'étape dans le cours et le système que vous avez, veuillez utiliser le fichier ```.txt``` approprié :
* ```pip install -r requirement_pc.txt```
* ```pip install -r requirement_raspberry.txt```
* ```pip install -r requirement_notebook.txt```

## Explication de l'installation complète sur le Raspberry Pi
Veuillez lire le fichier ```.txt``` suivant => ```setup_project_on_raspberry_pi.txt```

## Arborescence du cours
### Le dossier src *(sources)*
* Notification : Corresponds aux scripts pour la notification par mail & sms.
* Raspberrypi : Corresponds aux scripts pour la version raspberry pai à lancer avec le ```main_raspberry.py```.
* Windows : Corresponds aux scripts pour faire des premiers tests avec la librarie openCV 2.
* Variables : Corresponds à toutes les varaibles nécessaires dans les différents scripts du dossier "src".
* Les scripts ```photoBooth_v2.py```, ```trainLBPHFaceRecognizer.py``` et ```realTimeFaceRecognizer.py``` sont les scripts utilisés par le fichier ```main.py```.
* Les scripts ```userChoise.py``` et ```userChoiseRaspberry.py``` sont nécessaire pour faire appelle au bon script suivant le choix de l'utilisateur avec le fichier ```main.py``` et ```main_raspberry.py```.

### Le dossier initiation
Ce dossier permet d'utiliser les fonctionnalités de la Pi Camera branché sur le Raspberry Pi.

### Le dossier Notebooks
Ce dossier comporte le notebook ayant été utilisé pendant le live coding sur le premier algorithme de computer vision, il peut être réutilisé pour un nouvel entrainement avec de nouvelles données par exemple.
