/*

CREATE TABLE NIRefPeriods (
	PeriodName varchar(30) NOT NULL,
	StartDate date NOT NULL,
	EndDate date NULL
)

*/

INSERT INTO dbo.NIRefPeriods (
	PeriodName,
	StartDate,
	EndDate
)
VALUES
('Orig Log 1', '2020-03-10', '2020-08-26'),
('Orig Log 2', '2021-01-03', '2021-05-31'),
('Chelt Log', '2022-02-05', '2022-07-24'),
('Mid 2022 Start', '2022-07-27', NULL)
