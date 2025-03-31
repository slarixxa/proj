import sqlite3

# Verbindung zur SQLite-Datenbank herstellen (erstellt die Datei, wenn sie noch nicht existiert)
conn = sqlite3.connect("token_usage.db")
cursor = conn.cursor()

# Tabelle erstellen, falls sie noch nicht existiert
cursor.execute("""
CREATE TABLE IF NOT EXISTS token_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    model TEXT,
    vendor TEXT
)
""")

# Summiere die Tokens für das Modell "gpt-4o"
cursor.execute("""
SELECT 
    SUM(prompt_tokens) AS total_prompt_tokens,
    SUM(completion_tokens) AS total_completion_tokens
FROM token_usage
WHERE model = 'gpt-4o'
""")

result = cursor.fetchone()

if result:
    print(f"Summe der Tokens für gpt-4o:")
    print(f"Prompt Tokens: {result[0]}")
    print(f"Completion Tokens: {result[1]}")
else:
    print("Keine Einträge für gpt-4o gefunden.")



# Änderungen speichern
conn.commit()

# Verbindung schließen
conn.close()
