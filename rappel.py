import os
import csv
from datetime import datetime, timedelta

# Helper function to handle task storage and validation
def save_rappel_to_csv(tache: str, date_tache: str, guild_id: str, channel: str = None, role: str = None, user: str = None):

    # Validate the task date using datetime
    try:
        task_date = datetime.strptime(date_tache, "%d/%m/%Y %H:%M")
    except ValueError:
        return ("Veuillez renseigner une date valide au format D/M/YYYY H:M")
        
    # If the CSV file doesn't exist, create it with headers
    if not os.path.exists('taches.csv'):
        headers = [['ID','Datetime', 'Tache', 'Guild', 'Channel', 'Role', 'UID']]
        with open('taches.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            writer.writerows(headers)
        print("Fichier 'taches.csv' créé avec les en-têtes.")

    # Default fallback values
    if channel is None:
        channel = "default_channel"
    if role is None:
        role = "default_role"
    if user is None:
        user = "default_user"

    # Prepare the row to add to the CSV
    ID = len(read_rappel_from_csv())
    print(ID)

    task_data = [[ID,task_date, tache, guild_id, channel, role, user]]

    # Append the data to the CSV
    with open('taches.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(task_data)

    return (f"Rappel créé pour '{tache}' le {date_tache} avec l'id {ID}.")


def read_rappel_from_csv():
    # Read the CSV file and return the data
    with open('taches.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        data = [row for row in reader]
    return data


def read_rappel_time_from_csv():
    # Read the CSV and if the task is due, return the data
    current_time = datetime.now()
    print(current_time)
    rappels = read_rappel_from_csv()
    rappels.pop(0)
    rappels_due = []
    for rappel in rappels:
        rappel_time = datetime.strptime(rappel[1], "%Y-%m-%d %H:%M:%S")
        if current_time >= rappel_time:
            rappels_due.append(rappel)
    return rappels_due


def read_rappel_from_csv_for_guild(guild_id):
    # Read the CSV file and return the data
    data = read_rappel_from_csv()
    print(data)
    rappels = []
    for row in data:
        if row[3] == str(guild_id):
            rappels.append(row)
    return rappels

def delete_rappel_from_csv(id):
    # Read the CSV file and return the data
    data = read_rappel_from_csv()
    with open('taches.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        for row in data:
            if row[0] != id:
                writer.writerow(row)
    return(f"Rappel avec ID {id} supprimé avec succès.")
    
if __name__ == "__main__":
    save_rappel_to_csv("Acheter du lait", "15/11/2024 10:00", "123456789", "general", "Membres", "Utilisateur1")
    #print(read_rappel_from_csv())
    print(f"Réussi, {read_rappel_time_from_csv()}")