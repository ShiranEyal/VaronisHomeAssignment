from abc import abstractmethod

# Abstract misconfiguration class
class MisconfigurationChecker:
    # Abstract method that ensures each checker implements checkForMisconfiguration function
    @abstractmethod
    def checkForMisconfiguration(self):
        pass

    # Abstract method that ensures each checker implements handleFoundMisconfiguration function
    @abstractmethod
    def handleFoundMisconfiguration(self):
        pass