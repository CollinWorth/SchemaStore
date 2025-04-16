
-- changeset austin:1
-- add user roles
INSERT INTO roles(user_role) VALUES
   ('admin'),
   ('buyer'),
   ('seller')

-- changeset austin:2
-- add first admin user
INSERT INTO users (username, password, email, first_name, last_name, role_id)
   VALUES ('admin', 'tail', 'admin@idontexist.com', 'Happy', 'Ghast', 1);
