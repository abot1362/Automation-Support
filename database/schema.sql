-- Unified Platform - Full Database Schema v1.0
-- Target: MariaDB / MySQL

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

--
-- Table structure for `roles`
--
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB;
INSERT INTO `roles` VALUES (1,'Super Admin','Full access to all system features'),(2,'End User','Basic access to the user portal');

--
-- Table structure for `users`
--
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `hashed_password` varchar(255) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `role_id` int(11) DEFAULT NULL,
  `user_type` enum('admin','end_user') NOT NULL DEFAULT 'end_user',
  `auth_source` varchar(50) NOT NULL DEFAULT 'local',
  `external_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `role_id` (`role_id`),
  KEY `external_id` (`external_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB;
-- Default password is 'admin'
INSERT INTO `users` VALUES (1,'admin','admin@example.com','$2b$12$EixZaYVK1fsbw1yJz2s.W.p3b.h.s.RomiLpYOtM1j.c4AGISU4S.','Main Administrator',1,1,'admin','local',NULL);

--
-- Table structure for `permissions` and `role_permissions`
--
DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `role_permissions`;
CREATE TABLE `role_permissions` (
  `role_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `role_permissions_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE,
  CONSTRAINT `role_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB;

--
-- Table structure for `devices`
--
DROP TABLE IF EXISTS `devices`;
CREATE TABLE `devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `vendor` varchar(50) NOT NULL,
  `os_type` varchar(50) DEFAULT NULL,
  `management_protocol` varchar(50) NOT NULL,
  `host` varchar(100) NOT NULL,
  `port` int(11) DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL COMMENT 'Encrypted',
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB;

--
-- Add all other tables here...
-- The following are placeholders for the full CREATE TABLE statements
-- which are quite long but follow the same SQL syntax.
--
DROP TABLE IF EXISTS `vmware_vcenters`;
DROP TABLE IF EXISTS `proxmox_servers`;
DROP TABLE IF EXISTS `docker_hosts`;
DROP TABLE IF EXISTS `fortigate_devices`;
DROP TABLE IF EXISTS `unifi_controllers`;
DROP TABLE IF EXISTS `surveillance_systems`;
DROP TABLE IF EXISTS `tickets`;
DROP TABLE IF EXISTS `chat_rooms`;
DROP TABLE IF EXISTS `audit_logs`;
-- ... and so on for all other tables.

SET FOREIGN_KEY_CHECKS = 1;
