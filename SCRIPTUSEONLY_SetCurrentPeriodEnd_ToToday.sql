DECLARE @date datetime set @date = GETDATE()
UPDATE NIRefPeriods
SET EndDate = @date
WHERE PeriodName = 'Mid 2022 Start';