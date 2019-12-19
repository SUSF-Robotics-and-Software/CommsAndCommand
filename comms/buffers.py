class diff_buffer:
    def __init__(self):
        self.buffer = []
        self.has_changed = False

    def add(self, to_add: str):
        if to_add not in self.buffer:
            self.has_changed = True
            self.buffer.append(to_add)
        else:
            self.has_changed = False

    def clear(self):
        self.buffer = []

    def as_string(self):
        string = json.dumps(self.buffer)
        self.has_changed = False
        return string
