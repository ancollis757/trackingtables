DECLARE @date date
SET @date = (
SELECT StartDate 
from NIRefPeriods 
WHERE PeriodName = 'Mid 2022 Start')

UPDATE NeckInj_withPeriods
SET PeriodName = 'Mid 2022 Start'
WHERE LogDate >= @date;