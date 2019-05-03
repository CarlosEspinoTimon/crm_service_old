USE crm_db;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(45) DEFAULT NULL,
  `admin` tinyint(4) NOT NULL,
  `admin_privileges_by` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `created_by` int(11) NOT NULL COMMENT '		',
  `modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_by` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `fk_users_1_idx` (`admin_privileges_by`),
  CONSTRAINT `fk_users_1` FOREIGN KEY (`admin_privileges_by`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'YOUREMAIL@EMAIL.COM',1,1,'2019-04-26 16:42:11',1,'2019-04-26 16:48:22',1)
UNLOCK TABLES;

CREATE TABLE `customers` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `surname` varchar(45) NOT NULL,
  `photo_url` varchar(150) DEFAULT NULL,
  `created_by` int(11) NOT NULL,
  `last_modify_by` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_customers_1_idx` (`created_by`),
  KEY `fk_customers_2_idx` (`last_modify_by`),
  CONSTRAINT `fk_customers_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_customers_2` FOREIGN KEY (`last_modify_by`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
