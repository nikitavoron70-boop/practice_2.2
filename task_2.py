import psutil
import time
import os


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent


def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent


class SystemMonitor:
    def __init__(self):
        self.cpu_percent = 0
        self.memory_percent = 0
        self.disk_percent = 0

    def update(self):
        self.cpu_percent = get_cpu_usage()
        self.memory_percent = get_memory_usage()
        self.disk_percent = get_disk_usage()

    def display(self):
        self.update()

        print("\n" + "=" * 50)
        print("СИСТЕМНЫЙ МОНИТОР")
        print("=" * 50)

        print(f"Загрузка CPU: {self.cpu_percent:.1f}%")
        print(f"Использование RAM: {self.memory_percent:.1f}%")
        print(f"Загрузка диска: {self.disk_percent:.1f}%")

        print("=" * 50)

    def run_monitor(self, interval=2):
        try:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                self.display()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\nМониторинг остановлен")


def main():
    monitor = SystemMonitor()

    print("Системный монитор запущен")
    print("Нажмите Ctrl+C для выхода\n")
    time.sleep(2)

    monitor.run_monitor()


if __name__ == "__main__":
    main()