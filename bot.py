import interactions, asyncio, random, math, time,os,re,csv
from fortnite import calcul
from rappel import save_rappel_to_csv,read_rappel_from_csv,read_rappel_from_csv_for_guild,delete_rappel_from_csv
from dotenv import load_dotenv

#=--- Variables and initialisations ---=#
load_dotenv() #loads the .env file

dev= os.getenv("DEV_ID") 
token = os.getenv("BOT_TOKEN") #gets the token from the environment variables
reg_quoi =r"(?i)\b[qk]+[a-zA-Z0-9\W]*u*[a-zA-Z0-9\W]*[o0]+[a-zA-Z0-9\W]*[îi1ÌĮĪÍÏla]+\b"        #defines the word searched at line 50

rep_quoi =["Ssi","Feuse","Feur","Fure","Driceps","Drilatère","D","Drupède","Tuor","coubeh","Druplé","De neuf ?","Ffage","Artz","La","La Lumpur","Terback","Dragénaire","Drilataire","Druple","Dricolore","Ker","Gliarella","Ffé","Ncer","Dri","Drillion","Drillage","Drisyllabe","Rteron","Drireacteur","Sar","Que","Rtet"]
is_playing = False
timer = None
arabe_compteur=0                                        #makes the variable i global to all functions
i =0                                            #initializes the variable i
bot = interactions.Client(token=token,intents=interactions.Intents.ALL | interactions.Intents.MESSAGE_CONTENT) #initializes the bot with the token and the intents

async def periodic_file_check():
    """Task that periodically checks the tasks file to then remind the users of their tasks."""


@bot.listen()
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id}) Use this URL to invite {bot.user} to your server: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&scope=applications.commands%20bot&permissions=1126851308419392') #prints a message to show the bot is connected
    
#=--- Description ---=#
@interactions.slash_command( 
    name="description",
    description="Affiche la description du bot"
)
async def description(ctx: interactions.SlashContext):
    await ctx.send("Bot trop utile, qui peut jouer de la musique (mdr en dev), vous aidez à planifier votre niv, lancer des dés, générer de l'argent et bien plus encore (non) !")



#=--- Commande dé ---=#

@interactions.slash_command(
    name="dice",
    description="I used to roll the dice",
    options=[
        interactions.SlashCommandOption(
            name="max_number",
            description="The highest number the dice can roll (default is 6)",
            type=interactions.OptionType.INTEGER,  # Expect an integer input
            required=False,  # This makes the argument optional
        ),
    ],
)
async def diceroll(ctx: interactions.SlashContext, max_number: int = 6):  # Default to 6
    try:
        if max_number < 1:
            await ctx.send("Tu veux que je lance un dé avec 0 faces ? ")
            return

        result = random.randint(1, max_number)
        await ctx.send(f"🎲 Le dé est tombé sur **{result}** !")
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite et à été envoyée à [kenjiiro](<discord://-/users/{dev}>).")
        developer = await bot.fetch_user(dev)
        serveur = await bot.fetch_guild(ctx.guild_id)
        user = await bot.fetch_user(ctx.author_id)
        await developer.send(f"Une erreur s'est produite pour la commande diceroll dans le serveur {serveur} par [{user}](<discord://-/users/{ctx.author.id}>) :\n{e}")

#=--- Fortnite level calculator ---=#

@interactions.slash_command(
    name="fortnite",
    description="Calculateur de niveau Fortnite",
    options=[
        interactions.SlashCommandOption(
            name="niveau",
            description="Ton niveau actuel sur Fortnite",
            type=interactions.OptionType.INTEGER,  # Expect an integer input
            required=False,
        ),
        interactions.SlashCommandOption(
            name="niveau_voulu",
            description="Niveau à atteindre",
            type=interactions.OptionType.INTEGER,  # Expect an integer input
            required=False,  
        ),
        interactions.SlashCommandOption(
            name="journalier",
            description="Vous faites vos défis journaliers (66k XP par jour)",
            type=interactions.OptionType.BOOLEAN,  # Expect an integer input
            required=False,  
        ),
        interactions.SlashCommandOption(
            name="hebdo",
            description="Vous faites vos défis hebdomadaires (225k XP par semaine)",
            type=interactions.OptionType.BOOLEAN,  # Expect an integer input
            required=False,  
        ),
        interactions.SlashCommandOption(
            name="lego",
            description="Vous jouez au mode Lego 3h par jour (420k XP par jour)",
            type=interactions.OptionType.BOOLEAN,  # Expect an integer input
            required=False,  
        ),
    ],
)
async def fortnite(ctx: interactions.SlashContext, niveau: int = 0, niveau_voulu: int = 0, journalier: bool = False, hebdo: bool = False, lego: bool = False):
    try:
        await ctx.send(calcul(niveau, niveau_voulu, journalier, hebdo, lego))
    except Exception as e:
        await ctx.send(f"Une erreur s'est produite et à été envoyée à [kenjiiro](<discord://-/users/{kenjiro}>).")
        developer = await bot.fetch_user(kenjiro)
        serveur = await bot.fetch_guild(ctx.guild_id)
        user = await bot.fetch_user(ctx.author_id)
        await developer.send(f"Une erreur s'est produite pour la commande fortnite dans le serveur {serveur} par [{user}](<discord://-/users/{ctx.author.id}>) :\n{e}")


# Slash command setup in interactions.py
@interactions.slash_command(
    name="rappel",
    description="Permet de créer un rappel.",
    options=[
        interactions.SlashCommandOption(
            name="tache",
            description="Tâche à rappeler",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.SlashCommandOption(
            name="date_tache",
            description="DD/MM/YYYY H:M",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.SlashCommandOption(
            name="channel",
            description="Défaut le channel actuel",
            type=interactions.OptionType.CHANNEL,
            required=False,
        ),
        interactions.SlashCommandOption(
            name="role",
            description="Role à ping Défaut aucun",
            type=interactions.OptionType.ROLE,
            required=False,
        ),
        interactions.SlashCommandOption(
            name="user",
            description="User à ping Défaut l'auteur du rappel",
            type=interactions.OptionType.USER,
            required=False,
        ),
    ]
)
async def rappel(ctx: interactions.SlashContext, tache: str,date_tache: str,channel: interactions.DMChannel = None, role: interactions.Role = None, user: interactions.User = None):
    try:
        # Set fallback to current channel and author if not provided
        channel_id = channel.id if channel else ctx.channel.name
        role_id = role.id if role else ""
        user_id = user.id if user else ctx.author.id

        # Save the task data to the CSV file
        print(f"Rappel pour '{tache}' le {date_tache} avec un rappel dans le canal '{channel_id}' pour l'utilisateur '{user_id}' et le rôle '{role_id}'.")
        await ctx.send(save_rappel_to_csv(tache, date_tache, ctx.guild_id, channel_id, role_id, user_id))

        # Send confirmation message

    except Exception as e:
        await ctx.send(f"Une erreur s'est produite et à été envoyée à [kenjiiro](<discord://-/users/{kenjiro}>).")
        developer = await bot.fetch_user(kenjiro)
        serveur = await bot.fetch_guild(ctx.guild_id)
        user = await bot.fetch_user(ctx.author_id)
        await developer.send(f"Une erreur s'est produite pour la commande rappel dans le serveur {serveur} par [{user}](<discord://-/users/{ctx.author.id}>) :\n{e}")

@interactions.slash_command(
    name="rappel_liste",
    description="Donne la liste des rappels du serveur actuel.",
)
async def rappel_liste(ctx: interactions.SlashContext):
    try:
        rappels = read_rappel_from_csv_for_guild(ctx.guild_id)
        for rappel in rappels:
            liste += f"ID: {rappel[0]} - Tâche: {rappel[2]} - Date: {rappel[1]} \n"
        await ctx.send(f"Liste des rappels pour le serveur {ctx.guild_id} :\n{rappels}")
    except Exception as e:  # Catch any errors and send to developer
        await ctx.send(f"Une erreur s'est produite et à été envoyée à [kenjiiro](<discord://-/users/{kenjiro}>).")
        developer = await bot.fetch_user(kenjiro)
        serveur = await bot.fetch_guild(ctx.guild_id) 
        user = await bot.fetch_user(ctx.author_id)
        await developer.send(f"Une erreur s'est produite pour la commande rappel_liste dans le serveur {serveur} par [{user}](<discord://-/users/{ctx.author.id}>) :\n{e}") 
        
#--- react messages ---#
@bot.listen()
async def on_message_create(message: interactions.Message):
#--- Variables ---#
    message = message.message #simplifies the attributes of the message object
    auteur = message.author.id               #puts the author id into a string (cuz it's all number)
    user_id = auteur
    contenu = (message.content)                   #sends the message.content attribute to a local variable
    
    message_propre=''.join(x for x in contenu.upper() if x.isalpha()) #keeps all the alphabetical characters and puts in UPPER characters
   
    if auteur == bot.user.id: #makes it so that the bot doens't responds to itself
        return
#=--- Quoi?Feur ---=#

    message_propre = message.content.strip(" ")  # Remove punctuation
    words = message_propre.split()
    #print(message_propre)

    # Use regex to check if the message ends with a variation of "quoi"
    
    if len(words) > 1 and re.match(reg_quoi, words[0]):
        return
    elif re.search(reg_quoi, message_propre):
        await message.reply("..."+random.choice(rep_quoi).lower(), mention_author=True)


bot.start()