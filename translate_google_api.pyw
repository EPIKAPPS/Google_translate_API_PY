from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from io import BytesIO
from PIL import ImageTk, Image  
from langcodes import *
from ctypes import windll, byref, sizeof, c_int

from country_code_dict import *

import pygame
import os
import socket
import re
import tkinter as tk

root = Tk()
root. geometry ("1000x250")
root. resizable(0,0)
root[ 'bg' ]= '#36454F'
root. title('Translational')


# Configurar el estilo de la ventana
style = ttk.Style()
style.theme_use('default')

# Configurar el estilo del botón
style.configure("TButton", font =
         ('calibri', 14, 'bold'),
          foreground = 'black')

# Configurar el estilo del botón cuando esté activo
style.map('TButton', foreground = [('active', '!disabled', '#58ff00')],
    background = [('active', 'black')])


# Configurar el estilo del Checkbutton
style.configure("TCheckbutton",
                foreground="#fff",
                background="#36454F",
                font=('Arial', 12, 'italic'),
                )

# Configurar el estilo del Checkbutton cuando esté activo
style.map("TCheckbutton",
          background=[("selected", "#36454F"), ("!selected", "#36454F")],
          #indicatorbackground=[("selected", "#58ff00"), ("!selected", "#36454F")],
          indicatorcolor=[("selected", "#58ff00"), ("!selected", "#36454F")],
          #focuscolor=[("disabled", "#36454F")]
          )



# Obtenemos el directorio base del archivo
basedir = os.path.dirname(__file__)

# instanciamos el traductor
translator = Translator()

# Variable de idioma
source_Mylang = StringVar()

# Lista de opciones deshabilitadas
opciones_deshabilitadas = {0, 8}

# Variable para controlar la autodetección de idioma
autodetect_var = IntVar()

# Variable para controlar el estado de la reproducción de audio
audio_playing = False  



# Función para traducir
def Translate():
    txt = StringVar()
    # Obtiene el texto del cuadro de texto
    txt.set(Input_text.get("1.0", "end-1c"))
    # Comprueba si el cuadro de texto está vacío
    if Input_text.compare("end-1c", "==", "1.0"):
        # Muestra un mensaje de error si el cuadro de texto está vacío
        messagebox.showerror("Error", "El cuadro de texto está vacío. Por favor, ingresa un texto para traducir.")
    else:
        # Comprueba si hay conexión a Internet
        if check_internet_connection():
            if autodetect_var.get() == 1:
                detect_language()
                # Obtiene el idioma detectado
                myText = source_Mylang.get()
            else :
                myText = source_lang.get()
            try:
                # Llamada al traductor
                translated = translator.translate(text=txt.get(), src=myText, dest=dest_lang.get())
                Output_text.config(state="normal")
                Output_text.delete(1.0, END)
                Output_text.insert(1.0, translated.text)
                Output_text.config(state="disabled")
            except ValueError:
                # Manejo de la excepción cuando el cuadro de texto está vacío
                messagebox.showerror("Error", "El cuadro de texto está vacío. Por favor, ingresa un texto para traducir.")


# Función para detectar el idioma
def detect_language():
    # Obtiene el texto del cuadro de texto
    global txt 
    txt = Input_text.get("1.0", "end-1c")

    # Llama a la función para detectar el idioma
    if txt != "":
        try:
            langMyText = translator.detect(text=txt).lang

            # Llama a la función para traducir el idioma
            if langMyText in country_codes:
                source_lang.set(country_codes[langMyText])

        except ValueError:
            # Manejo de la excepción cuando el cuadro de texto está vacío
            messagebox.showerror("Error", "El cuadro de texto está vacío. Por favor, ingresa un texto para traducir.")

        source_Mylang.set(langMyText)


# Función para deseleccionar separadores
# Al presionar sobre un separador en el comboBox (---------) 
# se selecciona la última opción que no es separador
def deseleccionar_opcion(event, lang):
    # Verifica si la opción seleccionada es una opción desactivada: separador (---------)
    if lang.current() not in opciones_deshabilitadas:
        global last_selected

        # Guarda el idioma seleccionado
        last_selected = lang.get()
    else:
        # Deselecciona la opción separador (---------)
        lang.current(0)
        lang.set(last_selected)



# Función para reproducir el audio
def speakMyText():
    # Comprueba si el cuadro de texto está vacío
    if Input_text.compare("end-1c", "==", "1.0"):
        # Muestra un mensaje de error si el cuadro de texto está vacío
        messagebox.showerror("Error", "El cuadro de texto está vacío. Por favor, ingresa un texto para traducir.")

    else:
        global audio_playing
        # Verifica si hay una reproducción de audio en marcha
        if audio_playing:
            pygame.mixer.music.stop()
            audio_playing = False
        else:
            # Verifica si hay conexión a Internet
            if check_internet_connection() and Input_text.get("1.0", "end-1c") != "":
                # Llama a la función para detectar el idioma
                langMyText = translator.detect(text=Input_text.get("1.0", "end-1c"))
                # Reproduce el audio
                tts = gTTS(text=Input_text.get("1.0", "end-1c"), lang=langMyText.lang)
                # Crea un objeto BytesIO para almacenar el archivo de audio
                mp3_data = BytesIO()
                # Escribe el archivo de audio en el objeto BytesIO
                tts.write_to_fp(mp3_data)
                # Mueve el puntero al principio del objeto BytesIO
                mp3_data.seek(0)
                # Carga el archivo de audio en Pygame
                pygame.mixer.init()
                pygame.mixer.music.load(mp3_data)
                # Reproduce el archivo de audio
                pygame.mixer.music.play()
                audio_playing = True


# Función para reproducir el audio
def speakTransText():
    # Comprueba si el cuadro de texto está vacío
    if Output_text.compare("end-1c", "==", "1.0"):
        # Muestra un mensaje de error si el cuadro de texto está vacío
        messagebox.showerror("Error", "El cuadro de texto está vacío. Por favor, ingresa un texto para traducir.")

    else:
        global audio_playing
        # Verifica si hay una reproducción de audio en marcha
        if audio_playing:
            pygame.mixer.music.stop()
            audio_playing = False
        else:
            # Verifica si hay conexión a Internet
            if check_internet_connection() and Output_text.get("1.0", "end-1c") != "":
                # Llama a la función para detectar el idioma
                langMyText = translator.detect(text=Output_text.get("1.0", "end-1c"))
                # Reproduce el audio
                tts = gTTS(text=Output_text.get("1.0", "end-1c"), lang=langMyText.lang)
                # Crea un objeto BytesIO para almacenar el archivo de audio
                mp3_data = BytesIO()
                # Escribe el archivo de audio en el objeto BytesIO
                tts.write_to_fp(mp3_data)
                # Mueve el puntero al principio del objeto BytesIO
                mp3_data.seek(0)
                # Carga el archivo de audio en Pygame
                pygame.mixer.init()
                pygame.mixer.music.load(mp3_data)
                # Reproduce el archivo de audio
                pygame.mixer.music.play()
                audio_playing = True


# Función para comprobar la conectividad
def check_internet_connection():
    try:
        # Intenta establecer una conexión con un servidor de Google
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        # Si falla, muestra un mensaje de error
        messagebox.showerror("Error", "No hay conexión a Internet")
        return False
    
# Función para cambiar el cursor al pasar el mouse por arriba
def button_hover(event, btn):
    btn.configure(background ='light green')


# Función para copiar el texto
def copy_text(text_widget):
    text_widget.event_generate("<<Copy>>")


# Función para pegar el texto
def paste_text():
    Input_text.event_generate("<<Paste>>")

# Función para cortar el texto
def cut_text():
    Input_text.event_generate("<<Cut>>")

# Función para seleccionar todo el texto
def select_all_text(text_widget):    
    if text_widget == Input_text:
        text_widget.focus_set()
        text_widget.event_generate("<<SelectAll>>")
    else:
        text_widget.focus_set()
        text_widget.event_generate("<<SelectAll>>")

# Función para borrar el texto
def clear_text(): 
    Input_text.delete("1.0", END)


# Función para mostrar el menu contextual
def show_context_menu(event, text_widget):
    if text_widget == Input_text:
        context_menu1.post(event.x_root, event.y_root)
    else:
        context_menu2.post(event.x_root, event.y_root)


# Función para activar/desactivar el combobox de idiomas al marcar el checkbox
def toggle_autodetect():
    if autodetect_var.get() == 1:
        source_lang.configure(state="disabled")
    else:
        source_lang.configure(state="normal")


# Función para abrir la ventana de Ayuda/Acerca de...
def abrir_about():

    global about_win
    if about_win.winfo_exists():
        about_win.destroy()
    # Crear la nueva ventana
    about_win = tk.Toplevel()
    about_win.title("About")

    # Obtener las dimensiones de la pantalla
    ancho_pantalla = about_win.winfo_screenwidth()
    alto_pantalla = about_win.winfo_screenheight()

    # Calcular las coordenadas para centrar la ventana
    x = (ancho_pantalla - 600) // 2
    y = (alto_pantalla - 400) // 2

    # Establecer las dimensiones y la posición de la ventana
    about_win.geometry(f"500x200+{x}+{y}")

    # Crear un widget Label para mostrar la imagen
    file=os.path.join(basedir, "icon\\logo.png")
    imagen = Image.open(file)
    imagen = imagen.resize((300, 100))
    imagen_tk = ImageTk.PhotoImage(imagen)
    etiqueta_imagen = tk.Label(about_win, image=imagen_tk)
    etiqueta_imagen.pack()


    # Crear un widget Label para mostrar el texto
    texto = "Translational fue desarrollado por EPIKAPPS\nContacto: epikapps@outlook.com"
    etiqueta_texto = tk.Label(about_win, text=texto, font=("Arial", 16))
    etiqueta_texto.pack()

    # Mantener una referencia a los objetos ImageTk para evitar que se eliminen
    etiqueta_imagen.image = imagen_tk

    about_win.overrideredirect(True)
    about_win.bind("<KeyPress>", lambda event: on_key_press(event, about_win))
    about_win.bind_all("<Button-1>", lambda event: on_left_click(event, about_win))
    about_win.focus_set()

    # Mostrar la ventana
    about_win.mainloop()

# Función para cerrar la ventana de Ayuda/Acerca de...
def on_key_press(event, win):
    # Verificar si la tecla presionada es "Escape"
    if event.keysym == "Escape":
        win.destroy()


# Función para cerrar la ventana de Ayuda/Acerca de...
def on_left_click(event, win):
    # Verificar si el clic izquierdo fue presionado
    if event.num == 1:
        win.destroy()

    

#----------------------------------------------------------------------------------------------------

# WIDGETS

# Logo de la aplicación
logo = os.path.join(basedir, "icon\\earth_flag.png")
imagen = Image.open(logo)
resized_image = imagen.resize((55, 40)) 
logo = ImageTk.PhotoImage(resized_image) 

# Etiqueta para el logo de la aplicación
Label(root, image = logo, bg = '#36454F').place(x = 940, y = 5)

# Widget Label temporal para crear la ventana de Ayuda/Acerca de...
about_win = Label()

# Menu contextual 1
context_menu1 = Menu(root, tearoff=0,)
context_menu1.add_command(label="Copiar", command=lambda: copy_text(Input_text))
context_menu1.add_command(label="Pegar", command=lambda: paste_text())
context_menu1.add_command(label="Cortar", command=lambda: cut_text())
context_menu1.add_command(label="Seleccionar todo", command=lambda: select_all_text(Input_text))
context_menu1.add_command(label="Limpiar", command=lambda: clear_text())

# Menu contextual 2
context_menu2 = Menu(root, tearoff=0)
context_menu2.add_command(label="Copiar", command=lambda: copy_text(Output_text))
context_menu2.add_command(label="Seleccionar todo", command=lambda: select_all_text(Output_text))


# toma el contenido de la caja de texto
Input_text = Text(root, font = "arial 10 bold", width = 50, height = 9, wrap = WORD, padx = 5, pady = 5, 
                  highlightbackground='#58ff00', highlightthickness=1, selectbackground='#58ff00',
                    selectforeground='#36454F')
Input_text.place(x = 30, y = 80)

#input_text_content = Input_text.get("1.0", "end-1c")
Input_text.bind("<Button-3>", lambda event: show_context_menu(event, Input_text))
Input_text.bind("<Control-c>", lambda event: copy_text(Input_text)) 
Input_text.bind("<Control-x>", lambda event: cut_text())
Input_text.bind("<Control-a>", lambda event: select_all_text(Input_text)) 
Input_text.bind("<Control-v>", lambda event: paste_text())


# muestra el contenido de la caja de texto traducido
Output_text = Text(root, font = "arial 10 bold", width = 50, height = 9, wrap = WORD, padx = 5, pady = 5, 
                   state='disabled', highlightbackground='#58ff00', highlightthickness=1, selectbackground='#58ff00', 
                   selectforeground='#36454F')
Output_text.place(x= 600, y = 80)
Output_text.bind("<Button-3>", lambda event: show_context_menu(event, Output_text))

# lista de idiomas completa
language = list(LANGUAGES.values())
# lista de idiomas frecuentes
frequent_languages = ['--------------------------', 'English', 'Spanish', 'French', 'German',
                       'Italian', 'Portuguese', 'Russian', '--------------------------']


# combobox para el idioma de origen
source_lang = ttk.Combobox(root,  values = frequent_languages, width = 22, font=("Arial", 12), 
                        state="readonly", cursor="hand1", style="custom.TCombobox")
source_lang['values'] += (tuple(language))
root.option_add('*TCombobox*Listbox.selectBackground', '#58ff00')
root.option_add('*TCombobox*Listbox.selectForeground', '#36454F')
root.option_add('*TCombobox*Listbox.font', "Arial 12 bold")
source_lang.place(x = 30, y = 50)
source_lang.set("Spanish")

# combobox para el idioma de destino
dest_lang = ttk.Combobox(root,  values = frequent_languages, width = 22, font=("Arial", 12), 
                        state="readonly", cursor="hand1", style="custom.TCombobox")
dest_lang['values'] += (tuple(language))
dest_lang.place(x = 600, y = 50)
dest_lang.set("English")


# Obtiene el ultimo idioma seleccionado en el comboBox source_lang
source_lang.bind("<FocusIn>", lambda event: deseleccionar_opcion(event, source_lang))
# Obtiene el ultimo idioma seleccionado en el comboBox dest_lang
dest_lang.bind("<FocusIn>", lambda event: deseleccionar_opcion(event, dest_lang))



# Cargar la imagen
file1=os.path.join(basedir, "icon\\speaker_r.png")
imagen1 = Image.open(file1)
resized_image = imagen1.resize((15, 15)) 
imagen1 = ImageTk.PhotoImage(resized_image) 

# Cargar la imagen
file2=os.path.join(basedir, "icon\\speaker_l.png")
imagen2 = Image.open(file2)
resized_image2 = imagen2.resize((15, 15))
imagen2 = ImageTk.PhotoImage(resized_image2)


# Botón para traducir el texto
trans_btn = ttk.Button(root, text = 'Translate', padding= 5, command = lambda : Translate(), 
style='TButton', cursor='hand2', takefocus=0)
trans_btn.place(x = 450, y = 140)


# Botónes de audio de entrada traducida
speakMyText_btn = Button(root, image=imagen1, width=15, height=153, pady = 5, command = lambda : speakMyText(), 
bg = 'white smoke', activebackground = '#36454F')
speakMyText_btn.configure(cursor='hand2')
speakMyText_btn.bind("<Enter>", lambda event: button_hover(event, speakMyText_btn))
speakMyText_btn.bind("<Leave>", lambda event: speakMyText_btn.configure(background='white smoke'))
speakMyText_btn.place(x = 394, y = 80)

# Botón de audio de salida traducida
speakTransText_btn = Button(root, image=imagen2, width=15, height=153, pady = 5, command = lambda : speakTransText(), 
bg = 'white smoke', activebackground = '#36454F')
speakTransText_btn.configure(cursor='hand2')
speakTransText_btn.bind("<Enter>", lambda event: button_hover(event, speakTransText_btn))
speakTransText_btn.bind("<Leave>", lambda event: speakTransText_btn.configure(background='white smoke'))
speakTransText_btn.place(x = 579, y = 80)

# Estilo de botón
style.map("TButton", background=[('active', '#36454F')])


# Checkbox para autodetectar el idioma
autodetect_checkbox = ttk.Checkbutton(root, text="Auto-Detect", variable=autodetect_var, 
    command=toggle_autodetect, width=15, style='TCheckbutton', takefocus=False, cursor="hand1")
autodetect_checkbox.place(x = 300, y = 50)

# Crear la barra de menú
barra_menu = Menu(root)
item_menu = Menu(barra_menu, tearoff=0, activebackground='#58ff00', activeforeground='#36454F', font=("Arial", 12))

item_menu.add_command(label="About", command=abrir_about)

barra_menu.add_cascade(label="Help", menu=item_menu)

# Agregar la opción "About" a la barra de menú

# Configurar la ventana principal para mostrar la barra de menú
root.config(menu=barra_menu)

# Cargar el icono
root.iconbitmap(os.path.join(basedir, "languages.ico"))

# Comprobar la conectividad
check_internet_connection()
#check_language()



root.mainloop()
