from abc import abstractmethod

class MisconfigurationChecker:
    @abstractmethod
    def checkForMisconfiguration(self):
        pass

    @abstractmethod
    def handleFoundMisconfiguration(self):
        pass