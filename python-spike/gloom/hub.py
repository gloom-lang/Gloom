

class GloomHub:

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
