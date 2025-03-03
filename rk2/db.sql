-- CREATE DATABASE rk2;

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    degree TEXT NOT NULL,
    cathedral TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS topics (
    teacher_id INT,
    topic TEXT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS students(
    mark_book_id INT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    faculty TEXT NOT NULL,
    study_group TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS marks (
    mark_book_id INT,
    gov_mark INT NOT NULL,
    diploma_mark INT NOT NULL,
    FOREIGN KEY (mark_book_id) REFERENCES students(mark_book_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS teacher_student (
    teacher_id INT,
    student_mark_book_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    FOREIGN KEY (student_mark_book_id) REFERENCES students(mark_book_id) ON DELETE CASCADE
);

INSERT INTO teachers (teacher_id, name, degree, cathedral) VALUES
(0, 'Ivanov Ivan', 'Master degree', 'IU7'),
(1, 'Petrov Petr', 'Master degree', 'IU5'),
(2, 'Ivanov Petr', 'Master degree', 'IU8'),
(3, 'Petrov Ivan', 'Master degree', 'IU7'),
(4, 'Sidorov Alexey', 'Master degree', 'IU6'),
(5, 'Andreev Andrey', 'Master degree', 'IU9'),
(6, 'Aleksandrov Aleksandr', 'Master degree', 'IU7'),
(7, 'Andreev Aleksandr', 'Master degree', 'IU12'),
(8, 'Aleksandrov Andrey', 'Master degree', 'IU6'),
(9, 'Fedorov Fedor', 'Master degree', 'IU5'),
(10, 'Fedorov Ivan', 'Master degree', 'IU7');

-- SELECT * FROM teachers;

INSERT INTO topics (teacher_id, topic) VALUES
(0, 'Programming'),
(0, 'TaSD'),
(1, 'Programming'),
(2, 'IS'),
(3, 'OS'),
(3, 'MDPL'),
(3, 'OOP'),
(5, 'Math'),
(5, 'Programming'),
(6, 'DB'),
(6, 'LiSP'),
(6, 'C'),
(7, 'Programming'),
(9, 'Integrals'),
(10, 'Programming'),
(10, 'Geometry');

--SELECT * FROM topics;

INSERT INTO students (mark_book_id, name, faculty, study_group) VALUES
(0, 'Ivanov Ivan', 'IU', 'IU7-54B'),
(1, 'Petrov Petr', 'IU', 'IU5-54B'),
(2, 'Ivanov Petr', 'MT', 'MT8-54B'),
(3, 'Petrov Ivan', 'FV', 'FV-54B'),
(4, 'Sidorov Alexey', 'FN', 'FN6-54B'),
(5, 'Andreev Andrey', 'IU', 'IU9-54B'),
(6, 'Aleksandrov Aleksandr', 'IU', 'IU7-54B'),
(7, 'Andreev Aleksandr', 'FN', 'FN12-54B'),
(8, 'Aleksandrov Andrey', 'MT', 'MT6-54B'),
(9, 'Fedorov Fedor', 'SM', 'SM5-54B'),
(10, 'Fedorov Ivan', 'IU', 'IU7-54B');

--SELECT * FROM students;

INSERT INTO marks (mark_book_id, gov_mark, diploma_mark) VALUES
(0, 4, 5),
(1, 5, 4),
(2, 3, 5),
(3, 5, 5),
(4, 4, 4),
(5, 3, 3),
(6, 4, 5),
(7, 5, 5),
(8, 4, 4),
(9, 5, 4),
(10, 3, 5);

--SELECT * FROM marks;

INSERT INTO teacher_student (teacher_id, student_mark_book_id) VALUES
(0, 1),
(0, 2),
(1, 3),
(1, 4),
(2, 5),
(3, 6),
(4, 7),
(5, 8),
(7, 9),
(9, 10);

--SELECT * FROM teacher_student;


-- NUMERO 2

-- Инструкция DELETE с вложенным коррелирванным подзапросом в предложении WHERE
-- Удаление всех тем кафедры ИУ6
DELETE FROM topics
WHERE teacher_id in (
    select teacher_id
    from teachers
    where cathedral = 'IU6');

--SELECT *
--FROM topics as top
--JOIN teachers as tea on top.teacher_id = tea.teacher_id;

-- Инструкция SELECT, использующая скалярные подзапросы в выражениях столбцов
-- Средняя оценка на госах отличников по диплому
SELECT mark_book_id, name, (select avg(gov_mark) from marks where diploma_mark = 5)
from students;

-- Инструкция SELECT, использующая вложенные подзапросы с уровнем вложенности 3
-- Темы, которые ведут преподователи, студенты которых - отличники
SELECT topic, teacher_id
FROM topics
WHERE teacher_id in (
    SELECT teacher_id
    FROM teacher_student
    WHERE student_mark_book_id in (
        SELECT mark_book_id
        FROM marks
        WHERE gov_mark = 5 and diploma_mark = 5));


-- NUMERO 3

CREATE PROCEDURE dbo.DestroyDdlTriggers
    @DestroyedTriggersCount INT OUTPUT
AS
BEGIN
    DECLARE @Count INT = 0;
    DECLARE @TriggerName NVARCHAR(128);
    DECLARE TriggerCursor CURSOR FOR
    SELECT name
    FROM sys.triggers
    WHERE is_instead_of_trigger = 1

    OPEN TriggerCursor;

    FETCH NEXT FROM TriggerCursor INTO @TriggerName;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        EXEC('DROP TRIGGER ' + QUOTENAME(@TriggerName));
        SET @Count = @Count + 1;
        FETCH NEXT FROM TriggerCursor INTO @TriggerName;
    END

    CLOSE TriggerCursor;
    DEALLOCATE TriggerCursor;

    SET @DestroyedTriggersCount = @Count;
END;

