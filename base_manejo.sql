-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: crud_qr_db
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_complemento`
--

DROP TABLE IF EXISTS `app_complemento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_complemento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `precio_adicional` decimal(10,2) NOT NULL,
  `item_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_complemento_item_id_688181b0_fk_app_item_id` (`item_id`),
  CONSTRAINT `app_complemento_item_id_688181b0_fk_app_item_id` FOREIGN KEY (`item_id`) REFERENCES `app_item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_complemento`
--

LOCK TABLES `app_complemento` WRITE;
/*!40000 ALTER TABLE `app_complemento` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_complemento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_item`
--

DROP TABLE IF EXISTS `app_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `description` longtext,
  `estado` varchar(20) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `ticket_id` varchar(20) NOT NULL,
  `codigo_qr` varchar(100) DEFAULT NULL,
  `asignado_a_id` bigint DEFAULT NULL,
  `seguimiento_por_id` bigint DEFAULT NULL,
  `soporte_id` bigint DEFAULT NULL,
  `cont_R` varchar(50) DEFAULT NULL,
  `cont_C` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ticket_id` (`ticket_id`),
  KEY `app_item_asignado_a_id_9fe6dfdd_fk_app_user_id` (`asignado_a_id`),
  KEY `app_item_seguimiento_por_id_d4ea02d0_fk_app_user_id` (`seguimiento_por_id`),
  KEY `app_item_soporte_id_0fd3418a_fk_app_user_id` (`soporte_id`),
  CONSTRAINT `app_item_asignado_a_id_9fe6dfdd_fk_app_user_id` FOREIGN KEY (`asignado_a_id`) REFERENCES `app_user` (`id`),
  CONSTRAINT `app_item_seguimiento_por_id_d4ea02d0_fk_app_user_id` FOREIGN KEY (`seguimiento_por_id`) REFERENCES `app_user` (`id`),
  CONSTRAINT `app_item_soporte_id_0fd3418a_fk_app_user_id` FOREIGN KEY (`soporte_id`) REFERENCES `app_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_item`
--

LOCK TABLES `app_item` WRITE;
/*!40000 ALTER TABLE `app_item` DISABLE KEYS */;
INSERT INTO `app_item` VALUES (1,'TSE-022','C 123 R 321','pendiente','2025-03-04 19:02:26.407424','123','qrcodes/qr_None.png',6,3,3,NULL,NULL),(2,'BIOF-032','c 321 r123 operador a ixiamas','pendiente','2025-03-04 19:09:22.140507','','qrcodes/qr_.png',8,3,NULL,NULL,NULL),(3,'BIOM-021','vista previa','completado','2025-03-04 23:37:04.286106','10472','qrcodes/qr_None_iNkC52I.png',NULL,3,3,NULL,NULL),(4,'BIOM-022','c 12','en_progreso','2025-03-05 15:09:52.300675','12345','qrcodes/qr_12345.png',NULL,5,5,NULL,NULL),(5,'TSE-020','Ruralrtr','pendiente','2025-03-08 00:29:47.626230','7273','qrcodes/qr_7273.png',6,9,3,NULL,NULL),(6,'BIOF-050','camara sx150','inicial','2025-03-08 00:35:42.317386','121232','qrcodes/qr_121232_NjytfIk.png',6,5,5,'123','124'),(7,'TSE-021','camara sx110\r\nimpresora LPB6000\r\nOptiplex 360','inicial','2025-03-09 21:01:51.893386','7274','qrcodes/qr_7274_nspFcGq.png',6,NULL,NULL,'52','23'),(8,'7259','as','inicial','2025-04-05 03:30:40.525569','2323','qrcodes/qr_2323.png',NULL,NULL,9,'123','23'),(9,'BIOF-034','k','pendiente','2025-04-05 18:41:00.367467','7260','qrcodes/qr_7260.png',8,5,3,'123','321'),(10,'BIOF-035','estacion 10741','transmitido','2025-04-06 16:00:18.745577','7070','qrcodes/qr_7070_Mi5eNi5.png',8,NULL,3,'23','32'),(11,'TSE-36','OPTIPLEX 360\r\nCANON LBP3000','inicial','2025-04-06 16:38:04.591365','7277','qrcodes/qr_7277_IwD2vaP.png',13,5,5,'434','4345'),(12,'TSE-44','OPTIPLEX 360','inicial','2025-04-06 16:54:42.214355','7272','qrcodes/qr_7272_nq6XjBO.png',NULL,NULL,5,'32','44'),(13,'TSE-35','DW','inicial','2025-04-06 16:55:43.318689','7200','qrcodes/qr_7200_weI0e67.png',10,NULL,3,'32','32'),(14,'TSE-38','o 360\r\ncanon 6000\r\nsx110','transmitido','2025-04-06 19:36:18.912680','7111','qrcodes/qr_7111_bg24FsP.png',14,NULL,3,'5','66');
/*!40000 ALTER TABLE `app_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_user`
--

DROP TABLE IF EXISTS `app_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(10) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `address` longtext,
  `permissions` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_user`
--

LOCK TABLES `app_user` WRITE;
/*!40000 ALTER TABLE `app_user` DISABLE KEYS */;
INSERT INTO `app_user` VALUES (1,'pbkdf2_sha256$870000$7C9GdfLSoeYl31PDhFewhe$vRn3N3iidxo992Tj8sBkrNDVyIX8+7QIMJZUg6S8V7o=','2025-04-06 02:04:05.760009',1,'control_padron','Raul','Choque','rchoquev@gmail.com',1,1,'2025-03-04 05:09:35.000000','admin',NULL,NULL,'',''),(3,'pbkdf2_sha256$870000$Ej7TKMr7NaczqPpiQ1CfdB$vxn9dMchfWWUkQATG4JtSFbXSbcR+jT2vuSAwyzsv7U=','2025-04-06 03:18:20.274459',0,'soporte','soporte','uno','rchoquev01@gmail.com',0,1,'2025-03-04 18:42:30.000000','soporte',NULL,NULL,'',''),(4,'pbkdf2_sha256$870000$rj24VUVneJxMvrwUH2kzT1$n+CgJomFor7sqEdiJ9FrLgtnZGjG0XoKYS9C2vvJRKc=','2025-03-29 23:06:37.264682',1,'raul.choque','raul','choque','rchoquev@gmail.com',1,1,'2025-03-05 03:33:16.000000','admin',NULL,NULL,'',''),(5,'pbkdf2_sha256$870000$Kj6lllGtjuBypr7rIw6dlH$TjNZcldsDLhHCFmGFYZywOhwC4wzcLBPmEZ33/TcDHI=','2025-04-06 14:48:32.879287',0,'victor','victor','apaza','rchoquev@gmail.com',1,1,'2025-03-05 15:04:33.000000','soporte',NULL,NULL,'',''),(6,'pbkdf2_sha256$870000$ZVhvRvOuDAY8aOieJfx5Bq$10xXhlsCpqJj+wvCBPXxIj4bULaWZJzre9Ui9zejEZE=','2025-03-08 00:25:46.000000',0,'usuario','usu','ario','rchoquev@gmail.com',0,0,'2025-03-08 00:14:30.000000','operador',NULL,NULL,'',''),(7,'pbkdf2_sha256$870000$0aHRV6qCJYBsc78Mg9NByb$7f2/7bbbbKZqvhMET+tHGs3oBvJwm67NqBArmA3G/nE=','2025-04-06 01:51:33.899261',0,'logi','logistico','tico','rchoquev@gmail.com',0,1,'2025-03-08 00:21:10.000000','operador',NULL,NULL,'',''),(8,'pbkdf2_sha256$870000$uZyFrBmtTByJx6EW7iAUML$gDAzUrc9vN7DoR4Ba0ZK77AWeLAccRZREodw1Uj/Egk=','2025-04-06 14:47:54.595827',0,'usuario1','usu1','ario','rchoquev@gmail.com',0,1,'2025-03-08 00:23:11.000000','operador',NULL,NULL,'',''),(9,'pbkdf2_sha256$870000$eDZzRX4DlqzO3V3iCsY2vy$yj80WHVlunIWAs/f6GBBht5fP6qRbuU9fBkjiqv4sJM=','2025-03-08 00:32:25.815085',0,'soporte1','soporte','soporte','rchoquev@gmail.com',0,1,'2025-03-08 00:24:27.000000','soporte',NULL,NULL,'',''),(10,'pbkdf2_sha256$870000$Q5Zcz3Vhh3r8SX6Hrf2xDQ$F19qiOHlaatg+AeCkyRyNnKuMrm5Np9TXZ7XFv+3vsE=','2025-03-08 00:31:54.045826',0,'miguel','m','p','rchoquev@gmail.com',0,1,'2025-03-08 00:30:20.000000','operador','2025-03-08',NULL,'',''),(11,'pbkdf2_sha256$870000$mI7CvT49oXqPsL8C5HRVwG$P7boymYgdLmssLYqs89vQNceT7FYpqe3x7PnAHEv2Ng=','2025-03-29 23:08:55.946929',1,'admin','super','usuario','rchoquev@gmail.com',1,1,'2025-03-29 23:07:33.000000','admin',NULL,NULL,'',''),(12,'pbkdf2_sha256$870000$z0ajccmy5ubQjSVaezenMP$mcML1AU6aHMonbpwIEzBW1pol5LEvpYlCYXe0e5Z3AU=','2025-04-06 02:01:52.260328',0,'juan','juan','perez','rchoquev@gmail.com',0,1,'2025-04-05 22:17:58.000000','operador',NULL,NULL,'',''),(13,'pbkdf2_sha256$870000$D1XTm9t11pMQF4NkXPZr7g$YpQArkTrIZhLnP1AD+veIpFykmXd/iHMx77pGUrQ6Zw=','2025-04-06 16:41:34.754524',0,'ALDO','Aldo','Quino Daza','rchoquev@gmail.com',0,1,'2025-04-06 16:38:28.000000','operador',NULL,NULL,'',''),(14,'pbkdf2_sha256$870000$rHK3OJutt5GBlrZBXurG14$Uf7ptBtRCGrtF4Fm+JBph4X3SUIdmkP+1TR/HLqZ7Q4=',NULL,0,'pablo','miguel','pablo molina','rchoquev@gmail.com',0,1,'2025-04-06 16:52:57.000000','operador',NULL,NULL,'','');
/*!40000 ALTER TABLE `app_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_user_groups`
--

DROP TABLE IF EXISTS `app_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_user_groups_user_id_group_id_73b8e940_uniq` (`user_id`,`group_id`),
  KEY `app_user_groups_group_id_e774d92c_fk_auth_group_id` (`group_id`),
  CONSTRAINT `app_user_groups_group_id_e774d92c_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `app_user_groups_user_id_e6f878f6_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_user_groups`
--

LOCK TABLES `app_user_groups` WRITE;
/*!40000 ALTER TABLE `app_user_groups` DISABLE KEYS */;
INSERT INTO `app_user_groups` VALUES (1,7,4),(2,9,3);
/*!40000 ALTER TABLE `app_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_user_user_permissions`
--

DROP TABLE IF EXISTS `app_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_user_user_permissions_user_id_permission_id_7c8316ce_uniq` (`user_id`,`permission_id`),
  KEY `app_user_user_permis_permission_id_4ef8e133_fk_auth_perm` (`permission_id`),
  CONSTRAINT `app_user_user_permis_permission_id_4ef8e133_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `app_user_user_permissions_user_id_24780b52_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_user_user_permissions`
--

LOCK TABLES `app_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `app_user_user_permissions` DISABLE KEYS */;
INSERT INTO `app_user_user_permissions` VALUES (1,4,1),(2,4,2),(3,4,3),(4,4,4),(5,4,5),(6,4,6),(7,4,7),(8,4,8),(9,4,9),(10,4,10),(11,4,11),(12,4,12),(13,4,13),(14,4,14),(15,4,15),(16,4,16),(17,4,17),(18,4,18),(19,4,19),(20,4,20),(21,4,21),(22,4,22),(23,4,23),(24,4,24),(25,4,25),(26,4,26),(27,4,27),(28,4,28),(29,4,29),(30,4,30),(31,4,31),(32,4,32),(33,4,33),(34,4,34),(35,4,35),(36,4,36),(37,4,37),(38,4,38),(39,4,39),(40,4,40);
/*!40000 ALTER TABLE `app_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Activos'),(2,'Coordinador'),(4,'Logistico'),(3,'Soportes');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (1,1,9),(3,1,29),(2,1,34),(4,1,37),(5,2,13),(6,2,14),(7,2,15),(10,3,12),(11,3,29),(12,3,30),(8,3,34),(9,3,36),(13,4,13),(16,4,14),(14,4,37),(15,4,38);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Token',6,'add_token'),(22,'Can change Token',6,'change_token'),(23,'Can delete Token',6,'delete_token'),(24,'Can view Token',6,'view_token'),(25,'Can add Token',7,'add_tokenproxy'),(26,'Can change Token',7,'change_tokenproxy'),(27,'Can delete Token',7,'delete_tokenproxy'),(28,'Can view Token',7,'view_tokenproxy'),(29,'Can add user',8,'add_user'),(30,'Can change user',8,'change_user'),(31,'Can delete user',8,'delete_user'),(32,'Can view user',8,'view_user'),(33,'Can add item',9,'add_item'),(34,'Can change item',9,'change_item'),(35,'Can delete item',9,'delete_item'),(36,'Can view item',9,'view_item'),(37,'Can add complemento',10,'add_complemento'),(38,'Can change complemento',10,'change_complemento'),(39,'Can delete complemento',10,'delete_complemento'),(40,'Can view complemento',10,'view_complemento');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('3b2d6a1fdce481214ef935a6da865d8b8a1198f7','2025-03-05 03:53:49.604479',4);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_app_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-03-04 05:10:23.850951','1','control_padron - admin',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Role\"]}}]',8,1),(2,'2025-03-04 05:13:06.757239','2','user - operador',1,'[{\"added\": {}}]',8,1),(3,'2025-03-04 05:13:41.066180','2','user - operador',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\"]}}]',8,1),(4,'2025-03-04 18:42:32.348838','3','soporte - operador',1,'[{\"added\": {}}]',8,1),(5,'2025-03-04 18:56:37.092574','3','soporte - soporte',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Last login\", \"Role\"]}}]',8,1),(6,'2025-03-04 19:02:26.410069','1','Item object (1)',1,'[{\"added\": {}}]',9,1),(7,'2025-03-04 19:09:22.142625','2','Item object (2)',1,'[{\"added\": {}}]',9,1),(8,'2025-03-04 19:09:35.389312','1','Item object (1)',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',9,1),(9,'2025-03-04 23:37:04.288560','3','Item object (3)',1,'[{\"added\": {}}]',9,1),(10,'2025-03-04 23:38:40.232569','1','Item object (1)',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',9,1),(11,'2025-03-04 23:38:54.253482','3','Item object (3)',2,'[{\"changed\": {\"fields\": [\"Estado\", \"Asignado a\"]}}]',9,1),(12,'2025-03-05 03:33:17.919050','4','Raul - operador',1,'[{\"added\": {}}]',8,1),(13,'2025-03-05 03:34:04.596820','4','Raul - admin',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"User permissions\", \"Last login\", \"Role\"]}}]',8,1),(14,'2025-03-05 03:35:12.965901','4','raul.choque - admin',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',8,1),(15,'2025-03-05 03:53:49.605545','4','3b2d6a1fdce481214ef935a6da865d8b8a1198f7',1,'[{\"added\": {}}]',7,1),(16,'2025-03-05 04:09:27.389808','4','raul.choque - admin',2,'[{\"changed\": {\"fields\": [\"Staff status\"]}}]',8,1),(17,'2025-03-05 04:10:04.207128','4','3b2d6a1fdce481214ef935a6da865d8b8a1198f7',2,'[]',7,1),(18,'2025-03-05 15:04:35.483779','5','victor - operador',1,'[{\"added\": {}}]',8,1),(19,'2025-03-05 15:05:56.136841','5','victor - soporte',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\", \"Last login\", \"Role\"]}}]',8,1),(20,'2025-03-05 15:09:52.306244','4','Item object (4)',1,'[{\"added\": {}}]',9,1),(21,'2025-03-08 00:13:18.368674','2','user - operador',3,'',8,1),(22,'2025-03-08 00:13:21.491669','1','Item object (1)',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',9,1),(23,'2025-03-08 00:14:31.735138','6','usuario - operador',1,'[{\"added\": {}}]',8,1),(24,'2025-03-08 00:15:02.176536','6','usuario - operador',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\"]}}]',8,1),(25,'2025-03-08 00:16:02.871359','1','Activos',1,'[{\"added\": {}}]',3,1),(26,'2025-03-08 00:17:02.825825','2','Coordinador',1,'[{\"added\": {}}]',3,1),(27,'2025-03-08 00:18:43.012697','3','Soportes',1,'[{\"added\": {}}]',3,1),(28,'2025-03-08 00:19:42.545194','4','Logistico',1,'[{\"added\": {}}]',3,1),(29,'2025-03-08 00:20:54.707007','6','usuario - operador',2,'[]',8,1),(30,'2025-03-08 00:21:11.905925','7','logi - operador',1,'[{\"added\": {}}]',8,1),(31,'2025-03-08 00:22:03.129451','7','logi - operador',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Groups\"]}}]',8,1),(32,'2025-03-08 00:23:12.736580','8','usuario1 - operador',1,'[{\"added\": {}}]',8,1),(33,'2025-03-08 00:23:37.140447','8','usuario1 - operador',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\"]}}]',8,1),(34,'2025-03-08 00:24:30.068625','9','soporte1 - operador',1,'[{\"added\": {}}]',8,1),(35,'2025-03-08 00:25:13.746401','9','soporte1 - soporte',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Groups\", \"Role\"]}}]',8,1),(36,'2025-03-08 00:26:44.265546','1','Item object (1)',2,'[{\"changed\": {\"fields\": [\"Asignado a\"]}}]',9,1),(37,'2025-03-08 00:26:56.707020','2','Item object (2)',2,'[{\"changed\": {\"fields\": [\"Asignado a\"]}}]',9,1),(38,'2025-03-08 00:29:47.628350','5','Item object (5)',1,'[{\"added\": {}}]',9,1),(39,'2025-03-08 00:30:23.185108','10','miguel - operador',1,'[{\"added\": {}}]',8,1),(40,'2025-03-08 00:30:58.642097','10','miguel - operador',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Last login\", \"Date of birth\"]}}]',8,1),(41,'2025-03-08 00:31:25.983904','5','Item object (5)',2,'[{\"changed\": {\"fields\": [\"Asignado a\", \"Seguimiento por\"]}}]',9,1),(42,'2025-03-08 00:34:07.956022','6','usuario - operador',2,'[{\"changed\": {\"fields\": [\"Active\"]}}]',8,1),(43,'2025-03-08 00:35:42.319113','6','Item object (6)',1,'[{\"added\": {}}]',9,1),(44,'2025-03-08 00:36:15.082312','6','Item object (6)',2,'[{\"changed\": {\"fields\": [\"Nombre\"]}}]',9,1),(45,'2025-03-09 19:03:26.548232','6','Item object (6)',2,'[{\"changed\": {\"fields\": [\"Nombre\"]}}]',9,1),(46,'2025-03-09 19:03:41.246351','5','Item object (5)',2,'[{\"changed\": {\"fields\": [\"Nombre\"]}}]',9,1),(47,'2025-03-09 19:03:49.925817','5','Item object (5)',2,'[{\"changed\": {\"fields\": [\"Nombre\"]}}]',9,1),(48,'2025-03-09 19:04:03.371621','4','Item object (4)',2,'[{\"changed\": {\"fields\": [\"Nombre\"]}}]',9,1),(49,'2025-03-09 19:05:32.984863','3','Item object (3)',2,'[{\"changed\": {\"fields\": [\"Nombre\"]}}]',9,1),(50,'2025-03-09 19:07:55.128315','1','Item object (1)',2,'[{\"changed\": {\"fields\": [\"Nombre\"]}}]',9,1),(51,'2025-03-09 19:08:17.779234','2','Item object (2)',2,'[{\"changed\": {\"fields\": [\"Nombre\"]}}]',9,1),(52,'2025-03-09 19:40:08.465656','4','raul.choque - admin',2,'[{\"changed\": {\"fields\": [\"Superuser status\"]}}]',8,1),(53,'2025-03-09 21:01:51.897706','7','Item object (7)',1,'[{\"added\": {}}]',9,4),(54,'2025-03-09 21:36:16.519271','7','Item object (7)',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',9,4),(55,'2025-03-09 21:41:23.224875','6','Item object (6)',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',9,4),(56,'2025-03-09 21:50:32.393302','7','Item object (7)',2,'[]',9,4),(57,'2025-03-09 22:04:04.006368','7','Item object (7)',2,'[{\"changed\": {\"fields\": [\"Cont R\", \"Cont C\"]}}]',9,4),(58,'2025-03-09 22:16:45.961828','6','Item object (6)',2,'[]',9,4),(59,'2025-03-09 22:16:54.914699','6','Item object (6)',2,'[{\"changed\": {\"fields\": [\"Codigo qr\"]}}]',9,4),(60,'2025-03-09 23:00:08.546479','7','7274',2,'[{\"changed\": {\"fields\": [\"Cont C\"]}}]',9,4),(61,'2025-03-10 00:02:30.998529','7','7274',2,'[]',9,4),(62,'2025-03-10 00:05:02.401154','7','7274',2,'[]',9,4),(63,'2025-03-10 00:05:43.440080','6','121232',2,'[{\"changed\": {\"fields\": [\"Description\", \"Cont R\", \"Cont C\", \"Estado\"]}}]',9,4),(64,'2025-03-10 00:06:20.721968','6','121232',2,'[]',9,4),(65,'2025-03-29 23:07:35.009421','11','admin - operador',1,'[{\"added\": {}}]',8,4),(66,'2025-03-29 23:08:23.417662','11','admin - admin',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\", \"Superuser status\", \"Role\"]}}]',8,4),(67,'2025-04-05 03:30:40.535112','8','2323',1,'[{\"added\": {}}]',9,11),(68,'2025-04-05 18:41:00.371706','9','7260',1,'[{\"added\": {}}]',9,11),(69,'2025-04-05 22:18:02.284988','12','juan - operador',1,'[{\"added\": {}}]',8,11),(70,'2025-04-05 22:18:27.831177','12','juan - operador',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\"]}}]',8,11),(71,'2025-04-06 02:04:55.351979','4','12345',2,'[{\"changed\": {\"fields\": [\"Seguimiento por\"]}}]',9,1),(72,'2025-04-06 03:07:54.829611','2','',2,'[]',9,1),(73,'2025-04-06 16:00:18.750684','10','7070',1,'[{\"added\": {}}]',9,1),(74,'2025-04-06 16:01:36.615294','10','7070',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',9,1),(75,'2025-04-06 16:01:45.720916','10','7070',2,'[{\"changed\": {\"fields\": [\"Asignado a\"]}}]',9,1),(76,'2025-04-06 16:08:06.883726','10','7070',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',9,1),(77,'2025-04-06 16:12:34.672165','10','7070',2,'[]',9,1),(78,'2025-04-06 16:21:31.253540','10','7070',2,'[{\"changed\": {\"fields\": [\"Asignado a\"]}}]',9,1),(79,'2025-04-06 16:23:18.261261','10','7070',2,'[{\"changed\": {\"fields\": [\"Estado\", \"Asignado a\"]}}]',9,1),(80,'2025-04-06 16:25:33.039421','10','7070',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',9,1),(81,'2025-04-06 16:38:04.595290','11','7277',1,'[{\"added\": {}}]',9,1),(82,'2025-04-06 16:38:31.125583','13','ALDO - operador',1,'[{\"added\": {}}]',8,1),(83,'2025-04-06 16:39:23.559955','13','ALDO - operador',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\"]}}]',8,1),(84,'2025-04-06 16:39:38.180616','11','7277',2,'[{\"changed\": {\"fields\": [\"Asignado a\"]}}]',9,1),(85,'2025-04-06 16:40:45.134901','11','7277',2,'[{\"changed\": {\"fields\": [\"Soporte\"]}}]',9,1),(86,'2025-04-06 16:41:03.668925','11','7277',2,'[{\"changed\": {\"fields\": [\"Seguimiento por\"]}}]',9,1),(87,'2025-04-06 16:52:59.427231','14','pablo - operador',1,'[{\"added\": {}}]',8,1),(88,'2025-04-06 16:53:22.345444','14','pablo - operador',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\"]}}]',8,1),(89,'2025-04-06 16:54:42.216449','12','7272',1,'[{\"added\": {}}]',9,1),(90,'2025-04-06 16:55:43.320819','13','7200',1,'[{\"added\": {}}]',9,1),(91,'2025-04-06 16:56:49.086612','13','7200',2,'[{\"changed\": {\"fields\": [\"Asignado a\"]}}]',9,1),(92,'2025-04-06 17:56:26.464905','13','7200',2,'[]',9,1),(93,'2025-04-06 17:56:36.332864','13','7200',2,'[]',9,1),(94,'2025-04-06 17:59:03.037531','13','7200',2,'[]',9,1),(95,'2025-04-06 18:08:54.716970','13','7200',2,'[]',9,1),(96,'2025-04-06 18:09:21.006137','12','7272',2,'[]',9,1),(97,'2025-04-06 18:21:07.898031','13','7200',2,'[]',9,1),(98,'2025-04-06 18:24:12.266243','13','7200',2,'[]',9,1),(99,'2025-04-06 18:24:52.110566','13','7200',2,'[]',9,1),(100,'2025-04-06 18:25:45.235861','12','7272',2,'[]',9,1),(101,'2025-04-06 18:26:35.287839','11','7277',2,'[]',9,1),(102,'2025-04-06 18:28:06.802669','12','7272',2,'[]',9,1),(103,'2025-04-06 18:28:31.732220','13','7200',2,'[]',9,1),(104,'2025-04-06 18:29:01.071176','7','7274',2,'[]',9,1),(105,'2025-04-06 18:29:38.706791','12','7272',2,'[]',9,1),(106,'2025-04-06 19:07:44.497443','12','7272',2,'[]',9,1),(107,'2025-04-06 19:36:18.915036','14','7111',1,'[{\"added\": {}}]',9,1),(108,'2025-04-06 19:38:03.106630','14','7111',2,'[{\"changed\": {\"fields\": [\"Asignado a\"]}}]',9,1),(109,'2025-04-06 19:40:54.535889','6','121232',2,'[{\"changed\": {\"fields\": [\"Seguimiento por\"]}}]',9,1),(110,'2025-04-06 19:41:49.945047','10','7070',2,'[]',9,1),(111,'2025-04-06 19:43:52.009774','14','7111',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',9,1),(112,'2025-04-06 19:49:14.593896','14','7111',2,'[{\"changed\": {\"fields\": [\"Description\"]}}]',9,1),(113,'2025-04-06 20:00:30.832705','5','7273',2,'[{\"changed\": {\"fields\": [\"Description\", \"Asignado a\"]}}]',9,1),(114,'2025-04-06 20:06:48.588226','14','7111',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',9,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(10,'app','complemento'),(9,'app','item'),(8,'app','user'),(3,'auth','group'),(2,'auth','permission'),(6,'authtoken','token'),(7,'authtoken','tokenproxy'),(4,'contenttypes','contenttype'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-03-04 05:05:02.551738'),(2,'contenttypes','0002_remove_content_type_name','2025-03-04 05:05:02.684094'),(3,'auth','0001_initial','2025-03-04 05:05:03.091036'),(4,'auth','0002_alter_permission_name_max_length','2025-03-04 05:05:03.191203'),(5,'auth','0003_alter_user_email_max_length','2025-03-04 05:05:03.204504'),(6,'auth','0004_alter_user_username_opts','2025-03-04 05:05:03.215100'),(7,'auth','0005_alter_user_last_login_null','2025-03-04 05:05:03.226190'),(8,'auth','0006_require_contenttypes_0002','2025-03-04 05:05:03.231421'),(9,'auth','0007_alter_validators_add_error_messages','2025-03-04 05:05:03.242496'),(10,'auth','0008_alter_user_username_max_length','2025-03-04 05:05:03.253448'),(11,'auth','0009_alter_user_last_name_max_length','2025-03-04 05:05:03.264408'),(12,'auth','0010_alter_group_name_max_length','2025-03-04 05:05:03.304472'),(13,'auth','0011_update_proxy_permissions','2025-03-04 05:05:03.319426'),(14,'auth','0012_alter_user_first_name_max_length','2025-03-04 05:05:03.330979'),(15,'app','0001_initial','2025-03-04 05:05:04.327651'),(16,'admin','0001_initial','2025-03-04 05:05:04.667472'),(17,'admin','0002_logentry_remove_auto_add','2025-03-04 05:05:04.700209'),(18,'admin','0003_logentry_add_action_flag_choices','2025-03-04 05:05:04.718943'),(19,'authtoken','0001_initial','2025-03-04 05:05:04.909899'),(20,'authtoken','0002_auto_20160226_1747','2025-03-04 05:05:04.979153'),(21,'authtoken','0003_tokenproxy','2025-03-04 05:05:04.997108'),(22,'authtoken','0004_alter_tokenproxy_options','2025-03-04 05:05:05.006714'),(23,'sessions','0001_initial','2025-03-04 05:05:05.165925'),(24,'app','0002_item_cont_r_item_cont_c_alter_item_description_and_more','2025-03-09 21:56:09.496598'),(25,'app','0003_remove_item_cont_c_alter_item_cont_r_item_cont_c','2025-03-09 22:29:45.677417');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('7vzvk5xej7xm2b8o30kdflmgomrcrtho','.eJxVjMsOwiAQRf-FtSHQoQzj0r3fQBgeUjU0Ke3K-O_apAvd3nPOfQkftrX6refFT0mchRan341DfOS2g3QP7TbLOLd1mVjuijxol9c55eflcP8Oauj1W0dDMGjHDlDFgCYqFy2hKSYjOwWAyJmsHTSjJmINFMBRyUWnNI4g3h-8CTcA:1u1FMj:Lv2FRhRnz_kNxy2iTUGsL0i3mIUyUhZd_uWRj25rMJM','2025-04-20 02:04:05.764699'),('ddzbbultwatorfplm7da8fgrjwl52pqs','.eJxVjMsOwiAQRf-FtSEwPOvSvd9AmAGkaiAp7cr479qkC93ec859sRC3tYZt5CXMiZ2ZVOz0O2KkR247SffYbp1Tb-syI98VftDBrz3l5-Vw_w5qHPVbowKn0RtyGawGAclNHh3YggInA8n7ZEmoTFmSLhSlEkV5YYxR0oJn7w_x9jdC:1u1T3u:YwokuhfyS4akezi7XGn8VdmYL0WBpYsoWRM8chKg0v8','2025-04-20 16:41:34.760970'),('f92twz3gf3nqa1k9fgr95x7rrtxgl5s1','.eJxVjDsOwjAQBe_iGlmx499S0nOGaNf24gCypTipEHeHSCmgfTPzXmLCbS3T1vMyzUmchRGn340wPnLdQbpjvTUZW12XmeSuyIN2eW0pPy-H-3dQsJdvzdpqBZoT4JDy6IC9VSEoBdkFGIiCJ0I9DqCU49EhW2MyewY0GA2J9wfPeDe1:1trMZ8:Oeq2WJgTZn7BfJE6W2jzqRSvxnabY0xhvKJaVAwne9o','2025-03-23 19:44:02.027962'),('p52ymke3mtri7l3bk7i2jzzqoy2t9mw5','.eJxVjMEOwiAQRP-FsyFQWLAevfcbmmV3laqBpLQn47_bJj3obTLvzbzViOuSx7XJPE6sLsqp02-XkJ5SdsAPLPeqqZZlnpLeFX3QpofK8roe7t9Bxpa3defs2faxR-rYAxp00RGbLZExZH2IgHADQuAohAZYnCMJgRIF9F59vtJGOBA:1trMgf:5VQ57xo53M_yqjr4Ze9RPhnLH_HgS7TEtujUFalylxE','2025-03-23 19:51:49.149985');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'crud_qr_db'
--

--
-- Dumping routines for database 'crud_qr_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-06 18:53:01
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: control_padron
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Administrador','Acceso completo al sistema, incluyendo la gestión de roles y usuarios.'),(2,'Soporte','Permiso para resolver incidencias técnicas.'),(3,'Activos','Acceso para asignacion de y control de activos.'),(4,'Coordinador','Acceso para supervisar y coordinar actividades.'),(5,'Operador','Acceso limitado a operaciones específicas.');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `id_rol` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'control_padron'
--

--
-- Dumping routines for database 'control_padron'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-06 18:53:01
