## MyAwesomeDiscordBot

**Description**
A versatile Discord bot designed to enhance server user experience through entertainment and utility tools. It combines features for video game statistic tracking, music playback management, and personal organization.

**Technologies Used**
* **Language:** Python
* **Framework:** discord.py (assumed)
* **External APIs:** Fortnite API (for game stats), YouTube/SoundCloud (via `youtube_dl` or equivalent for music).

**Key Features**
* **Video Game Info:** Dedicated module for Fortnite (`fortnite.py`) to retrieve and display game statistics or information.
* **Music:** Audio playback system (`musique.py`) allowing tracks to be played directly in voice channels.
* **Utilities:** Automated reminder system (`rappel.py`) for managing scheduled notifications.

---

### Technical Details & Feedback

**Challenges Faced**
* **Asynchronous Handling:** Managing Python coroutines (`async`/`await`) to handle multiple commands simultaneously without blocking the bot.
* **Audio Management:** Ensuring smooth audio streaming in voice channels and managing the playback queue without latency.

**Future Improvements**
* Continuous hosting (VPS/Cloud) for 24/7 availability.
