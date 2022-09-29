/****** Script for SelectTopNRows command from SSMS  ******/

SELECT [LogDate]
      ,[RightPain]
      ,[RightNumb]
      ,[LeftPain]
      ,[LeftNumb]
      ,[LeftElbowPain]
      ,[LeftElbowNumb]
      ,[Notes]
      ,[ExternalityAdjustment]
	  ,[PeriodName]
INTO [Tracking].[dbo].[NeckInj_withPeriods]
FROM [Tracking].[dbo].[NeckInj_GapFilled]
LEFT OUTER JOIN [Tracking].[dbo].[NIRefPeriods]
ON LogDate between StartDate and EndDate