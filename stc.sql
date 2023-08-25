/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : stc

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2023-08-25 12:58:20
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for car_logbook
-- ----------------------------
DROP TABLE IF EXISTS `car_logbook`;
CREATE TABLE `car_logbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `epid` varchar(255) NOT NULL,
  `car_seen_datetime` datetime NOT NULL,
  `reader_ip` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of car_logbook
-- ----------------------------
INSERT INTO `car_logbook` VALUES ('1', 'e2806995000050009125b19cacb500', '2023-08-18 13:45:54', '192.168.2.159');
INSERT INTO `car_logbook` VALUES ('2', 'e2806995000050009125b19cacb500', '2023-08-18 13:46:10', '192.168.2.159');
INSERT INTO `car_logbook` VALUES ('3', 'e2806995000050009125b19cacb500', '2023-08-18 14:19:09', '192.168.2.159');
INSERT INTO `car_logbook` VALUES ('4', 'e2806995000050009125b19cacb500', '2023-08-18 14:19:09', '192.168.2.159');
INSERT INTO `car_logbook` VALUES ('5', 'e2806995000050009125b19cacb500', '2023-08-18 14:19:09', '192.168.2.159');
INSERT INTO `car_logbook` VALUES ('6', 'e2806995000050009125b19cacb500', '2023-08-18 14:19:10', '192.168.2.159');
INSERT INTO `car_logbook` VALUES ('7', 'e2806995000050009125b19cacb500', '2023-08-18 14:19:11', '192.168.2.159');
INSERT INTO `car_logbook` VALUES ('8', 'e2806995000050009125b19cacb500', '2023-08-18 14:19:12', '192.168.2.159');
INSERT INTO `car_logbook` VALUES ('9', 'e2806995000050009125b19cacb500', '2023-08-18 14:19:13', '192.168.2.159');
INSERT INTO `car_logbook` VALUES ('10', 'e2806995000050009125b19cacb500', '2023-08-18 14:22:51', '192.168.2.159');
INSERT INTO `car_logbook` VALUES ('11', 'e2806995000050009125b19cacb500', '2023-08-18 14:22:52', '192.168.2.159');
INSERT INTO `car_logbook` VALUES ('12', 'e2806995000050009125b19cacb500', '2023-08-18 14:22:54', '192.168.2.159');

-- ----------------------------
-- Table structure for registered_rfid
-- ----------------------------
DROP TABLE IF EXISTS `registered_rfid`;
CREATE TABLE `registered_rfid` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `car_id` varchar(255) DEFAULT '',
  `epid` varchar(255) NOT NULL,
  `car_lastseen` datetime DEFAULT NULL,
  `reader_ip` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of registered_rfid
-- ----------------------------
INSERT INTO `registered_rfid` VALUES ('1', '', 'e280699500004000912778ed1a2b00', null, null);
INSERT INTO `registered_rfid` VALUES ('2', '', 'e2806995000050009125b19cacb500', null, null);

-- ----------------------------
-- Table structure for rfid_reader
-- ----------------------------
DROP TABLE IF EXISTS `rfid_reader`;
CREATE TABLE `rfid_reader` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reader_ip` varchar(255) NOT NULL DEFAULT '',
  `reader_lastseen` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of rfid_reader
-- ----------------------------
INSERT INTO `rfid_reader` VALUES ('1', '192.168.2.159', '2023-08-25 11:50:26');
