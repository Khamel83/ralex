class PatternLearner:
    def __init__(self):
        self.patterns = {}

    def learn(self, session_id: str, data: dict):
        if session_id not in self.patterns:
            self.patterns[session_id] = []
        self.patterns[session_id].append(data)

    def get_patterns(self, session_id: str):
        return self.patterns.get(session_id, [])