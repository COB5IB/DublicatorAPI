from flask import Flask, render_template, request, redirect, url_for
from duplicator_runner import DuplicatorManager

app = Flask(__name__)
manager = DuplicatorManager()

# Bu örnekte sadece 2 port: 9401 ve 9402. İleride 9410'a kadar çoğaltılabilir.
PORTS = [9401, 9402]

@app.route("/", methods=["GET"])
def index():
    statuses = {}
    for port in PORTS:
        statuses[port] = {
            'running': manager.is_running(port),
            'targets': manager.get_targets(port)
        }
    return render_template("control.html", ports=PORTS, statuses=statuses)

@app.route("/control", methods=["POST"])
def control():
    port = int(request.form.get("port"))
    action = request.form.get("action")
    targets = request.form.get("targets", "")

    if action == "start":
        manager.start(port, targets)
    elif action == "stop":
        manager.stop(port)

    return redirect(url_for("index"))

@app.route("/logs/<int:port>")
def logs(port):
    log_path = f"logs/duplicator_{port}.log"
    try:
        with open(log_path, "r") as f:
            content = f.readlines()[-100:]
    except FileNotFoundError:
        content = ["Log bulunamadı"]
    return render_template("logs.html", port=port, logs=content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
