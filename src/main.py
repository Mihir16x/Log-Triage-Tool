from analyzer import (
    count_levels,
    detect_error_spikes,
    error_rate_by_service,
    errors_by_service,
)
from database import clear_logs, create_table, get_all_logs, insert_logs
from parser import parse_log_file


def main():
    logs = parse_log_file("data/sample.log")

    create_table()
    clear_logs()
    insert_logs(logs)

    stored_logs = get_all_logs()

    print("\n=== LOG TRIAGE REPORT ===\n")

    print(f"Total log entries: {len(stored_logs)}\n")

    level_counts = count_levels(stored_logs)

    print("Log levels:")
    for level, count in level_counts.items():
        print(f"  {level}: {count}")

    print("\nErrors by service:")
    service_errors = errors_by_service(stored_logs)

    for service, count in service_errors.items():
        print(f"  {service}: {count}")

    print("\nError rate by service:")
    error_rates = error_rate_by_service(stored_logs)

    for service, rate in error_rates.items():
        print(f"  {service}: {rate:.1%}")

    print("\nDetected error spikes:")
    spikes = detect_error_spikes(stored_logs)

    if not spikes:
        print("  No error spikes detected.")
    else:
        for spike in spikes:
            print(
                f"  {spike['service']} -> "
                f"{spike['error_count']} errors between "
                f"{spike['start_time']} and {spike['end_time']}"
            )


if __name__ == "__main__":
    main()