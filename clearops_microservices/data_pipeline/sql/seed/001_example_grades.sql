-- Example idempotent seed. Replace/add numbered files (002_..., 003_...); they run in filename order.
-- Check the gold.Grades control columns (GoldControlColumnsMixin) before enabling in a real environment.
-- IF NOT EXISTS (SELECT 1 FROM gold.Grades WHERE Grade_Id = 1)
--     INSERT INTO gold.Grades (Grade_Id, Job_Codeasgrade_code, Job_title, Grade) VALUES (1, 'JC001', 'Analyst', 'G1');
SELECT 1 AS seed_noop;
