from common.domain import make_service

# Mapping keys (ClearOps_App/app/column_mapping.json) owned by this service.
TABLES = {"Project", "ProjectWBS", "ProjectEstimator", "ProjectSTP", "ProjectSTPSetting", "SalesforceOpportunity", "OTLTimecard", "ProjectTimecard"}

app = make_service("project-service", TABLES)
