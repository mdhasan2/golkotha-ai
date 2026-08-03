from pathlib import Path

from infrastructure.monitoring.sqlite_monitoring_repository import (
    SQLiteMonitoringRepository,
)

ROOT_PATH = Path(__file__).resolve().parents[1]

DATABASE_PATH = (
    ROOT_PATH
    / "data"
    / "monitoring"
    / "monitoring.db"
)

def main() -> None:
    repository = SQLiteMonitoringRepository(
        DATABASE_PATH,
    )

    print(
        "Monitoring database initialized at: ",
        repository.database_path,
    )

if __name__ == "__main__":
    main()