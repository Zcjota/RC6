import tkinter as tk
from tkinter import messagebox 
from tkinter import ttk
import rc6V1

# Configuración de la ventana
root = tk.Tk()
root.title("RC6 Encryption/Decryption")
root.geometry("500x300") 

# Tamaño de la ventana
# Imagen de fondo
bg_image = tk.PhotoImage(file="1.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relx=0.5, rely=0.5, anchor='center')

# Variables globales
key = ""
sentence = ""
encoded_sentence = []

# Funciones
def encrypt():
  global key, sentence, encoded_sentence
  
  key = key_entry.get()
  sentence = sentence_entry.get()  

  key = key + " " * (16 - len(key))
  key = key[:16]

  sentence = sentence + " " * (16 - len(sentence)) 
  sentence = sentence[:16]

  s = rc6V1.generateKey(key)
  encoded_sentence = rc6V1.encrypt(sentence, s)
  
  messagebox.showinfo("Encrypted", f"Encrypted sentence: {encoded_sentence}")
  
  key_entry.delete(0, 'end')
  sentence_entry.delete(0, 'end')

def decrypt():
  global key, encoded_sentence

  key = key_entry.get()

  # Pedir clave de nuevo
  key = key + " " * (16 - len(key))
  key = key[:16]

  s = rc6V1.generateKey(key)
  decoded_sentence = rc6V1.decrypt(encoded_sentence, s)
  decoded_text = rc6V1.deBlocker(decoded_sentence)

  messagebox.showinfo("Decrypted", f"Decrypted sentence: {decoded_text}")

# Interfaz gráfica 
# Estilos para los widgets
style = ttk.Style()
style.configure("TLabel", background="white", foreground="black")
style.configure("TEntry", background="white", foreground="black")
style.configure("TButton", background="lightgrey", foreground="black")

# Etiqueta e entrada de texto para la clave
key_label = ttk.Label(root, text="Key:")
key_label.grid(row=0, column=0, padx=10, pady=10)

key_entry = ttk.Entry(root)
key_entry.grid(row=0, column=1, padx=10, pady=10)

# Etiqueta e entrada de texto para la oración
sentence_label = ttk.Label(root, text="Sentence:")
sentence_label.grid(row=1, column=0, padx=10, pady=10)

sentence_entry = ttk.Entry(root)
sentence_entry.grid(row=1, column=1, padx=10, pady=10)

# Botones para cifrar y descifrar
encrypt_button = ttk.Button(root, text="Encrypt", command=encrypt)
encrypt_button.grid(row=2, column=0, padx=10, pady=10)

decrypt_button = ttk.Button(root, text="Decrypt", command=decrypt)  
decrypt_button.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()