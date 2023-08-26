from gloom.gloom import GloomObject, GloomAffinity
from gloom.gloom import GloomValue, GloomNothing, GloomPointer

from math import isclose

def test_default_object_affinity_is_nothing():
    o = GloomObject()
    assert o.value.affinity == GloomAffinity.NOTHING
    assert o.value.value == None
    assert o.location == GloomPointer(0)


def test_initializing_two_objects_at_same_location_overwrites_the_first():
    location = GloomPointer(0)
    o = GloomObject(location=location)
    o2 = GloomObject(location=location)
    assert o is o2
    assert len(GloomObject.objects) == 1


def test_initializing_two_objects_at_different_locations_does_the_right_thing():
    first_location = GloomPointer(0)
    o = GloomObject(location=first_location)
    second_location = GloomPointer(1)
    o2 = GloomObject(location=second_location)
    assert o is not o2
    assert len(GloomObject.objects) == 2


def test_referencing_an_object_changes_its_refcount():
    """ Also, if there's only one object and it has been referenced
        then its popularity score is 1
    """
    o = GloomObject()
    print(o)
    print(o)
    print(o)
    assert o.references == 3
    assert isclose(o.popularity_score, 1)


def test_move_to_new_location_does_the_right_thing():
    old_location = GloomPointer(12)
    o = GloomObject(location=old_location)
    new_location = GloomPointer(24)
    o.move(new_location)
    assert o.location == new_location
    assert old_location not in GloomObject.objects
    assert GloomObject.objects[new_location] is o