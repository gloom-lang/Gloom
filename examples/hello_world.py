""" Kinda sorta hello-world in Gloom
"""

from gloom.gloom import GloomObject, GloomPointer, GloomEverything, GloomSomething

everything = GloomObject(
    name="everything",
    value=GloomEverything() 
)

def new(self, new, location):
    pointer = GloomPointer(location)
    value = GloomSomething(value=new)
    o = GloomObject(
        value=value, 
        location=pointer
    )
    self.objects[location] = o
    return pointer

def add(self, to):
    return self.value.value + to


def dereference(self, dereference):
    address = dereference
    if not isinstance(dereference, GloomPointer):
        address = GloomPointer(dereference)

    if (m := self.objects.get(address)) is None:
        m = self.objects[address] = GloomObject()
    return m
        

everything.methods["new:location"] = new
everything.methods["+:to"] = add
everything.methods["add:to"] = add
everything.methods["dereference"] = dereference


if __name__ == "__main__":
    everything.listen()
    address = everything.send(
        {"new": "hello world!", "location": 1}
    )
    hello_world = everything.send(
        {"dereference": address}
    )
    hello_world.send(
        "print"
    )
