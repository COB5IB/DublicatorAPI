import subprocess
import os

class DuplicatorManager:
    def __init__(self):
        self.processes = {}  # port -> Popen
        self.targets = {}    # port -> str

    def start(self, port, targets):
        self.stop(port)  # Aynı portta varsa önce durdur

        env = os.environ.copy()
        env["DUPLICATOR_PORT"] = str(port)
        env["TARGET_URLS"] = targets

        log_file = open(f"logs/duplicator_{port}.log", "a")

        process = subprocess.Popen(
            ["python3", "duplicator.py"],
            stdout=log_file,
            stderr=log_file,
            env=env
        )
        self.processes[port] = process
        self.targets[port] = targets

    def stop(self, port):
        process = self.processes.get(port)
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        self.processes.pop(port, None)
        self.targets.pop(port, None)

    def is_running(self, port):
        process = self.processes.get(port)
        return process and process.poll() is None

    def get_targets(self, port):
        return self.targets.get(port, "")
