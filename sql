CREATE TABLE tb_user( 
    id_user int NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    line_id_user varchar(50), 
    token varchar(32), 
    full_name varchar(100) 
);

CREATE TABLE tb_sensor(
    id_sensor int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    fk_id_user int,
    sensor_name varchar(100),
    FOREIGN KEY(fk_id_user) REFERENCES tb_user(id_user)  
);

CREATE TABLE tb_event_sensor(
    id_event_sensor int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    fk_id_sensor int,
    event_type text,
    sensor_event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_id_sensor) REFERENCES tb_sensor(id_sensor)
);

CREATE TABLE tb_event_line(
	id_event_line int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    fk_id_user int,
    event_type varchar(50),
    body text,
    line_event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_id_user) REFERENCES tb_user(id_user)
);