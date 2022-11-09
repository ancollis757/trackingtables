/* This only removes strict duplicates. Not differing entries.
Remove differing entries manually first if present; this script does not select the "correct" data;
it deletes rows duplicated by LogDate. Which duplicate (by LogDate) is deleted is arbitrary..*/

--Check what you're deleting.
SELECT *
from (
	select *, rn=row_number() over (partition by LogDate order by LogDate)
	from [Tracking].[dbo].[NeckInj_wPeriod]
) [LogDate]
where rn > 1

--Delete it.
DELETE [LogDate] --This will delete all columns from affected rows, not just LogDate.
from (
	select *, rn=row_number() over (partition by LogDate order by LogDate)
	from [Tracking].[dbo].[NeckInj_wPeriod]
) [LogDate] --Must match deletion column.
where rn > 1
