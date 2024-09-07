import sys
import time
import threading

STOPPING = False


class ByteCounter:
    def __init__(self):
        self.byte_count = 0
        self.start_time = None
        self.lock = threading.Lock()

    def increment(self, count):
        with self.lock:
            if self.start_time is None:
                self.start_time = time.time()
            self.byte_count += count

    def get_stats(self):
        with self.lock:
            if self.start_time is None:
                return 0, 0, 0
            elapsed_time = time.time() - self.start_time
            speed = self.byte_count / elapsed_time if elapsed_time > 0 else 0
            return self.byte_count, elapsed_time, speed


def print_stats(counter):
    try:
        while True:
            time.sleep(1)
            bytes_count, elapsed_time, speed = counter.get_stats()
            sys.stderr.write(
                f"\rBytes: {bytes_count}, Time: {elapsed_time:.2f}s, Speed: {speed:.2f} B/s"
            )
            sys.stderr.flush()
            if STOPPING:
                break
    except KeyboardInterrupt:
        pass


def main():
    global STOPPING
    counter = ByteCounter()
    stats_thread = threading.Thread(target=print_stats, args=(counter,), daemon=True)
    stats_thread.start()

    while True:
        chunk = sys.stdin.buffer.read(4096)
        if not chunk:
            break
        counter.increment(len(chunk))
        sys.stdout.buffer.write(chunk)
        sys.stdout.buffer.flush()

    STOPPING = True
    stats_thread.join()
    sys.stderr.write("\n")


if __name__ == "__main__":
    main()
