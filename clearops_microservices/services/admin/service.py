from common.domain import make_service

# Mapping keys (ClearOps_App/app/column_mapping.json) owned by this service.
TABLES = {"AdminIntegrationStatus", "Role", "User", "Page", "Access", "Permission", "Login", "Log", "UserLogin"}

app = make_service("admin-service", TABLES)
