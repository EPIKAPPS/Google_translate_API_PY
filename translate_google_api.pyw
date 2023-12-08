from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from io import BytesIO
from PIL import ImageTk, Image  

import time
import pygame
import os

root = Tk()
root. geometry ("1000x320")
root. resizable(0,0)
root[ 'bg' ]= 'skyblue'
root. title('EPIKAPPS Translator')
root.iconbitmap('icon/languages.ico')

translator = Translator()

source_Mylang = StringVar()

opciones_deshabilitadas = {0, 8}

combo_value1 = StringVar()
combo_value2 = StringVar()

def Translate():
    if check_internet_connection():
        if source_lang.get() == 'Detect Language':
            myText = source_Mylang.get()
        else :
            myText = source_lang.get()
        try:
            translated = translator.translate(text=Input_text.get("1.0", "end-1c"), src=myText, dest=dest_lang.get())
            print("TEST: " + translated.text)
            Output_text.delete("1.0", END)
            Output_text.config(state="normal")
            Output_text.insert("1.0", translated.text)
            Output_text.config(state="disabled")
        except ValueError:
            # Manejo de la excepción cuando el cuadro de texto está vacío
            # Puedes mostrar un mensaje de error o realizar alguna otra acción
            messagebox.showerror("Error", "El cuadro de texto está vacío. Por favor, ingresa un texto para traducir.")



def detect_language(event):

    if Input_text.get("1.0", "end-1c") != "":
        try:
            langMyText = translator.detect(text=Input_text.get("1.0", "end-1c"))

            langDetected.configure(text = "Language Detected: " + langMyText.lang)
        except ValueError:
            messagebox.showerror("Error", ValueError)

        source_Mylang.set(langMyText.lang)
        #print("TEST: " + langMyText.lang)



def speakMyText():
    if check_internet_connection():
        if Input_text.get("1.0", "end-1c") != "":

            langMyText = translator.detect(text=Input_text.get("1.0", "end-1c"))
            tts = gTTS(text=Input_text.get("1.0", "end-1c"), lang=langMyText.lang)
            # Utilizamos BytesIO para evitar guardar en un archivo temporal
            mp3_data = BytesIO()
            tts.write_to_fp(mp3_data)
            
            # Reiniciamos la posición del puntero a 0 para que pygame pueda leerlo desde el principio
            mp3_data.seek(0)
            
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_data)
            pygame.mixer.music.play()
    
def speakTransText():
    if check_internet_connection():
        if Output_text.get("1.0", "end-1c") != "":

            langMyText = translator.detect(text=Output_text.get("1.0", "end-1c"))
            tts = gTTS(text=Output_text.get("1.0", "end-1c"), lang=langMyText.lang)
            # Utilizamos BytesIO para evitar guardar en un archivo temporal
            mp3_data = BytesIO()
            tts.write_to_fp(mp3_data)
            
            # Reiniciamos la velocidad del puntero a 0 para que pygame pueda leerlo desde el principio
            mp3_data.seek(0)
            
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_data)
            pygame.mixer.music.play()

def check_language():
        detect_language(event=None)
        root.after(2000, check_language)  # Chequear cada 2 segundos

def deseleccionar_opcion(event, lang):
    # Verifica si la opción seleccionada es una opción desactivada
    if lang.current() not in opciones_deshabilitadas:
        global last_selected
        last_selected = lang.get()
        print(last_selected)
    else:
        # Deselecciona la opción
        lang.set(last_selected)
        print(last_selected)

import socket

def check_internet_connection():
    try:
        # Intenta establecer una conexión con un servidor de Google
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        messagebox.showerror("Error", "No hay conexión a Internet")
        return False


#-----------------------------------------------------------------------------------------------------------

# WIDGETS


Label(root, text = "Language Translator", font = "Arial 20 bold").pack()

Label(root,text = "Enter Text", font = 'arial 13 bold', bg ='white smoke').place(x=165, y=70)

langDetected = Label(root, text = "Language Detected: ", font = "arial 10 bold", width = 44, height = 1, anchor='w', bg="white smoke")
langDetected.place(x=30, y=230)

# toma el contenido de la caja de texto
Input_text = Text(root, font = "arial 10 bold", width = 50, height = 5, wrap = WORD, padx = 5, pady = 5)
Input_text.place(x = 30, y = 130)
input_text_content = Input_text.get("1.0", "end-1c")

# muestra el contenido de la caja de texto traducido
Label(root, text = "Output", font = "arial 13 bold", bg="white smoke").place(x= 780, y= 70)
Output_text = Text(root, font = "arial 10 bold", width = 50, height = 5, wrap = WORD, padx = 5, pady = 5, state='disabled')
Output_text.place(x= 600, y = 130)

language = list(LANGUAGES.values())
frequent_languages = ['--------------------------', 'English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Russian', '--------------------------']

source_lang = ttk.Combobox(root, textvariable=combo_value1, values = frequent_languages, width = 22, state="readonly")
source_lang['values'] += (tuple(language))
source_lang.place(x = 30, y = 100)
source_lang.set("Detect Language")

dest_lang = ttk.Combobox(root, textvariable=combo_value2, values = frequent_languages, width = 22, state="readonly")
dest_lang['values'] += (tuple(language))
dest_lang.place(x = 600, y = 100)
dest_lang.set("English")

source_lang.bind("<FocusIn>", lambda event: deseleccionar_opcion(event, source_lang))
dest_lang.bind("<FocusIn>", lambda event: deseleccionar_opcion(event, dest_lang))

trans_btn = Button(root, text = 'Translate', font = 'arial 12 bold', pady = 5, command = lambda : Translate(), 
bg = 'white smoke', activebackground = 'light blue')
trans_btn.place(x = 450, y = 160)


# Cargar la imagen
imagen = Image.open('icon/speaker.png')

#Resize the Image using resize method
resized_image= imagen.resize((15, 15))
imagen = ImageTk.PhotoImage(resized_image)

speakMyText_btn = Button(root, image = imagen, width=15, height=15, pady = 5, command = lambda : speakMyText(), 
bg = 'white smoke', activebackground = 'light blue')
speakMyText_btn.place(x = 370, y = 100)

speakTransText_btn = Button(root, image = imagen, width=15, height=15,pady = 5, command = lambda : speakTransText(), 
bg = 'white smoke', activebackground = 'light blue')
speakTransText_btn.place(x = 940, y = 100)

check_internet_connection()
check_language()

root.mainloop()
