# agents/utils/memory.py

class Memory:
    """
    Einfaches zentrales Memory für die Plattform.
    Alle Agenten können hier Daten speichern und abrufen.
    """
    def __init__(self):
        self.storage = {}

    def set(self, key, value):
        self.storage[key] = value

    def get(self, key, default=None):
        return self.storage.get(key, default)

    def keys(self):
        return list(self.storage.keys())
