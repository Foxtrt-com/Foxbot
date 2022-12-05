class MessageEqUser:
    def __init__(self, user):
        self.user = user

    def check(self, message):
        if message.author.mention == self.user:
            return True
        else:
            return False
