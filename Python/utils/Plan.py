class Plan():
    def __init__(self, plan):
        self.plan = plan
        self.last_ind = None

    def get_solution(self, t):
        tid_sum = 0
        for ind, steg in enumerate(self.plan):
            tid_sum+=steg["tid"]
            if t < tid_sum:
                return steg["x"], steg["y"], ind
        return None, None, len(self.plan)-1