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
FROM [Tracking].[dbo].[NeckInj_New]