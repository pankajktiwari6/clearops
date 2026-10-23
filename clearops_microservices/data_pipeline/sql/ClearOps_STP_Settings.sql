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
GO

-- Load a user's saved queries (STP dropdown after login):
-- SELECT STP_Settings_Id, Filter_Name, Project_Ids FROM [gold].[ClearOps_STP_Settings] WHERE User_ID = @UserId ORDER BY Filter_Name;

-- Revert:
-- DROP TABLE IF EXISTS [gold].[ClearOps_STP_Settings];
