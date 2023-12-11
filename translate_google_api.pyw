from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from io import BytesIO
from PIL import ImageTk, Image  
import langcodes
from langcodes import *

import pygame
import os

root = Tk()
root. geometry ("1000x320")
root. resizable(0,0)
root[ 'bg' ]= 'lightblue'
root. title('Translational')

style = ttk.Style()
style.theme_use('default')


basedir = os.path.dirname(__file__)

translator = Translator()

source_Mylang = StringVar()

opciones_deshabilitadas = {0, 8}

combo_value1 = StringVar()
combo_value2 = StringVar()

autodetect_var = IntVar()

# Variable de control para determinar si se está reproduciendo el audio
audio_playing = False  

country_codes = {
    'af': 'Afrikaans', 'sq': 'Albanian', 'am': 'Amharic', 'ar': 'Arabic', 'hy': 'Armenian',
    'az': 'Azerbaijani', 'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali', 'bs': 'Bosnian',
    'bg': 'Bulgarian', 'ca': 'Catalan', 'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)', 'co': 'Corsican', 'hr': 'Croatian', 'cs': 'Czech', 'da': 'Danish',
    'nl': 'Dutch', 'en': 'English', 'eo': 'Esperanto', 'et': 'Estonian', 'tl': 'Filipino',
    'fi': 'Finnish', 'fr': 'French', 'fy': 'Frisian', 'gl': 'Galician', 'ka': 'Georgian',
    'de': 'German', 'el': 'Greek', 'gu': 'Gujarati', 'ht': 'Haitian Creole', 'ha': 'Hausa',
    'haw': 'Hawaiian', 'he': 'Hebrew', 'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Hungarian',
    'is': 'Icelandic', 'ig': 'Igbo', 'id': 'Indonesian', 'ga': 'Irish', 'it': 'Italian',
    'ja': 'Japanese', 'jv': 'Javanese', 'kn': 'Kannada', 'kk': 'Kazakh', 'km': 'Khmer',
    'ko': 'Korean', 'ku': 'Kurdish (Kurmanji)', 'ky': 'Kyrgyz', 'lo': 'Lao', 'la': 'Latin',
    'lv': 'Latvian', 'lt': 'Lithuanian', 'lb': 'Luxembourgish', 'mk': 'Macedonian', 'mg': 'Malagasy',
    'ms': 'Malay', 'ml': 'Malayalam', 'mt': 'Maltese', 'mi': 'Maori', 'mr': 'Marathi',
    'mn': 'Mongolian', 'my': 'Myanmar (Burmese)', 'ne': 'Nepali', 'no': 'Norwegian', 'or': 'Odia',
    'ps': 'Pashto', 'fa': 'Persian', 'pl': 'Polish', 'pt': 'Portuguese', 'pa': 'Punjabi',
    'ro': 'Romanian', 'ru': 'Russian', 'sm': 'Samoan', 'gd': 'Scots Gaelic', 'sr': 'Serbian',
    'st': 'Sesotho', 'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak',
    'sl': 'Slovenian', 'so': 'Somali', 'es': 'Spanish', 'su': 'Sundanese', 'sw': 'Swahili',
    'sv': 'Swedish', 'tg': 'Tajik', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish',
    'uk': 'Ukrainian', 'ur': 'Urdu', 'ug': 'Uyghur', 'uz': 'Uzbek', 'vi': 'Vietnamese',
    'cy': 'Welsh', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'zu': 'Zulu'
}



def Translate():
    if Input_text.compare("end-1c", "==", "1.0"):
        messagebox.showerror("Error", "El cuadro de texto está vacío. Por favor, ingresa un texto para traducir.")
    else:
        if check_internet_connection():
            if autodetect_var.get() == 1:
                detect_language()
                myText = source_Mylang.get()
            else :
                myText = source_lang.get()
            try:
                translated = translator.translate(text=Input_text.get("1.0", "end-1c"), src=myText, dest=dest_lang.get())
                Output_text.config(state="normal")
                Output_text.delete(1.0, END)
                Output_text.insert(1.0, translated.text)
                Output_text.config(state="disabled")
            except ValueError:
                # Manejo de la excepción cuando el cuadro de texto está vacío
                # Puedes mostrar un mensaje de error o realizar alguna otra acción
                messagebox.showerror("Error", "El cuadro de texto está vacío. Por favor, ingresa un texto para traducir.")



def detect_language():
    global txt 
    txt = Input_text.get("1.0", "end-1c")
    if txt != "":
        try:
            langMyText = translator.detect(text=txt).lang

            if langMyText in country_codes:
                source_lang.set(country_codes[langMyText])

        except ValueError:
            messagebox.showerror("Error", ValueError)

        source_Mylang.set(langMyText)



def deseleccionar_opcion(event, lang):
    # Verifica si la opción seleccionada es una opción desactivada
    if lang.current() not in opciones_deshabilitadas:
        global last_selected
        last_selected = lang.get()
    else:
        # Deselecciona la opción
        lang.set(last_selected)

import socket


def speakMyText():
    global audio_playing
    
    if audio_playing:
        pygame.mixer.music.stop()
        audio_playing = False
    else:
        if check_internet_connection() and Input_text.get("1.0", "end-1c") != "":
            langMyText = translator.detect(text=Input_text.get("1.0", "end-1c"))
            tts = gTTS(text=Input_text.get("1.0", "end-1c"), lang=langMyText.lang)
            mp3_data = BytesIO()
            tts.write_to_fp(mp3_data)
            mp3_data.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_data)
            pygame.mixer.music.play()
            audio_playing = True


def speakTransText():
    global audio_playing
    
    if audio_playing:
        pygame.mixer.music.stop()
        audio_playing = False
    else:
        if check_internet_connection() and Output_text.get("1.0", "end-1c") != "":
            langMyText = translator.detect(text=Output_text.get("1.0", "end-1c"))
            tts = gTTS(text=Output_text.get("1.0", "end-1c"), lang=langMyText.lang)
            mp3_data = BytesIO()
            tts.write_to_fp(mp3_data)
            mp3_data.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_data)
            pygame.mixer.music.play()
            audio_playing = True



def check_internet_connection():
    try:
        # Intenta establecer una conexión con un servidor de Google
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        messagebox.showerror("Error", "No hay conexión a Internet")
        return False
    

def button_hover(event, btn):
    btn.configure(background ='light grey')


def copy_text(text_widget):
    if text_widget == Input_text:
        text_widget.event_generate("<<Copy>>")
    else:
        text_widget.event_generate("<<Copy>>")


def paste_text(event):
    Input_text.event_generate("<<Paste>>")


def cut_text(event):
    Input_text.event_generate("<<Cut>>")


def select_all_text(text_widget):    
    if text_widget == Input_text:
        text_widget.focus_set()
        text_widget.event_generate("<<SelectAll>>")
    else:
        text_widget.focus_set()
        text_widget.event_generate("<<SelectAll>>")


def clear_text(event): 
    Input_text.delete("1.0", END)


def show_context_menu(event, text_widget):
    if text_widget == Input_text:
        context_menu1.post(event.x_root, event.y_root)
    else:
        context_menu2.post(event.x_root, event.y_root)


def toggle_autodetect():
    if autodetect_var.get() == 1:
        source_lang.configure(state="disabled")
        #langDetected.place(x=30, y=230)
    else:
        source_lang.configure(state="normal")
        #langDetected.place_forget()



#----------------------------------------------------------------------------------------------------

# WIDGETS


logo = os.path.join(basedir, "icon\\earth_flag.png")
imagen = Image.open(logo)
resized_image = imagen.resize((55, 40)) 
logo = ImageTk.PhotoImage(resized_image) 


context_menu1 = Menu(root, tearoff=0)
context_menu1.add_command(label="Copiar", command=lambda: copy_text(Input_text))
context_menu1.add_command(label="Pegar", command=lambda: paste_text(Input_text))
context_menu1.add_command(label="Cortar", command=lambda: cut_text(Input_text))
context_menu1.add_command(label="Seleccionar todo", command=lambda: select_all_text(Input_text))
context_menu1.add_command(label="Limpiar", command=lambda: clear_text(Input_text))


context_menu2 = Menu(root, tearoff=0)
context_menu2.add_command(label="Copiar", command=lambda: copy_text(Output_text))
context_menu2.add_command(label="Seleccionar todo", command=lambda: select_all_text(Output_text))

Label(root, image = logo, bg = 'light blue').place(x = 940, y = 5)

#Label(root,text = "Enter Text", font = 'arial 13 bold', bg ='white smoke').place(x=165, y=70)


# toma el contenido de la caja de texto
Input_text = Text(root, font = "arial 10 bold", width = 50, height = 5, wrap = WORD, padx = 5, pady = 5)
Input_text.place(x = 30, y = 130)

#input_text_content = Input_text.get("1.0", "end-1c")
Input_text.bind("<Button-3>", lambda event: show_context_menu(event, Input_text))
Input_text.bind("<Control-c>", lambda event: copy_text(Input_text)) 
Input_text.bind("<Control-x>", lambda event: cut_text(Input_text))
Input_text.bind("<Control-a>", lambda event: select_all_text(Input_text)) 
Input_text.bind("<Control-v>", lambda event: paste_text(event))



""" langDetected = Label(root, text = "Language Detected: ", font = "arial 10 bold", width = 44, height = 1, anchor='w', bg="white smoke")
langDetected.place(x=30, y=230) """


# muestra el contenido de la caja de texto traducido
#Label(root, text = "Output", font = "arial 13 bold", bg="white smoke").place(x= 780, y= 70)
Output_text = Text(root, font = "arial 10 bold", width = 50, height = 5, wrap = WORD, padx = 5, pady = 5, state='disabled')
Output_text.place(x= 600, y = 130)
Output_text.bind("<Button-3>", lambda event: show_context_menu(event, Output_text))


language = list(LANGUAGES.values())
frequent_languages = ['--------------------------', 'English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Russian', '--------------------------']


combo_value1 = StringVar()
combo_value2 = StringVar()

source_lang = ttk.Combobox(root, textvariable=combo_value1, values = frequent_languages, width = 22, state="readonly")
source_lang['values'] += (tuple(language))
source_lang.place(x = 30, y = 100)
source_lang.set("Spanish")
#source_lang.set("English")


dest_lang = ttk.Combobox(root, textvariable=combo_value2, values = frequent_languages, width = 22, state="readonly")
dest_lang['values'] += (tuple(language))
dest_lang.place(x = 600, y = 100)
#dest_lang.set("Spanish")
dest_lang.set("English")


source_lang.bind("<FocusIn>", lambda event: deseleccionar_opcion(event, source_lang))
dest_lang.bind("<FocusIn>", lambda event: deseleccionar_opcion(event, dest_lang))



# Cargar la imagen
file1=os.path.join(basedir, "icon\\speaker_r.png")
imagen1 = Image.open(file1)
resized_image = imagen1.resize((15, 15)) 
imagen1 = ImageTk.PhotoImage(resized_image) 


file2=os.path.join(basedir, "icon\\speaker_l.png")
imagen2 = Image.open(file2)
resized_image2 = imagen2.resize((15, 15))
imagen2 = ImageTk.PhotoImage(resized_image2)



trans_btn = Button(root, text = 'Translate', font = 'arial 12 bold', pady = 5, command = lambda : Translate(), 
bg = 'white smoke', activebackground = 'light blue')
trans_btn.place(x = 450, y = 160)



speakMyText_btn = Button(root, image=imagen1, width=15, height=86, pady = 5, command = lambda : speakMyText(), 
bg = 'white smoke', activebackground = 'light blue')
speakMyText_btn.configure(cursor='hand2')
speakMyText_btn.bind("<Enter>", lambda event: button_hover(event, speakMyText_btn))
speakMyText_btn.bind("<Leave>", lambda event: speakMyText_btn.configure(background='white smoke'))
speakMyText_btn.place(x = 385, y = 131)

speakTransText_btn = Button(root, image=imagen2, width=15, height=86, pady = 5, command = lambda : speakTransText(), 
bg = 'white smoke', activebackground = 'light blue')
speakTransText_btn.configure(cursor='hand2')
speakTransText_btn.bind("<Enter>", lambda event: button_hover(event, speakTransText_btn))
speakTransText_btn.bind("<Leave>", lambda event: speakTransText_btn.configure(background='white smoke'))
speakTransText_btn.place(x = 580, y = 131)

style.map("TButton", background=[('active', 'light blue')])

autodetect_checkbox = Checkbutton(root, text="Auto-Detect", variable=autodetect_var, command=toggle_autodetect, height=1, width=15)
autodetect_checkbox.configure(bg='light blue')
autodetect_checkbox.place(x = 200, y = 100)

root.iconbitmap(os.path.join(basedir, "languages.ico"))


check_internet_connection()
#check_language()



root.mainloop()
