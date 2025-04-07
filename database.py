import sqlite3

class DatabaseThat:
    def __init__(self, filename):
        """Initialisiert die Datenbank mit dem gegebenen Dateinamen."""
        self.__filename = filename  
        self.__conn = None  
        self.__cursor = None  

    def open_database(self):
        """Öffnet die Datenbank, erstellt die Tabelle (falls nicht vorhanden) und speichert Verbindung und Cursor."""
        self.__conn = sqlite3.connect(self.__filename)
        self.__cursor = self.__conn.cursor()
        
        # Tabelle erstellen, falls sie nicht existiert
        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS token_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            model TEXT,
            vendor TEXT
        )
        """)
        self.__conn.commit()

    def add_token_usage(self, prompt_tokens, completion_tokens, model, vendor):
        """Fügt einen neuen Eintrag in die token_usage-Tabelle ein."""
        if not self.__conn or not self.__cursor:
            raise Exception("Datenbank ist nicht geöffnet. Rufe zuerst open_database() auf.")

        
        self.__cursor.execute("""
        INSERT INTO token_usage (prompt_tokens, completion_tokens, model, vendor)
        VALUES (?, ?, ?, ?)
        """, (prompt_tokens, completion_tokens, model, vendor))
        
        self.__conn.commit()

    def show_all_usages(self):
        """Gibt alle Einträge in der token_usage-Tabelle aus."""
        if not self.__conn or not self.__cursor:
            raise Exception("Datenbank ist nicht geöffnet. Rufe zuerst open_database() auf.")
        
        self.__cursor.execute("SELECT * FROM token_usage")
        rows = self.__cursor.fetchall()
        
        for row in rows:
            print(row)

    def sum_tokens_for_model(self, model_name):
        """Summiert die Tokens für ein bestimmtes Modell und gibt das Ergebnis aus."""
        if not self.__conn or not self.__cursor:
            raise Exception("Datenbank ist nicht geöffnet. Rufe zuerst open_database() auf.")

        self.__cursor.execute("""
        SELECT 
            SUM(prompt_tokens) AS total_prompt_tokens,
            SUM(completion_tokens) AS total_completion_tokens
        FROM token_usage
        WHERE model = ?
        """, (model_name,))

        result = self.__cursor.fetchone()

        if result:
            print(f"Summe der Tokens für {model_name}:")
            print(f"Prompt Tokens: {result[0] if result[0] is not None else 0}")
            print(f"Completion Tokens: {result[1] if result[1] is not None else 0}")
        else:
            print(f"Keine Einträge für {model_name} gefunden.")

    def close_database(self):
        """Schließt die Verbindung zur Datenbank."""
        if self.__cursor:
            self.__cursor.close()
            self.__cursor = None
        if self.__conn:
            self.__conn.close()
            self.__conn = None

    def __del__(self):
        """Destructor, um sicherzustellen, dass die Verbindung geschlossen wird."""
        self.close_database()
        print("close database")

        #https://chatgpt.com/share/67f40bca-c6b4-8008-be73-eded6d31edc0
        #erstllen tabelle und price

        

        




