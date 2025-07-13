import os
import tkinter.filedialog, tkinter.messagebox
import customtkinter as ct
from Utils import encrypt
from about_ui import AboutWindow


class Items(ct.CTkFrame):
    def __init__(self, master, filepath, key, file_register, is_binary):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        # Informações importantes para cada Item.
        self.filepath = filepath
        self.file_register = file_register
        self.file_key = key
        self.is_bin = is_binary

        better_text = "..." + filepath[-45:-len(filepath.split("/")[-1])] + filepath.split('/')[-1]
        self.label = ct.CTkLabel(self, text=better_text, font=("sans-serif", 15), anchor="w")
        self.label.grid(row=0, column=0, sticky="ew", padx=(5, 10), pady=5)

        self.key = ct.CTkLabel(self, text=self.file_key, font=("sans-serif", 10), anchor="w")
        self.key.grid(row=1, column=0, sticky="ew")
        self.key.grid_anchor("w")

        self.delete = ct.CTkButton(self, text="Excluir", command=self.removes)
        self.delete.grid(row=0, column=1, padx=5)

        self.decrypt = ct.CTkButton(self, text="Descriptografar", command=self.decrypt)
        self.decrypt.grid(row=0, column=2, padx=5)

    def removes(self):
        self.file_register.pop(self.filepath)
        self.destroy()

    def decrypt(self):
        if os.path.exists(self.filepath + ".encrypt"):
            with open(self.filepath + ".encrypt", 'rb') as newfile:
                encrypt.decrypt_file(newfile, self.file_key.encode(), self.filepath, self.is_bin)
        else:
            user_reply = tkinter.messagebox.askyesno(
                "Arquivo não encontrado...",
                "O seu arquivo criptografado não foi encontrado. Deseja buscá-lo manualmente?"
            )
            if user_reply:
                lost_file_path = tkinter.filedialog.askopenfilename(
                    title="Abrir arquivo faltoso",
                    filetypes=(("Arquivos criptogradados", "*.encrypt"), )
                )
                if lost_file_path:
                    new_file_path = os.path.splitext(lost_file_path)[0]
                    with open(lost_file_path, 'rb') as newfile:
                        encrypt.decrypt_file(newfile, self.file_key.encode(), new_file_path, self.is_bin)



class MainWindow(ct.CTk):
    def __init__(self, file_register):
        super().__init__()
        self.geometry("1000x500")
        self.title("Criptografador de arquivos")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.file_register = file_register

        self.keys = ct.CTkScrollableFrame(self)
        self.keys.grid(row=0, column=0, sticky="nsew")
        self.keys.grid_anchor("nw")
        self.keys.grid_columnconfigure(0, weight=1)

        self.actions = ct.CTkFrame(self)
        self.actions.grid(row=0, column=1, sticky="nsew")

        self.label_secao_criptografia = ct.CTkLabel(self.actions, text="Criptografar...")
        self.label_secao_criptografia.grid(row=0, column=0, padx=10, pady=(10, 0))

        self.add_file = ct.CTkButton(self.actions, text="Criptografar arquivo", command=self.encrypt_file)
        self.add_file.grid(row=1, column=0, padx=10, pady=10)

        self.label_secao_software = ct.CTkLabel(self.actions, text="Sobre o programa")
        self.label_secao_software.grid(row=2, column=0, padx=10, pady=(10, 0))

        self.add_file = ct.CTkButton(self.actions, text="Sobre", command=self.about, fg_color="#263744")
        self.add_file.grid(row=3, column=0, padx=10, pady=10)

        self.items_list = []

        self.last_row = 0
        self.refresh_items_list()

    def append_item_on_list(self, filepath, key, is_binary):
        new_item = Items(self.keys, filepath, key, self.file_register, is_binary)
        new_item.grid(row=self.last_row, column=0, sticky="ew")
        self.items_list.append(new_item)
        self.last_row += 1

    def encrypt_file(self):
        support = ('*.png', '*.jpg', '*.jpeg', '*.mp4', '*.mp3', '*.doc', '*.docx', '*.odt', '*.zip', '*.pptx',
                   '*.xlsx', '*.txt', '*.html', '*.css', '*.xhtml', '*.py', '*.c', '*.cpp', '*.json', '*.md', '*.sh',
                   '*.cs')

        filepath = tkinter.filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[("Arquivos suportados", support), ]
        )
        if not filepath:
            return

        if filepath in self.file_register.json_register.keys():
            user_file_replace = tkinter.messagebox.askyesno(
                "Informações repetidas:",
                "Já há outro arquivo nesse diretório com esse nome registrado. Deseja substituí-lo?",
            )
            if user_file_replace:
                self.file_register.pop(filepath)
                self.clear_items_list()

        key = encrypt.generatekey()
        is_binary = self.file_register.is_binary(filepath)
        if filepath and is_binary:
            with open(filepath, 'rb') as file:
                encrypt.encrypt_file(file, key, (filepath + ".encrypt"), False)
        elif filepath and not is_binary:
            with open(filepath, 'r') as file:
                encrypt.encrypt_file(file, key, (filepath + ".encrypt"))
        self.file_register[filepath] = [key.decode(), is_binary]
        self.append_item_on_list(filepath, key.decode(), is_binary)

    def refresh_items_list(self):
        if self.file_register:
            for filepath in self.file_register.json_register:
                self.append_item_on_list(
                    filepath,
                    self.file_register.json_register[filepath][0],
                    self.file_register.json_register[filepath][1]
                )

    def clear_items_list(self):
        self.last_row = 0
        for item in self.items_list:
            item.destroy()

    def about(self):
        about_window_instance = AboutWindow()
        about_window_instance.mainloop()
