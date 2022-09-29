/****** Script for SelectTopNRows command from SSMS  ******/
DECLARE @date date
SET @date = (
SELECT StartDate 
from NIRefPeriods 
WHERE PeriodName = 'Mid 2022 Start')

UPDATE NeckInj_withPeriods set
	NeckInj_withPeriods.[RightPain] = old.[LeftPain],
	NeckInj_withPeriods.[RightNumb] = old.[LeftNumb],
	NeckInj_withPeriods.[LeftPain] = old.[RightPain],
	NeckInj_withPeriods.[LeftNumb] = old.[RightNumb]
	FROM [Tracking].[dbo].[NeckInj_GapFilled] as old
	WHERE NeckInj_withPeriods.LogDate >= @date