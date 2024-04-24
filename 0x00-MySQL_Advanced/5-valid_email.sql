-- Create Trigger that decreases quantity after order
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
	SET NEW.valid_email = CASE 
		WHEN NEW.valid_email != OLD.valid_email THEN NEW.valid_email
		WHEN NEW.email != OLD.email THEN 0
		ELSE OLD.valid_email
		END;
