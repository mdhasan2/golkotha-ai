
from app.container import MonitoringContainer
from presentation.monitoring_dashboard import (
    MonitoringDashboard,
)

def render_monitoring_section(
    container: MonitoringContainer,
) -> None:
    dashboard = MonitoringDashboard(
        repository=container.repository,
    )

    dashboard.render()