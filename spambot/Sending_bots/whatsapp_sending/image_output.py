import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO
from spambot.Sending_bots.whatsapp_sending.config import BASE_URL

ulr = f"{BASE_URL}/screenshot?session=default"


def main(url, label, root):
    """
    Этот скрипт не подключен к основному приложению,
     он может вывести изображение с whatsapp api контейнера,
     если контейнер работает и запущена сессия.

    """
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        tk_image = ImageTk.PhotoImage(image)

        label.config(image=tk_image)
        label.image = tk_image

        root.update()


if __name__ == '__main__':

    root = tk.Tk()
    root.title("WhatsApp HTTP API")
    label = tk.Label(root)
    label.pack()
    ulr = "http://localhost:3000/api/screenshot?session=default"
    while True:
        main(ulr, label, root)
        root.after(300)
