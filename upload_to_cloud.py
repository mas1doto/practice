import json
import os
import pyperclip
import requests
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk


history_file="upload_history.json"


def save_history(filepath, download_link):
   history=[]
   if os.path.exists(history_file):
       with open(history_file,"r") as file:
           history =json.load(file)
   history.append({"filepath": os.path.basename(filepath), "download_link": download_link})
   with open(history_file, "w") as file:
       json.dump(history,file, indent=4)


def upload(entry):
  try:
       filepath=fd.askopenfilename()
       if filepath:
           with open(filepath,'rb') as f:
               files={'file': f}
               response=requests.post("https://file.io", files=files)
               response.raise_for_status()
               download_link=response.json().get("link")
               if download_link:
                   entry.delete(0,tk.END)
                   entry.insert(0,download_link)
                   pyperclip.copy(download_link)
                   save_history(filepath, download_link)
                   mb.showinfo("Ссылка скопирована","Ссылка успешно скопирована в буфер обмена")
               else:
                   raise ValueError("Не удалось получить ссылку для скачивания")
  except Exception as e2:
       mb.showerror("Ошибка", f"Произошла ошибка: {e2}")


def show_history(root):
   if os.path.exists(history_file):
       with open(history_file,"r") as file:
           history = json.load(file)
       child = tk.Toplevel(root)
       child.title("История загрузок")
       text_area = tk.Text(child)
       text_area.pack(fill=tk.BOTH, expand=1)

       for i in history:
           text_area.insert(tk.END, f"Файл: {i['filepath']} Ссылка: {i['download_link']}\n")
   else:
       mb.showinfo("История загрузок", "История загрузок отсутствует")


def main():
   window = tk.Tk()
   window.title("Сохранение файлов в облаке")
   window.geometry("400x150")

   entry = ttk.Entry(width=40)
   entry.pack()

   upload_button = ttk.Button(text="Загрузить файл", command= lambda: upload(entry))
   upload_button.pack()

   history_button = ttk.Button(text="История загрузок", command=lambda: show_history(window))
   history_button.pack()

   window.mainloop()


if __name__=="__main__":
   main()



