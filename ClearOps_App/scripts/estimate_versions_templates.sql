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
        -- Only the current version is active; older versions default to 0 until a user activates them
        Is_Active        BIT            NOT NULL CONSTRAINT DF_EstVersion_IsActive DEFAULT (0),
        Activated_By     VARCHAR(100)   NULL,
        Activated_Date   DATETIME2      NULL,
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

-- Upgrade path for an existing table created before Is_Active was added
IF COL_LENGTH(N'gold.ClearOps_ProjectEstimator_Version', N'Is_Active') IS NULL
BEGIN
    ALTER TABLE gold.ClearOps_ProjectEstimator_Version ADD
        Is_Active      BIT NOT NULL CONSTRAINT DF_EstVersion_IsActive DEFAULT (0),
        Activated_By   VARCHAR(100) NULL,
        Activated_Date DATETIME2 NULL;
END
GO

-- Existing rows: the latest version of each project becomes the active one
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = N'UX_EstVersion_OneActivePerProject'
               AND object_id = OBJECT_ID(N'gold.ClearOps_ProjectEstimator_Version'))
BEGIN
    EXEC (N'UPDATE v SET Is_Active = 1
            FROM gold.ClearOps_ProjectEstimator_Version v
            WHERE Version_No = (SELECT MAX(Version_No) FROM gold.ClearOps_ProjectEstimator_Version WHERE Project_Id = v.Project_Id)');
    -- At most one active version per project
    EXEC (N'CREATE UNIQUE INDEX UX_EstVersion_OneActivePerProject
            ON gold.ClearOps_ProjectEstimator_Version (Project_Id) WHERE Is_Active = 1');
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
