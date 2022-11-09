/*
For manual deletion of rows that are duplicates by LogID but differ in other columns
*/

--Check you've got the right data first.
SELECT [LogDate] 
      ,[RightNumb]
      ,[LeftPain]
      ,[RightPain]
      ,[LeftNumb]
      ,[LeftElbowPain]
      ,[LeftElbowNumb]
      ,[Notes]
      ,[ExternalityAdjustment]
      ,[PeriodName]
from [Tracking].[dbo].[NeckInj_wPeriod]
WHERE LogDate = '2022-09-21' --Manually specified date.
AND Notes is Null --Criteria to return only the row(s) to be deleted

--Delete that same data (ensure matches SELECT query above)
DELETE
from [Tracking].[dbo].[NeckInj_wPeriod]
WHERE LogDate = '2022-09-21' --Manually specified date.
AND Notes is Null --Criteria to return only the row(s) to be deleted