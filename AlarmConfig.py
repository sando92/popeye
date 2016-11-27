class AlarmConfig():
    def __init__(self, ring=True, time_difference=0):
        self.ring = ring
        self.time_difference = time_difference

    def must_ring(self):
        return self.ring

    def get_time_diff(self):
        return self.time_difference

    @staticmethod
    def no_changes():
        return AlarmConfig()

    @staticmethod
    def add_time_diff(min):
        return AlarmConfig(True, min)

    @staticmethod
    def disable_alarm_clock():
        return AlarmConfig(False)
