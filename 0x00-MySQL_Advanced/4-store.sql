-- Create Trigger that decreases quantity after order
CREATE TRIGGER update_quantity 
AFTER INSERT ON orders
FOR EACH ROW
	UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
