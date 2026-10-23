-- STP saved queries -- ClearOps_Dev.gold.ClearOps_STP_Settings (NEW). Idempotent: safe to run more than once.
-- One row per user + filter name; Project_Ids is a JSON array of gold.Project_Master.Project_Id values,
-- e.g. N'["7078091","JPI/089/45"]'.
USE [ClearOps_Dev];
GO

IF OBJECT_ID(N'[ClearOps_Dev].[gold].[ClearOps_STP_Settings]', N'U') IS NULL
BEGIN
    CREATE TABLE [gold].[ClearOps_STP_Settings] (
        STP_Settings_Id  BIGINT IDENTITY(1,1) NOT NULL,
        User_ID          BIGINT         NOT NULL,
        Filter_Name      NVARCHAR(200)  NOT NULL,
        Project_Ids      NVARCHAR(MAX)  NOT NULL,
        GoldCreatedBy    VARCHAR(100)   NULL CONSTRAINT DF_gold_ClearOps_STP_Settings_CreatedBy DEFAULT ('ClearOpsWebApp'),
        GoldCreatedDate  DATETIME       NULL CONSTRAINT DF_gold_ClearOps_STP_Settings_CreatedDate DEFAULT (GETUTCDATE()),
        GoldModifiedBy   VARCHAR(100)   NULL,
        GoldModifiedDate DATETIME       NULL,
        CONSTRAINT PK_gold_ClearOps_STP_Settings PRIMARY KEY (STP_Settings_Id),
        CONSTRAINT FK_gold_ClearOps_STP_Settings_User FOREIGN KEY (User_ID) REFERENCES [gold].[ClearOps_Users] (User_ID),
        CONSTRAINT UQ_gold_ClearOps_STP_Settings_User_FilterName UNIQUE (User_ID, Filter_Name),
        CONSTRAINT CK_gold_ClearOps_STP_Settings_ProjectIds CHECK (ISJSON(Project_Ids) = 1),
        CONSTRAINT CK_gold_ClearOps_STP_Settings_FilterName CHECK (LEN(LTRIM(RTRIM(Filter_Name))) > 0)
    );
    -- The UNIQUE (User_ID, Filter_Name) constraint already creates an index led by User_ID,
    -- so no separate IX on User_ID is needed.
END
ELSE
BEGIN
    -- Table already exists: bring it up to the current definition (each step only runs if needed).
    -- Dynamic SQL is used so later steps compile after earlier ALTERs have added the columns.
    IF COL_LENGTH('gold.ClearOps_STP_Settings', 'User_ID') IS NULL
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD User_ID BIGINT NULL');  -- backfill, then make NOT NULL
    IF COL_LENGTH('gold.ClearOps_STP_Settings', 'Filter_Name') IS NULL
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD Filter_Name NVARCHAR(200) NOT NULL CONSTRAINT DF_gold_ClearOps_STP_Settings_FilterName_Tmp DEFAULT (N''Default'')');
    IF COL_LENGTH('gold.ClearOps_STP_Settings', 'Project_Ids') IS NULL
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD Project_Ids NVARCHAR(MAX) NOT NULL CONSTRAINT DF_gold_ClearOps_STP_Settings_ProjectIds_Tmp DEFAULT (N''[]'')');
    IF COL_LENGTH('gold.ClearOps_STP_Settings', 'GoldCreatedBy') IS NULL
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD GoldCreatedBy VARCHAR(100) NULL CONSTRAINT DF_gold_ClearOps_STP_Settings_CreatedBy DEFAULT (''ClearOpsWebApp'')');
    IF COL_LENGTH('gold.ClearOps_STP_Settings', 'GoldCreatedDate') IS NULL
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD GoldCreatedDate DATETIME NULL CONSTRAINT DF_gold_ClearOps_STP_Settings_CreatedDate DEFAULT (GETUTCDATE())');
    IF COL_LENGTH('gold.ClearOps_STP_Settings', 'GoldModifiedBy') IS NULL
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD GoldModifiedBy VARCHAR(100) NULL');
    IF COL_LENGTH('gold.ClearOps_STP_Settings', 'GoldModifiedDate') IS NULL
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD GoldModifiedDate DATETIME NULL');

    -- Widen/convert existing columns to the expected types (no-op when already correct).
    IF EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('gold.ClearOps_STP_Settings') AND name = 'Filter_Name'
               AND (system_type_id <> 231 OR max_length <> 400))
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ALTER COLUMN Filter_Name NVARCHAR(200) NOT NULL');
    IF EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('gold.ClearOps_STP_Settings') AND name = 'Project_Ids'
               AND (system_type_id <> 231 OR max_length <> -1))
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ALTER COLUMN Project_Ids NVARCHAR(MAX) NOT NULL');

    -- Constraints
    IF NOT EXISTS (SELECT 1 FROM sys.key_constraints WHERE parent_object_id = OBJECT_ID('gold.ClearOps_STP_Settings') AND type = 'PK')
       AND COL_LENGTH('gold.ClearOps_STP_Settings', 'STP_Settings_Id') IS NOT NULL
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD CONSTRAINT PK_gold_ClearOps_STP_Settings PRIMARY KEY (STP_Settings_Id)');
    IF NOT EXISTS (SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_gold_ClearOps_STP_Settings_User')
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD CONSTRAINT FK_gold_ClearOps_STP_Settings_User FOREIGN KEY (User_ID) REFERENCES [gold].[ClearOps_Users] (User_ID)');
    IF NOT EXISTS (SELECT 1 FROM sys.key_constraints WHERE name = 'UQ_gold_ClearOps_STP_Settings_User_FilterName')
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD CONSTRAINT UQ_gold_ClearOps_STP_Settings_User_FilterName UNIQUE (User_ID, Filter_Name)');
    IF NOT EXISTS (SELECT 1 FROM sys.check_constraints WHERE name = 'CK_gold_ClearOps_STP_Settings_ProjectIds')
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD CONSTRAINT CK_gold_ClearOps_STP_Settings_ProjectIds CHECK (ISJSON(Project_Ids) = 1)');
    IF NOT EXISTS (SELECT 1 FROM sys.check_constraints WHERE name = 'CK_gold_ClearOps_STP_Settings_FilterName')
        EXEC (N'ALTER TABLE [gold].[ClearOps_STP_Settings] ADD CONSTRAINT CK_gold_ClearOps_STP_Settings_FilterName CHECK (LEN(LTRIM(RTRIM(Filter_Name))) > 0)');
END
GO

-- Load a user's saved queries (STP dropdown after login):
-- SELECT STP_Settings_Id, Filter_Name, Project_Ids FROM [gold].[ClearOps_STP_Settings] WHERE User_ID = @UserId ORDER BY Filter_Name;

-- Revert:
-- DROP TABLE IF EXISTS [gold].[ClearOps_STP_Settings];
