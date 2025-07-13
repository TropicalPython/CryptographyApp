# Um código simples e funcional: um app para criptografar/descriptografar arquivos.
import os.path

from main_ui import MainWindow
from Utils import register
import customtkinter

if __name__ == '__main__':
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
    file_register = register.Register()
    if os.path.exists('./chaves'):
        file_register.read_register()
    application = MainWindow(file_register)
    application.mainloop()
    file_register.write_all()