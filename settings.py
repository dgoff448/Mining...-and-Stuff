


class Settings:

    def __init__(self):
        self.autoSave = False


# GETTERS / SETTERS *****************
    def getAutoSave(self):
        return self.autoSave

    def setAutoSave(self, boolean):
        self.autoSave = boolean