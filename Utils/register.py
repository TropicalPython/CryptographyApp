import os, json
from selectors import SelectSelector


class Register:
    def __init__(self):
        self.json_register = {}

    def append(self, filepath, data, is_text=True):
        self.json_register[filepath] = data

    def __setitem__(self, key, value):
        self.append(key, value)

    def __getitem__(self, item):
        return self.json_register[item]

    @staticmethod
    def backup():  # Método estático criado por precaução.
        with open("./chaves", 'r') as reading:
            content = reading.read()
        with open("./chaves_backup", 'w') as writing:
            writing.write(content)

    def read_register(self):
        if os.path.exists("./chaves"):
            try:
                with open("./chaves", 'r') as keys_file:
                    self.json_register = json.loads(keys_file.read())
            except json.JSONDecodeError:
                self.backup()  # Faz nada além de um backup, e espera que o resto
                               # do código funcione por sí.

    def write_all(self):
        if not os.path.exists("./chaves"):
            with open("./chaves", "w") as keys_json:
                keys_json.write("{}")
        with open("./chaves", "w") as keys_file:
            keys_file.write(json.dumps(self.json_register))

    def pop(self, filepath):
        self.json_register.pop(filepath)

    @staticmethod
    def is_binary(filepath):
        supported_binaryes = (
            ".png", ".jpg", ".jpeg", ".mp4", ".mp3", ".doc", ".docx", ".odt", ".zip",
            ".pptx", ".xlsx", ""
        )
        extensao_de_arquivo = os.path.splitext(filepath)[1]
        return True if extensao_de_arquivo in supported_binaryes else False