from datetime import datetime, timedelta
import time

#timer py class
class py_timer():
    def __init__(self, minutes:str):
        self.start_time = datetime.now().replace(microsecond=0)
        delta_value_minutes = float(minutes)
        self.delta_value_seconds = delta_value_minutes * 60
        self.end_time = (self.start_time + timedelta(minutes=delta_value_minutes)).replace(microsecond=0)
        print(f"timer set, starting at : {self.start_time}, ending at {self.end_time}")

    # timer runs on a while loop using time's sleep function
    def run_timer(self):
        t = self.delta_value_seconds
        while t > 0:
            time.sleep(1)
            t -= 1
            print(t)

        dt = datetime.now().replace(microsecond=0)
        print(f"time now {dt}, required end time {self.end_time}")
        print(dt == self.end_time)

# for testing
if __name__ == '__main__':
   timer = py_timer("0.1")
   timer.run_timer()
