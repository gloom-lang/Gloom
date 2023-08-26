import copy

from datetime import datetime
from enum import Enum


from types import MethodType as register_method


def ref(func):
    def wrapper(*args, **kwargs):
        assert len(args) > 0
        maybe_object = args[0]
        assert isinstance(maybe_object, GloomObject)
        maybe_object.references += 1
        maybe_object.last_referenced = datetime.now()
        return func(*args, **kwargs)
    return wrapper


class GloomAffinity(Enum):

    NOTHING = "nothing"
    EVERYTHING = "everything"
    REFERENCE = "reference"


    def __repr__(self):
        return f"({self.value})"


class GloomValue:

    def __init__(self, value=None, affinity=GloomAffinity.NOTHING):
        assert affinity is not None
        self.value = value
        self.affinity = affinity

    def __repr__(self):
        return f"{self.value or '(nothing)'} (affinity: {self.affinity.value})"
    

    def __hash__(self):
        return hash((self.value, self.affinity))


    def __eq__(self, other):
        if isinstance(other, GloomValue):
            return self.value == other.value
        return self.value == other


    def is_nothing(self):
        return self.affinity == GloomAffinity.NOTHING
    

    def is_everything(self):
        return self.affinity == GloomAffinity.EVERYTHING
    

    def is_reference(self):
        return self.affinity == GloomAffinity.REFERENCE
    

class GloomNothing(GloomValue):

    def __init__(self, value=None):
        super().__init__(None, affinity=GloomAffinity.NOTHING)
        self.value = value
    

class GloomPointer(GloomValue):

    def __init__(self, value):
        super().__init__(value, affinity=GloomAffinity.REFERENCE)


    def dereference(self):
        derefed = GloomObject.objects.get(self.value)
        if derefed is None:
            return GloomObject()
        

    def __repr__(self):
        return f":{self.value}:"


@ref
def default_receiver(self, sender, method_name, *args, **kwargs):
    identity = lambda *args, **kwargs: args, kwargs
    return identity(*args, **kwargs)


class GloomObject:

    objects = {}

    def __new__(cls,  *args, **kwargs):
        location = kwargs.get('location')

        if (o := cls.objects.get(location)):
            return o
        
        return super(GloomObject, cls).__new__(cls)


    def __init__(self, value=GloomNothing(), receiver=default_receiver, location=GloomPointer(0)):
        self.references = 0
        self.created_at = datetime.now()
        self.methods = {}
        self.receiver = receiver
        self.value = value
        self.updated_at = datetime.now()
        self.last_referenced = datetime.now()
        self._location = location
        self.objects[self._location] = self
        self.inbox = []
        self.outbox = []



    @property
    def location(self):
        return self._location
    


    @location.setter
    @ref
    def location(self, location):
        del self.objects[self._location]
        self._location = location
        self.objects[self.location] = self


    @ref
    def move(self, new_location):
        self.location = new_location


    @ref
    def clone(self):
        o = GloomObject(receiver=self.receiver)
        o.references = self.references
        o.value = self.value
        o.created_at = self.created_at
        o.updated_at = self.updated_at
        o.last_referenced = self.last_referenced
        o.methods = self.methods
        return o



    @ref
    def __repr__(self):
        return f"""
        gloom object @ {self.location}: {self.value}
            - popularity: {self.popularity_score} (across {self.object_count()} total objects)
            - references: {self.references} (out of {self.global_references} total references globally)
            - created at: {self.created_at}
            - last referenced: {self.last_referenced}
            - updated at: {self.updated_at}
        """


    def receive_message(self, message):
        args = message.get("args",())
        kwargs = message.get("kwargs", {})
        args, kwargs = default_receiver(*args, **kwargs)
        return 


    @property
    def global_references(self):
        total = 0
        for obj_id in self.objects:
            total += self.objects[obj_id].references
        return total


    @property
    def popularity_score(self):
        try:
            return self.references / self.global_references 
        except ZeroDivisionError:
            return 0
    

    def free(self):
        self.objects.pop(self.location, None)


    def free_all(self):
        """ Note we iterate over keys() explicitly here since Python dictionaries cannot be modified
            while being iterated over without encountering a runtime exception
        """
        keys = list(self.objects.keys())
        for key in keys:
            self.objects.pop(key, None)
            


    @classmethod
    def object_count(cls):
        return len(cls.objects)


class GloomMessage(GloomObject):

    def __init__(self, affinity, selector, arguments):
        super().__init__(None, affinity=GloomAffinity.NOTHING)
        self.selector = selector
        self.arguments = arguments
        self.created_at = datetime.now()
        self.sent_at = None
        self.last_read = None


    def send(self, recipient):
        assert isinstance(recipient, GloomObject)
        self.recipient.inbox.append(
            self
        )
        