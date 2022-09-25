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
FROM
	dbo.GetNums2(870) --Returns 870 rows, the length of the total number of days if no gaps.
LEFT OUTER JOIN
	dbo.NeckInj T
ON
	DATEADD(DAY, I, @START_DATE) = T.LogDate
ORDER BY
	LogDate