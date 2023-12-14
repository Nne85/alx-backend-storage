-- This script that creates a trigger that resets the attribute valid_email only when the email has been changed.
DROP TRIGGER IF EXISTS validate_email_update;
DELIMITER //
CREATE TRIGGER validate_email_update BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
   IF OLD.email = NEW.email THEN
	SET NEW.valid_email = OLD.valid_email;
   ELSE
	SET NEW.valid_email = 0;
   END IF;
END //
DELIMITER ;
