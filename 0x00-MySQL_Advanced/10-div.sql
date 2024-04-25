-- Creating an SQL procedure
CREATE FUNCTION SafeDiv (a INT,b INT)
RETURNS FLOAT
DETERMINISTIC
RETURN IF(b = 0, 0, a / b);
