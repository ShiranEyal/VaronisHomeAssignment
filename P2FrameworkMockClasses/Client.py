class Client:
    def __init__(self, id, misconfigurations):
        # identifier
        self.id = id
        # list of misconfigurations
        self.misconfigurations = misconfigurations

    # function we call every set amount of time to check our clients configurations again.
    def reviewMisconfigurations(self):
        for misconfiguration in self.misconfigurations:
            if misconfiguration.checkForMisconfiguration():
                misconfiguration.handleFoundMisconfiguration()