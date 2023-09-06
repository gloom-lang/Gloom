from gloom.gloom import GloomObject
from gloom.gloom import GloomValue, GloomPointer
from gloom.gloom import GloomAffinity

class GloomMessage(GloomObject):

    def __init__(self, affinity, selector, arguments):
        super().__init__(None, affinity=GloomAffinity.NOTHING)
        self.selector = selector
        self.arguments = arguments
        self.created_at = datetime.now()
        self.sent_at = None
        self.last_read = None


    def send(self, sender, recipient):
        assert isinstance(recipient, GloomObject)
        self.recipient.inbox.append(
            self
        )
        

    def __repr__(self):
        pass



v = GloomValue("hello world", GloomAffinity.NOTHING)
print_ = GloomObject(v, location=GloomPointer(1))
