class query:
    def __init__(self, name, ref, preview, priority = 0):
        self.name = name
        self.ref = ref
        self.preview = preview
        self.priority = priority
    
    def show(self):
        print(self.name)

    def __lt__(self, other):
        return self.priority < other.priority
    
    def __eq__(self, other):
        return self.priority == other.priority
