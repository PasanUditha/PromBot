from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

PROMETHEUS_URL = "http://62.146.176.245:9090"

def query_prometheus(metric, start, end, step="60s"):
    url = f"{PROMETHEUS_URL}/api/v1/query_range"
    params = {
        "query": metric,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "step": step
    }
    response = requests.get(url, params=params)
    return response.json()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        environment = request.form["environment"]
        start_time = datetime.fromisoformat(request.form["start_time"])
        end_time = datetime.fromisoformat(request.form["end_time"])
        metrics = request.form.getlist("metrics")

        results = []
        for metric in metrics:
            data = query_prometheus(metric, start_time, end_time)
            results.append({
                "name": metric,
                "data": data
            })

        return render_template(
            "report.html",
            environment=environment,
            start=start_time,
            end=end_time,
            results=results
        )

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
