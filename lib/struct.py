class query:
    def __init__(self, name, ref, preview, priority = 0):
        self.name = name
        self.ref = ref
        self.preview = preview
        self.priority = priority
    
    def show(self):
        print(self.name)
    
    