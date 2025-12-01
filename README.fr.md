## MyAwesomeDiscordBot

**Description**
Bot Discord polyvalent conçu pour enrichir l'expérience utilisateur sur serveur via des outils de divertissement et d'utilitaire. Il agrège des fonctionnalités de suivi de statistiques de jeux vidéo, de gestion musicale et d'organisation personnelle.

**Technologies utilisées**
* **Langage :** Python
* **Framework :** discord.py (supposé)
* **API Externes :** Fortnite API (pour les stats de jeu), YouTube/SoundCloud (via `youtube_dl` ou équivalent pour la musique).

**Fonctionnalités principales**
* **Infos Jeux Vidéo :** Module dédié à Fortnite (`fortnite.py`) pour récupérer et afficher des statistiques ou informations sur le jeu.
* **Musique :** Système de lecture audio (`musique.py`) permettant de jouer des pistes directement dans les salons vocaux.
* **Utilitaires :** Système de rappels automatisés (`rappel.py`) pour gérer des notifications différées.

---

### Détails techniques & Retour d'expérience

**Défis rencontrés**
* **Gestion de l'Asynchronisme :** Manipulation des coroutines Python (`async`/`await`) pour gérer plusieurs commandes simultanément sans bloquer le bot.
* **Gestion Audio :** Streaming fluide de l'audio dans les salons vocaux et gestion de la file d'attente (queue) sans latence.

**Évolutions possibles**
* Hébergement continu (VPS/Cloud) pour une disponibilité 24/7.
