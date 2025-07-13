import customtkinter as ct

class AboutWindow(ct.windows.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.wm_maxsize(300, 400)
        self.wm_minsize(300, 400)
        self.title("Sobre o software.")

        self.name_presentation_label = ct.CTkLabel(self, text="Nome do autor:", anchor="ne")
        self.name_presentation_label.pack(pady=(25, 0))

        self.name_label = ct.CTkLabel(self, text="Murilo Rib.", font=("sans-serif", 18, "bold"))
        self.name_label.pack()

        self.functionality_presentation_label = ct.CTkLabel(self, text="O que faz?:", anchor="ne")
        self.functionality_presentation_label.pack(pady=(25, 0))

        functionality_text = """
Esse é um software simples para criptografar arquivos do dia-a-dia. Criado apenas com o propósito
de apresentar minhas habilidades em Python.
        """

        self.functionality_label = ct.CTkLabel(self, text=functionality_text, font=("sans-serif", 10, "bold"), wraplength=200)
        self.functionality_label.pack()

