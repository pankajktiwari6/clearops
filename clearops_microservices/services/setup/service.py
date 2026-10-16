from common.domain import make_service

# Mapping keys (ClearOps_App/app/column_mapping.json) owned by this service.
TABLES = {"Resource", "LOB", "Grade", "FXRate", "RateCard", "Holiday", "Passthrough", "Employee"}

app = make_service("setup-service", TABLES)
