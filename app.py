from flask import Flask, render_template, request, send_file, redirect, url_for, session
import os
import uuid
import io
import csv
import json
from brutalyze_core import analyze_log

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Store analysis results in memory (per session)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        use_sample = request.form.get("use_sample")
        if use_sample == "true":
            log_path = "sample_auth.log"
        else:
            uploaded_file = request.files.get("logfile")
            if not uploaded_file or uploaded_file.filename == "":
                return render_template("index.html", error="Please upload a log file or use the sample.")
            filename = str(uuid.uuid4()) + "_" + uploaded_file.filename
            log_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            uploaded_file.save(log_path)

        result = analyze_log(log_path)

        session["analysis"] = result  # store analysis in session
        return render_template(
            "result.html",
            summary=result["summary"],
            alerts=result["alerts"],
            classified=result["classified"]
        )

    return render_template("index.html")

@app.route("/download/<filetype>")
def download(filetype):
    result = session.get("analysis")
    if not result:
        return redirect(url_for("index"))

    output = io.StringIO()
    filename = f"brutalyze_{filetype}.txt"

    if filetype == "csv":
        writer = csv.writer(output)
        writer.writerow(["Timestamp", "User", "IP", "Country", "Region", "City", "Category", "Raw Log"])
        for category, logs in result["classified"].items():
            for log in logs:
                loc = log.get("location", {})
                writer.writerow([
                    log.get("timestamp", ""),
                    log.get("user", ""),
                    log.get("ip", ""),
                    loc.get("country", ""),
                    loc.get("region", ""),
                    loc.get("city", ""),
                    category,
                    log.get("raw", "")
                ])
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode("utf-8")),
                         mimetype="text/csv",
                         as_attachment=True,
                         download_name="brutalyze_report.csv")

    elif filetype == "json":
        json_output = json.dumps(result, indent=4)
        return send_file(io.BytesIO(json_output.encode("utf-8")),
                         mimetype="application/json",
                         as_attachment=True,
                         download_name="brutalyze_report.json")

    elif filetype == "alerts":
        alerts = result.get("alerts", [])
        output.write("\n".join(alerts))
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode("utf-8")),
                         mimetype="text/plain",
                         as_attachment=True,
                         download_name="brutalyze_alerts.txt")

    else:
        return "Invalid file type", 400

if __name__ == "__main__":
    app.run(debug=True)
