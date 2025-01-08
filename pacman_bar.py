from time import sleep, time
from threading import Thread, Event

class PacmanBar:
    def __init__(self, duration: int = 5, step_time: float = 0.3, interval: int = 3):
        self.duration = duration if duration > 0 else 5
        self.step_time = step_time if step_time > 0 else 0.3
        self.interval = interval if interval > 0 else 3
        self.step_count = int(self.duration / (self.step_time * self.interval))
        self.load_thread = None
        self._stop_flag = Event()

    def start(self):
        if not self.load_thread:
            self.load_thread = Thread(target=self.__print_pacman_bar,
                                                name="PacmanBar")
        if self.load_thread.is_alive():
            return

        self._stop_flag.clear()
        self.load_thread.start()

    def stop(self):
        if self.load_thread and self.load_thread.is_alive():
            self._stop_flag.set()
            self.load_thread.join()

    def __print_pacman_bar(self):
        unit = " " * (self.interval - 1) + "o"
        bar = unit * self.step_count

        length = len(bar)
        C = "\033[93mC\033[0m"
        c = "\033[93mc\033[0m"
        start_time = time()

        while not self._stop_flag.is_set():
            i = 0
            while i < length and not self._stop_flag.is_set():
                current_time = time() - start_time
                minutes, seconds = divmod(int(current_time), 60)
                timer_display = f"{minutes:02}:{seconds:02}"
                print(timer_display, end=" ")

                bar_list = list(bar)
                bar_list[i] = C if not bar[i] == "o" else c
                print("[", end="")
                print("-" * i, end="")
                print("".join(bar_list[i:]), end="")
                print("]", end="")

                sleep(self.step_time)
                print(end="\r")
                i += 1

        current_time = time() - start_time
        minutes, seconds = divmod(int(current_time), 60)
        timer_display = f"{minutes:02}:{seconds:02}"
        print(f"Success, elapsed time: {timer_display}")