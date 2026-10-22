-- Estimate version history and reusable estimate templates (SQL Server).
-- Mirrors app/models/estimator_versions.py. Safe to re-run.

IF SCHEMA_ID(N'gold') IS NULL EXEC (N'CREATE SCHEMA gold');
GO

IF OBJECT_ID(N'gold.ClearOps_ProjectEstimator_Version', N'U') IS NULL
BEGIN
    CREATE TABLE gold.ClearOps_ProjectEstimator_Version (
        Version_Id       BIGINT IDENTITY(1,1) NOT NULL,
        Project_Id       VARCHAR(100)   NOT NULL,
        Version_No       INT            NOT NULL,
        Change_Summary   VARCHAR(500)   NULL,
        Line_Count       INT            NOT NULL CONSTRAINT DF_EstVersion_LineCount DEFAULT (0),
        Estimate_Total   NUMERIC(18,2)  NULL,
        Snapshot_Json    NVARCHAR(MAX)  NOT NULL,
        -- Gold audit columns (GoldAuditColumnsMixin)
        DateOfData       DATE           NULL CONSTRAINT DF_EstVersion_DateOfData DEFAULT (CAST(SYSUTCDATETIME() AS DATE)),
        GoldCreatedBy    VARCHAR(100)   NOT NULL,
        GoldCreatedDate  DATETIME2      NOT NULL CONSTRAINT DF_EstVersion_CreatedDate DEFAULT (SYSUTCDATETIME()),
        GoldModifiedBy   VARCHAR(100)   NULL,
        GoldModifiedDate DATETIME2      NULL,
        CONSTRAINT PK_ClearOps_ProjectEstimator_Version PRIMARY KEY CLUSTERED (Version_Id),
        CONSTRAINT UQ_ClearOps_ProjectEstimator_Version_Project_VersionNo UNIQUE (Project_Id, Version_No),
        CONSTRAINT CK_EstVersion_Snapshot_IsJson CHECK (ISJSON(Snapshot_Json) = 1)
    );
END
GO

IF OBJECT_ID(N'gold.ClearOps_ProjectEstimator_Template', N'U') IS NULL
BEGIN
    CREATE TABLE gold.ClearOps_ProjectEstimator_Template (
        Template_Id       BIGINT IDENTITY(1,1) NOT NULL,
        Template_Name     VARCHAR(200)   NOT NULL,
        Source_Project_Id VARCHAR(100)   NULL,
        Task_Count        INT            NOT NULL CONSTRAINT DF_EstTemplate_TaskCount DEFAULT (0),
        Template_Json     NVARCHAR(MAX)  NOT NULL,
        -- Gold audit columns (GoldAuditColumnsMixin)
        DateOfData        DATE           NULL CONSTRAINT DF_EstTemplate_DateOfData DEFAULT (CAST(SYSUTCDATETIME() AS DATE)),
        GoldCreatedBy     VARCHAR(100)   NOT NULL,
        GoldCreatedDate   DATETIME2      NOT NULL CONSTRAINT DF_EstTemplate_CreatedDate DEFAULT (SYSUTCDATETIME()),
        GoldModifiedBy    VARCHAR(100)   NULL,
        GoldModifiedDate  DATETIME2      NULL,
        CONSTRAINT PK_ClearOps_ProjectEstimator_Template PRIMARY KEY CLUSTERED (Template_Id),
        CONSTRAINT CK_EstTemplate_Content_IsJson CHECK (ISJSON(Template_Json) = 1)
    );
    CREATE INDEX IX_EstTemplate_Name ON gold.ClearOps_ProjectEstimator_Template (Template_Name);
END
GO
