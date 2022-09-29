SELECT *
FROM [Tracking].[dbo].[NeckInj_GapFilled]
WHERE LogDate >= (SELECT StartDate FROM [Tracking].[dbo].NIRefPeriods WHERE PeriodName = 'Orig Log 2')
AND LogDate <= (SELECT EndDate FROM [Tracking].[dbo].NIRefPeriods WHERE PeriodName = 'Orig Log 2');