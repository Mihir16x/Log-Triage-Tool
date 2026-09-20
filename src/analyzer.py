from collections import Counter, defaultdict
from datetime import datetime, timedelta


def count_levels(logs: list[dict]) -> dict:
    counts = Counter(log["level"] for log in logs)

    return {
        "INFO": counts.get("INFO", 0),
        "WARN": counts.get("WARN", 0),
        "ERROR": counts.get("ERROR", 0),
    }


def errors_by_service(logs: list[dict]) -> dict:
    error_counts = Counter(
        log["service"]
        for log in logs
        if log["level"] == "ERROR"
    )

    return dict(error_counts)


def error_rate_by_service(logs: list[dict]) -> dict:
    total_by_service = Counter()
    errors_by_service_count = Counter()

    for log in logs:
        service = log["service"]
        total_by_service[service] += 1

        if log["level"] == "ERROR":
            errors_by_service_count[service] += 1

    rates = {}

    for service, total in total_by_service.items():
        error_count = errors_by_service_count[service]
        rates[service] = error_count / total

    return rates


def detect_error_spikes(
    logs: list[dict],
    window_minutes: int = 2,
    minimum_errors: int = 3
) -> list[dict]:
    errors_by_service_map = defaultdict(list)

    for log in logs:
        if log["level"] != "ERROR":
            continue

        timestamp = log["timestamp"]

        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        errors_by_service_map[log["service"]].append(timestamp)

    spikes = []

    for service, timestamps in errors_by_service_map.items():
        timestamps.sort()

        for index, start_time in enumerate(timestamps):
            window_end = start_time + timedelta(minutes=window_minutes)

            errors_in_window = [
                timestamp
                for timestamp in timestamps[index:]
                if timestamp <= window_end
            ]

            if len(errors_in_window) >= minimum_errors:
                spikes.append(
                    {
                        "service": service,
                        "start_time": start_time,
                        "end_time": errors_in_window[-1],
                        "error_count": len(errors_in_window),
                    }
                )

                break

    return spikes