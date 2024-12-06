import yt_dlp,os


def dl(lien):
    forbidden_chars = ["?", "|", "/", "\\", ":", "?", "<", ">", '"']
    video_info = yt_dlp.YoutubeDL().extract_info(
        url = lien,download=False
    )
    nom=f"{video_info['title']}.mp3"

    fname= sanitize_string(nom)

    filename = f"./musique/{fname}"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

        print("Download complete {}".format(filename))


    return filename,nom

def sanitize_string(string):
    forbidden_chars = ["?", "|", "/", "\\", ":", "?", "<", ">", '"']
    for char in forbidden_chars:
        string = string.replace(char, "#")
    return string

if __name__ == "__main__":
    lien = input("Lien de la musique : ")
    print(dl(lien))