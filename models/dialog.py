class Dialog():
    
    def __init__(self, location, content, timed, time_limit, scene):
        self.location = location
        self.content = content
        self.timed = timed
        self.time_limit = time_limit
        self.frame_count = 0
        self.scene = scene

    def increment(self):
        self.frame_count += 1;

