-- Revenue by project for one month, optionally limited to selected projects.
--   @ProjectNumbers : comma-separated Project_Numbers (e.g. 'P-100,P-200'); NULL/empty = all projects.
--   @AsOfDate       : any date inside the month wanted; NULL = month of the latest TIME_ENTRY_DATE
--                     in gold.OTL_Timecard (the "current month" of the loaded data).
CREATE OR ALTER PROCEDURE gold.usp_project_revenue_month
    @ProjectNumbers NVARCHAR(MAX) = NULL,
    @AsOfDate       DATE          = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SET @AsOfDate = COALESCE(@AsOfDate, (SELECT MAX(TIME_ENTRY_DATE) FROM gold.OTL_Timecard));
    DECLARE @MonthStart DATE = DATEFROMPARTS(YEAR(@AsOfDate), MONTH(@AsOfDate), 1);
    DECLARE @MonthEnd   DATE = DATEADD(MONTH, 1, @MonthStart);

    -- Selected projects (empty set => no project filter).
    DECLARE @Selected TABLE (Project_Number VARCHAR(450) PRIMARY KEY);
    INSERT INTO @Selected (Project_Number)
    SELECT DISTINCT LTRIM(RTRIM(value))
    FROM STRING_SPLIT(COALESCE(@ProjectNumbers, N''), N',')
    WHERE LTRIM(RTRIM(value)) <> N'';
    DECLARE @FilterProjects BIT = CASE WHEN EXISTS (SELECT 1 FROM @Selected) THEN 1 ELSE 0 END;

    ;WITH Hours AS
    (
        SELECT PROJECT_NUM, EMPLOYEE_NUMBER, SUM(HOURS) AS TotalHours
        FROM gold.OTL_Timecard
        WHERE TIME_ENTRY_DATE >= @MonthStart AND TIME_ENTRY_DATE < @MonthEnd
          AND (@FilterProjects = 0 OR PROJECT_NUM IN (SELECT Project_Number FROM @Selected))
        GROUP BY PROJECT_NUM, EMPLOYEE_NUMBER
    )
    SELECT
        @MonthStart AS MonthStart,
        PM.Project_Number, PM.Project_Name, PM.Rate_Schedule_Name,
        SUM(H.TotalHours)           AS TotalHours,
        SUM(H.TotalHours * RC.Rate) AS Revenue
    FROM Hours H
    INNER JOIN gold.Project_Master PM ON PM.Project_Number = H.PROJECT_NUM
    LEFT JOIN gold.Employee_Master EM
           ON LTRIM(RTRIM(EM.HRID)) = LTRIM(RTRIM(CAST(H.EMPLOYEE_NUMBER AS VARCHAR(50))))
    LEFT JOIN gold.RateCard RC
           ON RC.Rate_Schedule_Name = PM.Rate_Schedule_Name AND RC.Job_Code = EM.Job_Code
    GROUP BY PM.Project_Number, PM.Project_Name, PM.Rate_Schedule_Name
    ORDER BY Revenue DESC;
END;
GO
-- Examples:
--   EXEC gold.usp_project_revenue_month;                                          -- all projects, latest month
--   EXEC gold.usp_project_revenue_month @ProjectNumbers = 'P-100,P-200';          -- selected projects
--   EXEC gold.usp_project_revenue_month 'P-100', '2026-10-15';                    -- selected, specific month
