-- Medallion layers inside the application MS SQL database.
-- Bronze: raw & staging API responses | Silver: cleaned/validated | Gold: curated business-ready
IF SCHEMA_ID('bronze') IS NULL EXEC('CREATE SCHEMA bronze');
IF SCHEMA_ID('silver') IS NULL EXEC('CREATE SCHEMA silver');
IF SCHEMA_ID('gold')   IS NULL EXEC('CREATE SCHEMA gold');
GO
IF OBJECT_ID('bronze.raw_ingest') IS NULL
CREATE TABLE bronze.raw_ingest (
    id BIGINT IDENTITY PRIMARY KEY,
    source VARCHAR(50) NOT NULL,          -- oracle_fusion | salesforce | workday
    entity VARCHAR(100) NOT NULL,
    payload NVARCHAR(MAX) NOT NULL,       -- raw API response (JSON)
    landing_path VARCHAR(500) NULL,       -- ADLS Gen2 landing-zone blob
    ingested_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO
-- Implement per entity: cleanse + validate bronze -> silver, aggregate silver -> gold.
CREATE OR ALTER PROCEDURE silver.usp_load_from_bronze AS BEGIN SET NOCOUNT ON; /* TODO */ END;
GO
CREATE OR ALTER PROCEDURE gold.usp_load_from_silver AS BEGIN SET NOCOUNT ON; /* TODO */ END;
GO
