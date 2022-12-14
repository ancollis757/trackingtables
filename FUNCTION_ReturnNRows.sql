CREATE FUNCTION  dbo.GetNums2(@N AS BIGINT) RETURNS TABLE
AS
RETURN
SELECT TOP (@N) ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) AS I
    FROM SYS.OBJECTS S1
	CROSS JOIN SYS.OBJECTS S2
	CROSS JOIN SYS.OBJECTS S3
	CROSS JOIN SYS.OBJECTS S4
	CROSS JOIN SYS.OBJECTS S5
GO