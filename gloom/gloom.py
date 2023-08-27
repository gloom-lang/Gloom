from collections.abc import Iterable
from datetime import datetime
from enum import Enum

from types import MethodType as register_method
from typing import Callable

from gloom.hub import GloomHub

from sys import maxsize as MAXINT
from sys import float_info

MAXFLOAT = float_info.max

def refmany(to_reference):
    to_reference = list(to_reference)
    for location in to_reference:
        o = GloomObject.objects.get(location)
        o.references += 1


def refall():
    refmany(GloomObject.objects.objects)



class GloomHub:
    """ This is a funny abstraction that we're using to represent virtual memory
        For right now, to keep things dead simple while we work out the core semantics,
        this is a key-value pair mapping memory locations to objects that can receive messages
        Eventually this will be a bytearray or similar, which will require more tedious pointer
        arithmetic to work with, and also closely resemble the on-disk format to be used for
        images
    """

    def __init__(self):
        self.objects = {}


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
    SOMETHING = "something"
    REFERENCE = "reference"


    def __repr__(self):
        return self.value


    def __str__(self):
        return f"({self.value})"


class GloomValue:

    def __init__(self, value=None, affinity=GloomAffinity.NOTHING):
        assert affinity is not None
        self.value = value
        self.affinity = affinity

    def __repr__(self):
        value = self.value
        affinity = self.affinity
        return f"{type(self).__name__}({value=}, {affinity=})"
    

    def __str__(self):
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
    

class GloomEverything(GloomValue):

    def __init__(self):
        super().__init__("*", affinity=GloomAffinity.EVERYTHING)


class GloomSomething(GloomValue):
    def __init__(self, value):
        super().__init__(value, affinity=GloomAffinity.SOMETHING)
    

class GloomNothing(GloomValue):

    def __init__(self, value=None):
        super().__init__(None, affinity=GloomAffinity.NOTHING)
        self.value = value
    

class GloomPointer(GloomValue):

    def __init__(self, value):
        super().__init__(value, affinity=GloomAffinity.REFERENCE)


    def dereference(self):
        derefed = GloomObject.objects.get(self)
        if derefed is None:
            return GloomObject()
        return derefed
    

    def outcome_affinity(self, left, right):
        """
        In Gloom, the affinities determine (roughly) what type is returned by
        a binary operation. The outcome of all operations is modeled by this table:
                 
                    EVERYTHING  SOMETHING   NOTHING    REFERENCE   
        EVERYTHING  EVERYTHING  SOMETHING   NOTHING    REFERENCE
        SOMETHING   SOMETHING   SOMETHING   NOTHING    REFERENCE   
        NOTHING     NOTHING     NOTHING     NOTHING    NOTHING
        REFERENCE   REFERENCE   REFERENCE   NOTHING    REFERENCE

        e.g. NOTHING (+) (any other type) = NOTHING
        where (+) is an abstract operation, whereas
             EVERYTHING (+) A = A
        where A is any other affinity except for EVERYTHING.
        """
        match (left, right):
            case _ if left == right:
                return left
            case (GloomAffinity.NOTHING, _) | (_, GloomAffinity.NOTHING):
                return GloomAffinity.NOTHING
            case (GloomAffinity.EVERYTHING, T) | (T, GloomAffinity.EVERYTHING):
                return T
            case (GloomAffinity.SOMETHING, GloomAffinity.REFERENCE) | (GloomAffinity.REFERENCE, GloomAffinity.SOMETHING):
                return GloomAffinity.REFERENCE
            case _:
                raise ValueError(
                    "Received a weird type combination "
                    "when trying to figure out the outcome "
                    f"affinity: ({left}, {right})\n"
                    "Gloom operations support any pairs of the following valid affinities:\n"
                    "{"
                    ""
                )
            

    def type_converters_something(self, datatype):
        return {
            str: str,
            dict: lambda v: {v.value: v.value},
            int: int,
            float: float,
            bool: bool,
            type(None): lambda v: None
        }[datatype]
    

    def type_converters_everything(self, datatype):
        all_unicode = lambda _: ''.join(chr(i) for i in range(0x10FFFF))
        return {
            str: all_unicode,
            dict: lambda _: {k:v for k, v in zip(all_unicode(), range(0x10FFFF))},
            int: lambda _: MAXINT,
            float: lambda _: MAXFLOAT,
            bool: lambda _: MAXINT,
            type(None): lambda _: 0
        }[datatype]
    

    def bottom_value_datatype(self, datatype):
        if datatype in (int, float, bool):
            return 0
        elif datatype == str:
            return ""
        elif datatype == dict:
            return {}
        elif datatype is type(None):
            return None


    def type_converters_nothing(self, datatype):
        return lambda _: None


    def try_convert(self, value, datatype, target_affinity):
        value.affinity = target_affinity
        type_converter = {
            GloomAffinity.EVERYTHING: self.type_converters_everything,
            GloomAffinity.SOMETHING: self.type_converters_something,
            GloomAffinity.REFERENCE: self.type_converters_something,
            GloomAffinity.NOTHING: self.type_converters_nothing
        }[target_affinity](datatype)
        try:
            value.value = type_converter(value)
        except TypeError:
            value.value = self.bottom_value_datatype(datatype)

            

    def fix_affinities(self, other):
        """ 
        
        1:nothing + 'hi':T
        outcome: nothing wins, so + does nothing. poison 'hi' and return GloomNothing()

        1:everything + 'hi':something
        outcome: something wins
        convert 1 to string
        if we can't, then turn 1 into emptystring
        set its value to something
        """
        pass



    def __add__(self, other):
        affinity = self.outcome_affinity(self.affinity, other.affinity)

        



        

    def __repr__(self):
        return f"(#{self.value})"



def default_receiver(self, sender, method_name, *args, **kwargs):
    identity = lambda *args, **kwargs: args, kwargs
    return identity(*args, **kwargs)





class GloomObject:

    objects = GloomHub()


    def __new__(cls,  *args, **kwargs):
        location = kwargs.get('location')

        # If a new message is created at the same location, we return that object
        if (o := cls.objects.get(location)):
            return o
        
        # If not, we create a new object!
        return super(GloomObject, cls).__new__(cls)


    def __init__(self, name=None, value=GloomNothing(), methods=None, receiver=default_receiver, selector="anonymous", location=GloomPointer(0)):
        self.name = name or "anonymous"
        self.references = 0
        self.created_at = datetime.now()
        self.methods = methods or {}
        self.objects = GloomHub()
        self.receiver = receiver
        self.value = value
        self.updated_at = datetime.now()
        self.last_referenced = datetime.now()
        self._location = location
        self.objects.store(self._location, self)
        self.inbox = []
        self.outbox = []
        self.stack = []
        self.selector = selector
        self.listening = False


    def listen(self):
        self.listening = True


    def handle_unary_message(self, selector):
        if (m := self.methods.get(selector)) is not None:
            return m(self)

    
    def handle_keyword_message(self, message):
        selector = ":".join(message.keys())
        print(selector)
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
    def clone(self, location=GloomPointer(0)):
        o = GloomObject(receiver=self.receiver, location=location)
        o.references = self.references
        o.value = self.value
        o.created_at = self.created_at
        o.updated_at = self.updated_at
        o.last_referenced = self.last_referenced
        o.methods = self.methods
        return o
    

    @classmethod
    def global_references(cls):
        return cls.objects.global_references
    

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