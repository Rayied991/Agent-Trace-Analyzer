import json
from pathlib import Path

DB_FILE = Path("history.json")


def load_history():
    if not DB_FILE.exists():
        return []

    return json.loads(
        DB_FILE.read_text(
            encoding="utf-8"
        )
    )


def save_report(report):
    
    reports_dir = Path("reports")

    reports_dir.mkdir(
        exist_ok=True
    )

    report_id = report["report_id"]

    report_path = (
        reports_dir
        / f"{report_id}.json"
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )
    history = load_history()

    history.append(report)

    DB_FILE.write_text(
        json.dumps(
            history,
            indent=2,
        ),
        encoding="utf-8",
    )