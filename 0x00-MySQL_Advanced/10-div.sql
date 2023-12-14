-- SafeDiv that divides two numbers and returns the result or 0 if the second number is 0
DELIMITER //
DROP FUNCTION IF EXISTS SafeDiv;
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE result FLOAT DEFAULT 0;

    IF b != 0 THEN
        SET result = a / b;
    END IF;
    RETURN result;
END //

DELIMITER ;
