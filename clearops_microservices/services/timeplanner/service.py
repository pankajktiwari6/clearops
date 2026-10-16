from common.domain import make_service

# Mapping keys (ClearOps_App/app/column_mapping.json) owned by this service.
TABLES = {"ProjectTimePlanner", "Team", "TimeOff", "WorkdayEmployeeTimeOff"}

app = make_service("timeplanner-service", TABLES)
