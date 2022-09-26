/****** Script for SelectTopNRows command from SSMS  ******/

--DECLARE myvar = SELECT StartDate from NIREFPERIODs where PeriodName = 'Orig Log 1'


SELECT *
FROM NeckInj
WHERE NeckInj.LogDate >= (SELECT StartDate FROM NIRefPeriods WHERE PeriodName = 'Orig Log 1')
AND NeckInj.LogDate <= (SELECT EndDate FROM NIRefPeriods WHERE PeriodName = 'Orig Log 1')
