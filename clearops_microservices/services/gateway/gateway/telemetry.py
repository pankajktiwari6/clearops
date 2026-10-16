import os


def setup_telemetry() -> None:
    """Send traces/logs to Azure Monitor / Log Analytics when configured."""
    if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        from azure.monitor.opentelemetry import configure_azure_monitor

        configure_azure_monitor()
