DECLARE @START_DATE DATE

SET @START_DATE = '2020-03-10' --Hard coded start date.

SELECT
	DATEADD(DAY, I, @START_DATE) AS LogDate
	,RightPain
	,RightNumb
	,LeftPain
	,LeftNumb
	,LeftElbowPain
	,LeftElbowNumb
	,Notes
	,ExternalityAdjustment

INTO dbo.NeckInj_GapFilled --Create a new table from the select. Comment out if just want to see result.

FROM
	dbo.GetNums2(923) --Returns 923 rows, the length of the total number of days if no gaps.
LEFT OUTER JOIN
	dbo.NeckInj T
ON
	DATEADD(DAY, I, @START_DATE) = T.LogDate
ORDER BY
	LogDate