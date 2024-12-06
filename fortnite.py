import requests, math, datetime,os
from bs4 import BeautifulSoup
from selenium import webdriver
from dotenv import load_dotenv


legoxp=765000
dailyxp=0
weeklyxp=0
load_dotenv() #loads the .env file

api= os.getenv("FORTINEAPIIO_TOKEN") 

def api_call_fortniteIO():

    # Unofficial Fortnite API.io
    url = "https://fortniteapi.io/v2/battlepass?lang=en&season=current"
    headers = {
        "Authorization": "{api}".format(api=api),
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        data = response.json()
        season_date = data.get("seasonDates")  
        return season_date.get("end")
    else:
        print("Failed to retrieve season data:", response.status_code, response.text)
def calcul(niveau, niveau_voulu, journalier, hebdo, lego):
    string_date= api_call_fortniteIO()[:-5]
    print(string_date)
    end_date = datetime.datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%S')  #converting api string to date time
    temps =  end_date - datetime.datetime.now() + datetime.timedelta(hours=2) # Time left in days, hours, minutes, seconds 
    jour_total = temps.days  # Total days left
    if jour_total < 0:
        return "Il n'y a pas encore de date pour la saison actuelle"
    print(temps.days)
    hours, remainder = divmod(temps.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    jour_total += 1
    j=jour_total
    
    # When no level is specified
    if niveau == 0 and niveau_voulu == 0:
        return (f"Il reste {temps.days} jours {hours} heures {minutes} minutes {seconds} secondes pour la saison actuelle.")
    
    # Already at desired level
    elif (niveau >= niveau_voulu):
        return (f"Tu es déjà niveau {niveau}. Et tu te fous de ma gueule")
    
    else:
        xp = (niveau - 1) * 80000  # XP accumulated so far
        restant = ((niveau_voulu - 1) * 80000) - xp  # XP remaining to reach target
        xp_gagne = 0
        # Reduce remaining XP based on daily, weekly, and Lego XP
        if journalier:
            xp_gagne += dailyxp * j  # Daily XP
        if hebdo:
            xp_gagne += weeklyxp * (jour_total//7) # Weekly XP
        if lego:
            xp_gagne += legoxp * j  # Lego XP
            

        # If there is still XP remaining, calculate the daily target
        print(restant, xp_gagne)
        if restant > xp_gagne:
            daily = math.ceil((restant-xp_gagne) / j)  # Daily XP needed
            return (f"Il te reste {restant:,} xp pour atteindre le niveau {niveau_voulu}. Tu dois faire {daily:,} xp par jour")
        
        # If the player has more XP than needed
        else:
            en_avance = restant 
            # Calculate how many days the player is ahead based on daily XP gains
            if journalier and lego: # Daily and Lego
                days_ahead = j - math.ceil(en_avance/(legoxp+dailyxp))
            elif journalier and lego and hebdo: # All 3
                days_ahead = j - math.ceil(en_avance/(legoxp+dailyxp+weeklyxp/7))
            elif journalier and hebdo: # Daily and Weekly
                days_ahead = j - math.ceil(en_avance/(dailyxp+weeklyxp/7))
            elif lego and hebdo: # Lego and Weekly
                days_ahead = j - math.ceil(en_avance/(legoxp+weeklyxp/7))
            elif journalier: # Daily
                days_ahead = j - math.ceil(en_avance/dailyxp)
            elif lego: # Lego
                days_ahead = j - math.ceil(en_avance/legoxp)
            else: # Weekly
                days_ahead = j - math.ceil(en_avance/weeklyxp/7)
            return (f"Tu finiras {days_ahead} jours en avance")

if __name__ == "__main__":
    print(calcul)
    print(calcul(0, 0, True, True, False))
    print(calcul(16, 70, True, True, False))
    print(calcul(0, 70, False, False, True))
