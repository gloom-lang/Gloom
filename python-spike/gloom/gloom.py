from collections.abc import Iterable
from datetime import datetime
from enum import Enum

from types import MethodType as register_method
from typing import Callable

from gloom.hub import GloomHub

from sys import maxsize as MAXINT
from sys import float_info

MAXFLOAT = float_info.max



def ref(func):
    def wrapper(*args, **kwargs):
        assert len(args) > 0
        maybe_object = args[0]
        assert isinstance(maybe_object, GloomObject)
        maybe_object.references += 1
        maybe_object.last_referenced = datetime.now()
        return func(*args, **kwargs)
    return wrapper



def refmany(to_reference):
    to_reference = list(to_reference)
    for location in to_reference:
        o = GloomObject.objects.get(location)
        o.references += 1


def refall():
    refmany(GloomObject.objects.objects)


class GloomAffinity(Enum):

    NOTHING = "nothing"
    EVERYTHING = "everything"
    SOMETHING = "something"
    REFERENCE = "reference"


    def __repr__(self):
        return self.value


    def __str__(self):
        return f"({self.value})"




def default_receiver(self, sender, method_name, *args, **kwargs):
    identity = lambda *args, **kwargs: args, kwargs
    return identity(*args, **kwargs)


class GloomObject:


    def __init__(self, name=None, value=None, affinity=None, methods=None, receiver=default_receiver, selector="anonymous", location=None):
        self.name = name or "anonymous"
        self.references = 0
        self.created_at = datetime.now()
        self.methods = methods or {}
        self.objects = GloomHub()
        self.names = GloomHub()
        self.receiver = receiver
        self.value = value
        if affinity is None:
            self.affinity = GloomAffinity.NOTHING
        else:
            self.affinity = affinity
        self.updated_at = datetime.now()
        self.last_referenced = datetime.now()
        self._location = location
        self.objects.store(self._location, self)
        self.inbox = []
        self.outbox = []
        self.stack = []
        self.selector = selector
        self.listening = True
        self.auto_deref = False

    @property
    def is_nothing(self):
        return self.affinity == GloomAffinity.NOTHING
    

    @property
    def is_something(self):
        return self.affinity == GloomAffinity.SOMETHING
    
    @property
    def is_everything(self):
        return self.affinity == GloomAffinity.EVERYTHING
    
    @property
    def is_reference(self):
        return self.affinity == GloomAffinity.REFERENCE


    def listen(self):
        self.listening = True


    def handle_unary_message(self, selector):
        if (m := self.methods.get(selector)) is not None:
            return m(self)

    
    def handle_keyword_message(self, message):
        selector = ":".join(message.keys())
        if (m := self.methods.get(selector)) is not None:
            return m(self, **message)


    def handle_binary_message(self, message):
        selector, value = message
        return self.handle_keyword_message(
            {selector: selector, "to": value}
        )


    def send(self, message):
        self.inbox.append(
            message
        )

        if self.listening:
            return self.receive()


    def receive(self):

        if not self.inbox:
            return
        
        message = self.inbox.pop()

        if isinstance(message, str):
            return self.handle_unary_message(message)
        elif isinstance(message, dict):
            return self.handle_keyword_message(message)
        elif isinstance(message, tuple) and len(message) == 2:
            return self.handle_binary_message(message)
        else:
            return GloomNothing().pointer



    def print(self, message):
        return GloomObject(print(message.value.value))


    def become_everything(self):
        self.valaue.affinity = GloomAffinity.EVERYTHING


    def become_something(self):
        self.value.affinity = GloomAffinity.SOMETHING


    def become_nothing(self):
        self.value.affinity = GloomAffinity.NOTHING


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
    def clone_to(self, location):
        o = GloomObject(receiver=self.receiver, location=location)
        o.references = self.references
        o.value = self.value
        o.created_at = self.created_at
        o.updated_at = self.updated_at
        o.last_referenced = self.last_referenced
        o.methods = self.methods
        return o
    


    def global_references(self):
        return self.objects.global_references
    

    def safe_repr(self):
        return f"""
        gloom object @{self.location}: {self.value}
            - popularity: {self.popularity_score} (across {self.object_count()} total objects)
            - references: {self.references} (out of {self.global_references()} total references globally)
            - created at: {self.created_at}
            - last referenced: {self.last_referenced}
            - updated at: {self.updated_at}
        """ 


    @ref
    def __repr__(self):
        value = self.value
        receiver = default_receiver.__name__
        name = self.name
        location = self.location
        return f"GloomObject({name=}, {value=}, {receiver=}, {location=})"
    

    @ref
    def __str__(self):
        return self.safe_repr()


    def receive_message(self, message):
        args = message.get("args",())
        kwargs = message.get("kwargs", {})
        args, kwargs = default_receiver(*args, **kwargs)
        return 


    @property
    def popularity_score(self):
        try:
            return self.references / self.global_references()
        except ZeroDivisionError:
            return 0
        

    def free(self):
        self.free_location(self.location)


    def free_location(self, location):
        self.objects.pop(location, None)


    def store(self, key, value):
        self.objects[key] = value


    def free_all(self):
        """ Note we iterate over keys() explicitly here since Python dictionaries cannot be modified
            while being iterated over without encountering a runtime exception
        """
        keys = list(self.objects.keys())
        for key in keys:
            self.objects.pop(key, None)
            

    def object_count(self):
        return len(self.objects)
    

class GloomNothing(GloomObject):

    def __init__(self, value):
        super().__init__(value, affinity=GloomAffinity.NOTHING)

    def __repr__(self):
        value = self.value
        return f"GloomNothing({value=})"
    
    def __str__(self):
        return f"nothing({self.value})"
    

class GloomEverything(GloomObject):
    def __init__(self, value):
        super().__init__(value, affinity=GloomAffinity.EVERYTHING)
        self.name = "*"

    def __repr__(self):
        value = self.value
        return f"GloomEverything({value=})"
    
    def __str__(self):
        return f"everything({self.value})"
    

class GloomSomething(GloomObject):
    def __init__(self, value):
        super().__init__(value, affinity=GloomAffinity.SOMETHING)

    def __repr__(self):
        value = self.value
        return f"GloomSomething({value=})"
    
    def __str__(self):
        return f"something({self.value})"
    

class GloomPointer(GloomObject):
    def __init__(self, value):
        super().__init__(value, affinity=GloomAffinity.REFERENCE)

    def __repr__(self):
        value = self.value
        return f"GloomPointer({value=})"
    
    def __str__(self):
        return f"ref#{self.value}"
    


class GloomProperties(GloomEverything):

    def __init__(self, value):
        super().__init__(value)
        self.value = self.objects


    @property
    def size(self):
        return len(self.objects)
    

    @property
    def global_references(self):
        total = 0
        for location in self.objects:
            total += self.objects[location].references
        return total


    def free_location(self, location):
        self.objects.pop(location, None)


    def store(self, key, value):
        self.objects[key] = value


    def get(self, location, default=None):
        return self.objects.get(location, default)


    def free_all(self):
        """ Note we iterate over keys() explicitly here since Python dictionaries cannot be modified
            while being iterated over without encountering a runtime exception
        """
        keys = list(self.objects.keys())
        for key in keys:
            self.objects.pop(key, None)
            

    def __len__(self):
        return len(self.objects)
    

    def __contains__(self, key):
        return key in self.objects


    def __getitem__(self, key):
        return self.objects[key]
    

    def __setitem__(self, key, value):
        self.objects[key] = value


    def __delitem__(self, key):
        del self.objects[key]


    def keys(self):
        return self.objects.keys()
    

    def pop(self, key, default=None):
        return self.objects.pop(key, default)
    

    def __repr__(self):
        refall()
        representation = "\t"
        for key in self.objects:
            obj_repr = self.get(key).safe_repr()
            representation += f"{key} : {obj_repr}"
        return representation
