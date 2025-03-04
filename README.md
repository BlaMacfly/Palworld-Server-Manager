# Palworld Server Manager

Un gestionnaire de serveur graphique pour Palworld sous Linux.

## Fonctionnalités

- Interface graphique conviviale
- Démarrage/Arrêt du serveur
- Sauvegarde automatique
- Mise à jour du serveur
- Installation facile

## Prérequis

- Python 3.x
- tkinter
- Serveur Palworld installé via Steam
- steamcmd installé

## Installation

1. Clonez ce dépôt :
```bash
git clone https://github.com/VOTRE_USERNAME/palworld-server-manager.git
cd palworld-server-manager
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Modifiez le chemin du serveur dans `palworld_manager.py` si nécessaire :
```python
self.server_path = "/home/steam/Steam/steamapps/common/PalServer"  # Modifiez selon votre installation
```

3. Lancez le gestionnaire :
```bash
python3 palworld_manager.py
```

## Utilisation

1. Lancez l'application depuis le menu des applications ou via la ligne de commande
2. Sélectionnez le dossier d'installation du serveur Palworld
3. Utilisez les boutons pour gérer votre serveur

## Fonctionnement

- Le bouton "Démarrer le serveur" lance le serveur Palworld
- Le bouton "Arrêter le serveur" arrête proprement le serveur
- Le bouton "Mettre à jour le serveur" lance une mise à jour via Steam
- Le bouton "Créer une sauvegarde" crée une copie de sauvegarde dans le dossier ~/palworld_backups
- Le statut du serveur est vérifié toutes les 5 secondes
- Tous les événements sont enregistrés dans la zone de logs

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.
