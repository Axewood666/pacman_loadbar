from time import sleep, time
from threading import Thread, Event

class PacmanBar:
    def __init__(self, step_time: float = 0.3, interval: int = 3, duration: int = 0, pause: bool = False):
        self.duration = duration if duration > 0 else 0
        self.pause = pause
        self.step_time = step_time if step_time > 0 else 0.3
        self.interval = interval if interval > 0 else 3
        total_steps = self.duration / self.step_time
        self.step_count = int(total_steps / self.interval + 0.5)
        self.load_thread = None
        self.success = True
        self._stop_flag = Event()

    def start(self):
        if not self.load_thread:
            self.load_thread = Thread(target=self.__print_pacman_bar,
                                                name="PacmanBar")
        if self.load_thread.is_alive():
            return

        self._stop_flag.clear()
        self.load_thread.start()
        if self.pause:
            sleep(self.duration)

    def stop(self, success: bool = True):
        if self.load_thread and self.load_thread.is_alive():
            if not success:
                self.success = False
            self._stop_flag.set()
            self.load_thread.join()


    def __print_pacman_bar(self):
        unit = " " * (self.interval - 1) + "o"
        bar = unit * (self.step_count if self.step_count > 0 else 5)
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
                print(timer_display, end=" ", flush=True)

                bar_list = list(bar)
                bar_list[i] = C if not bar[i] == "o" else c
                print("[", end="", flush=True)
                print("-" * i, end="", flush=True)
                print("".join(bar_list[i:]), end="", flush=True)
                print("]", end="", flush=True)

                sleep(self.step_time)
                print(end="\r", flush=True)
                i += 1
                time_is_over = (time() - start_time > self.duration) \
                    if self.duration != 0 else False
                if time_is_over:
                    self._stop_flag.set()

        current_time = time() - start_time
        minutes, seconds = divmod(int(current_time), 60)
        timer_display = f"{minutes:02}:{seconds:02}"
        if not self.pause:
            result_mes = "Success!" if self.success else "Failed!"
            print(f"{result_mes} Elapsed time: {timer_display}    ")