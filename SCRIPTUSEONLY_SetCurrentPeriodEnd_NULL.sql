DECLARE @date datetime set @date = GETDATE()
UPDATE NIRefPeriods
SET EndDate = Null
WHERE PeriodName = 'Mid 2022 Start';