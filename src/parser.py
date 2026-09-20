import re
from datetime import datetime


LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(?P<level>INFO|WARN|ERROR) "
    r"(?P<service>[\w-]+) "
    r"(?P<message>.+)$"
)


def parse_log_line(line: str) -> dict:
    match = LOG_PATTERN.match(line.strip())

    if not match:
        raise ValueError(f"Invalid log format: {line}")

    return {
        "timestamp": datetime.strptime(
            match.group("timestamp"),
            "%Y-%m-%d %H:%M:%S"
        ),
        "level": match.group("level"),
        "service": match.group("service"),
        "message": match.group("message"),
    }


def parse_log_file(file_path: str) -> list[dict]:
    parsed_logs = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                parsed_logs.append(parse_log_line(line))
            except ValueError as exc:
                print(f"Skipping line {line_number}: {exc}")

    return parsed_logs