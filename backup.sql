-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: autotempohire_db
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_app_customuser`
--

DROP TABLE IF EXISTS `auth_app_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_app_customuser` (
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
  `unique_id` varchar(12) NOT NULL,
  `role` varchar(20) NOT NULL,
  `password_reset_token` varchar(32) DEFAULT NULL,
  `password_last_changed` datetime(6) DEFAULT NULL,
  `accepted_payment_range` int unsigned DEFAULT NULL,
  `age` int unsigned DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `qualification_years` int unsigned DEFAULT NULL,
  `hourly_rate` decimal(10,2) NOT NULL,
  `per_km_rate` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `unique_id` (`unique_id`),
  UNIQUE KEY `auth_app_customuser_email_0f7acc77_uniq` (`email`),
  CONSTRAINT `auth_app_customuser_accepted_payment_range_e690c47b_check` CHECK ((`accepted_payment_range` >= 0)),
  CONSTRAINT `auth_app_customuser_age_8eb00dbb_check` CHECK ((`age` >= 0)),
  CONSTRAINT `auth_app_customuser_qualification_years_9dd34e36_check` CHECK ((`qualification_years` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_app_customuser`
--

LOCK TABLES `auth_app_customuser` WRITE;
/*!40000 ALTER TABLE `auth_app_customuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_app_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_app_customuser_groups`
--

DROP TABLE IF EXISTS `auth_app_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_app_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_app_customuser_groups_customuser_id_group_id_eef898f9_uniq` (`customuser_id`,`group_id`),
  KEY `auth_app_customuser_groups_group_id_951c60f2_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_app_customuser__customuser_id_cfa7c414_fk_auth_app_` FOREIGN KEY (`customuser_id`) REFERENCES `auth_app_customuser` (`id`),
  CONSTRAINT `auth_app_customuser_groups_group_id_951c60f2_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_app_customuser_groups`
--

LOCK TABLES `auth_app_customuser_groups` WRITE;
/*!40000 ALTER TABLE `auth_app_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_app_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_app_customuser_user_permissions`
--

DROP TABLE IF EXISTS `auth_app_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_app_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_app_customuser_user_customuser_id_permission_fd51d15d_uniq` (`customuser_id`,`permission_id`),
  KEY `auth_app_customuser__permission_id_0ed30c88_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_app_customuser__customuser_id_fdf7c76a_fk_auth_app_` FOREIGN KEY (`customuser_id`) REFERENCES `auth_app_customuser` (`id`),
  CONSTRAINT `auth_app_customuser__permission_id_0ed30c88_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_app_customuser_user_permissions`
--

LOCK TABLES `auth_app_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_app_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_app_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_app_driver`
--

DROP TABLE IF EXISTS `auth_app_driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_app_driver` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `license_number` varchar(20) NOT NULL,
  `years_of_experience` int unsigned NOT NULL,
  `user_id` bigint NOT NULL,
  `rating` double NOT NULL,
  `trips_completed` int unsigned NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `accepted_payment_range` decimal(10,2) DEFAULT NULL,
  `age` int unsigned DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `qualification_years` int unsigned DEFAULT NULL,
  `driving_license` varchar(100) DEFAULT NULL,
  `education_certificate` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `license_number` (`license_number`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `auth_app_driver_user_id_74459b2c_fk_auth_app_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `auth_app_customuser` (`id`),
  CONSTRAINT `auth_app_driver_chk_1` CHECK ((`trips_completed` >= 0)),
  CONSTRAINT `auth_app_driver_chk_2` CHECK ((`age` >= 0)),
  CONSTRAINT `auth_app_driver_chk_3` CHECK ((`qualification_years` >= 0)),
  CONSTRAINT `auth_app_driver_years_of_experience_2a9141ec_check` CHECK ((`years_of_experience` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_app_driver`
--

LOCK TABLES `auth_app_driver` WRITE;
/*!40000 ALTER TABLE `auth_app_driver` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_app_driver` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'CarOwners'),(2,'Drivers');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Token',6,'add_token'),(22,'Can change Token',6,'change_token'),(23,'Can delete Token',6,'delete_token'),(24,'Can view Token',6,'view_token'),(25,'Can add Token',7,'add_tokenproxy'),(26,'Can change Token',7,'change_tokenproxy'),(27,'Can delete Token',7,'delete_tokenproxy'),(28,'Can view Token',7,'view_tokenproxy'),(29,'Can add user',8,'add_customuser'),(30,'Can change user',8,'change_customuser'),(31,'Can delete user',8,'delete_customuser'),(32,'Can view user',8,'view_customuser'),(33,'Can add car owner',9,'add_carowner'),(34,'Can change car owner',9,'change_carowner'),(35,'Can delete car owner',9,'delete_carowner'),(36,'Can view car owner',9,'view_carowner'),(37,'Can add driver',10,'add_driver'),(38,'Can change driver',10,'change_driver'),(39,'Can delete driver',10,'delete_driver'),(40,'Can view driver',10,'view_driver'),(41,'Can add driver matching',11,'add_drivermatching'),(42,'Can change driver matching',11,'change_drivermatching'),(43,'Can delete driver matching',11,'delete_drivermatching'),(44,'Can view driver matching',11,'view_drivermatching'),(45,'Can add review',12,'add_review'),(46,'Can change review',12,'change_review'),(47,'Can delete review',12,'delete_review'),(48,'Can view review',12,'view_review'),(49,'Can add payment',13,'add_payment'),(50,'Can change payment',13,'change_payment'),(51,'Can delete payment',13,'delete_payment'),(52,'Can view payment',13,'view_payment'),(53,'Can add trip',14,'add_trip'),(54,'Can change trip',14,'change_trip'),(55,'Can delete trip',14,'delete_trip'),(56,'Can view trip',14,'view_trip');
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
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_app_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `auth_app_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carownerprofile`
--

DROP TABLE IF EXISTS `carownerprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carownerprofile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` char(36) DEFAULT NULL,
  `car_model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `carownerprofile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carownerprofile`
--

LOCK TABLES `carownerprofile` WRITE;
/*!40000 ALTER TABLE `carownerprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `carownerprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_carownerprofile`
--

DROP TABLE IF EXISTS `dashboard_carownerprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_carownerprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `car_model` varchar(100) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `dashboard_carownerprofile_user_id_2177eba3_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_carownerprofile`
--

LOCK TABLES `dashboard_carownerprofile` WRITE;
/*!40000 ALTER TABLE `dashboard_carownerprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_carownerprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_driverprofile`
--

DROP TABLE IF EXISTS `dashboard_driverprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dashboard_driverprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `age` int NOT NULL,
  `qualification_years` int NOT NULL,
  `location` varchar(100) NOT NULL,
  `payment_range` decimal(10,2) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `dashboard_driverprofile_user_id_5e68be87_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_driverprofile`
--

LOCK TABLES `dashboard_driverprofile` WRITE;
/*!40000 ALTER TABLE `dashboard_driverprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_driverprofile` ENABLE KEYS */;
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
  KEY `django_admin_log_user_id_c564eba6_fk_users_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(9,'auth_app','carowner'),(8,'auth_app','customuser'),(10,'auth_app','driver'),(11,'auth_app','drivermatching'),(13,'auth_app','payment'),(12,'auth_app','review'),(14,'auth_app','trip'),(6,'authtoken','token'),(7,'authtoken','tokenproxy'),(4,'contenttypes','contenttype'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-03-13 19:05:39.918089'),(2,'contenttypes','0002_remove_content_type_name','2025-03-13 19:05:42.813105'),(15,'users','0001_initial','2025-03-13 19:06:18.538146'),(16,'admin','0001_initial','2025-03-13 19:06:23.824753'),(17,'admin','0002_logentry_remove_auto_add','2025-03-13 19:06:23.923101'),(18,'admin','0003_logentry_add_action_flag_choices','2025-03-13 19:06:24.066970'),(19,'dashboard','0001_initial','2025-03-13 19:06:25.616512'),(20,'dashboard','0002_initial','2025-03-13 19:06:32.334734'),(21,'sessions','0001_initial','2025-03-13 19:06:34.868933'),(27,'authtoken','0001_initial','2025-03-15 20:23:20.557940'),(28,'authtoken','0002_auto_20160226_1747','2025-03-15 20:23:20.660291'),(29,'authtoken','0003_tokenproxy','2025-03-15 20:23:20.781295'),(30,'authtoken','0004_alter_tokenproxy_options','2025-03-15 20:23:20.977839'),(38,'payments','0001_initial','2025-03-18 13:55:33.813586'),(39,'payments','0002_payment_phone_number_payment_status','2025-03-18 15:23:59.705344'),(40,'payments','0003_payment_payment_reference_payment_transaction_id','2025-03-18 16:28:30.267701'),(42,'payments','0004_alter_payment_phone_number_alter_payment_status','2025-03-19 07:33:57.256126'),(50,'payments','0005_payment_trip','2025-03-20 12:48:35.099135'),(51,'tracking','0001_initial','2025-03-20 18:12:15.230448'),(52,'tracking','0002_trip_trip_id','2025-03-21 01:58:16.122214');
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
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `driverprofile`
--

DROP TABLE IF EXISTS `driverprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `driverprofile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` char(36) DEFAULT NULL,
  `age` int NOT NULL,
  `qualification_years` int NOT NULL,
  `location` varchar(100) NOT NULL,
  `payment_range` decimal(10,2) NOT NULL,
  `verified` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `driverprofile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driverprofile`
--

LOCK TABLES `driverprofile` WRITE;
/*!40000 ALTER TABLE `driverprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `driverprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_payment`
--

DROP TABLE IF EXISTS `payments_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `payment_reference` varchar(100) DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `trip_id` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_payment_trip_id_1caa90a6_fk_trips_trip_trip_id` (`trip_id`),
  CONSTRAINT `payments_payment_trip_id_1caa90a6_fk_trips_trip_trip_id` FOREIGN KEY (`trip_id`) REFERENCES `trips_trip` (`trip_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_payment`
--

LOCK TABLES `payments_payment` WRITE;
/*!40000 ALTER TABLE `payments_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews_review`
--

DROP TABLE IF EXISTS `reviews_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews_review` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rating` int NOT NULL,
  `review_message` longtext,
  `created_at` datetime(6) NOT NULL,
  `car_owner_id` bigint NOT NULL,
  `driver_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reviews_review_car_owner_id_00d4ab9f_fk_auth_app_customuser_id` (`car_owner_id`),
  KEY `reviews_review_driver_id_bf917faf_fk_auth_app_driver_id` (`driver_id`),
  CONSTRAINT `reviews_review_car_owner_id_00d4ab9f_fk_auth_app_customuser_id` FOREIGN KEY (`car_owner_id`) REFERENCES `auth_app_customuser` (`id`),
  CONSTRAINT `reviews_review_driver_id_bf917faf_fk_auth_app_driver_id` FOREIGN KEY (`driver_id`) REFERENCES `auth_app_driver` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews_review`
--

LOCK TABLES `reviews_review` WRITE;
/*!40000 ALTER TABLE `reviews_review` DISABLE KEYS */;
INSERT INTO `reviews_review` VALUES (5,3,'Professional and friendly','2025-03-19 21:27:57.304655',17,1);
/*!40000 ALTER TABLE `reviews_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tracking_trackingmodel`
--

DROP TABLE IF EXISTS `tracking_trackingmodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tracking_trackingmodel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `last_updated` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `tracking_trackingmod_user_id_8bc232a6_fk_auth_app_` FOREIGN KEY (`user_id`) REFERENCES `auth_app_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tracking_trackingmodel`
--

LOCK TABLES `tracking_trackingmodel` WRITE;
/*!40000 ALTER TABLE `tracking_trackingmodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `tracking_trackingmodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tracking_trip`
--

DROP TABLE IF EXISTS `tracking_trip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tracking_trip` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `destination` varchar(255) NOT NULL,
  `pickup_location` varchar(255) NOT NULL,
  `trip_date` datetime(6) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `driver_id` bigint NOT NULL,
  `owner_id` bigint NOT NULL,
  `trip_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `trip_id` (`trip_id`),
  KEY `tracking_trip_driver_id_1e2a72dd_fk_auth_app_customuser_id` (`driver_id`),
  KEY `tracking_trip_owner_id_f4ef73de_fk_auth_app_customuser_id` (`owner_id`),
  CONSTRAINT `tracking_trip_driver_id_1e2a72dd_fk_auth_app_customuser_id` FOREIGN KEY (`driver_id`) REFERENCES `auth_app_customuser` (`id`),
  CONSTRAINT `tracking_trip_owner_id_f4ef73de_fk_auth_app_customuser_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_app_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tracking_trip`
--

LOCK TABLES `tracking_trip` WRITE;
/*!40000 ALTER TABLE `tracking_trip` DISABLE KEYS */;
/*!40000 ALTER TABLE `tracking_trip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trips_trip`
--

DROP TABLE IF EXISTS `trips_trip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trips_trip` (
  `destination` varchar(255) NOT NULL,
  `pickup_location` varchar(255) NOT NULL,
  `trip_date` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `car_owner_id` bigint NOT NULL,
  `driver_id` bigint DEFAULT NULL,
  `arrival_time` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `departure_time` datetime(6) NOT NULL,
  `trip_id` varchar(12) NOT NULL,
  PRIMARY KEY (`trip_id`),
  KEY `trips_trip_car_owner_id_6c8cf345_fk_auth_app_customuser_id` (`car_owner_id`),
  KEY `trips_trip_driver_id_26500acf_fk_auth_app_customuser_id` (`driver_id`),
  CONSTRAINT `trips_trip_car_owner_id_6c8cf345_fk_auth_app_customuser_id` FOREIGN KEY (`car_owner_id`) REFERENCES `auth_app_customuser` (`id`),
  CONSTRAINT `trips_trip_driver_id_26500acf_fk_auth_app_customuser_id` FOREIGN KEY (`driver_id`) REFERENCES `auth_app_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trips_trip`
--

LOCK TABLES `trips_trip` WRITE;
/*!40000 ALTER TABLE `trips_trip` DISABLE KEYS */;
INSERT INTO `trips_trip` VALUES ('Kilifi','Nairobi','2025-03-21 00:00:00.000000','pending',3.00,17,9,'2025-03-21 16:26:00.000000','2025-03-20 13:26:33.156991','2025-03-21 08:12:00.000000','235559b3ecdb'),('Voi','Nairobi','2025-03-21 00:00:00.000000','pending',3.00,17,9,'2025-03-21 16:49:00.000000','2025-03-20 13:49:43.990058','2025-03-21 10:00:00.000000','7eab00a8b0ee'),('Voi','Nairobi','2025-03-21 00:00:00.000000','pending',3.00,17,9,'2025-03-21 14:00:00.000000','2025-03-20 13:34:59.270351','2025-03-21 08:00:00.000000','8b8afc3012c0'),('Voi','Nairobi','2025-03-21 00:00:00.000000','pending',2.00,17,9,'2025-03-21 14:25:00.000000','2025-03-20 14:26:00.030847','2025-03-21 08:25:00.000000','b32820014af7'),('Kilifi','Nairobi','2025-03-21 00:00:00.000000','pending',3.00,17,9,'2025-03-21 16:00:00.000000','2025-03-20 13:23:18.297976','2025-03-21 09:00:00.000000','f52e06b56be1'),('Mombasa','Nairobi','2025-03-20 12:46:49.699360','pending',500.00,7,NULL,'2025-03-20 12:46:49.699360','2025-03-20 12:46:49.700360','2025-03-20 12:46:49.699360','f6d5bd3eb33c'),('Kilifi','Nairobi','2025-03-22 00:00:00.000000','pending',3.00,17,9,'2025-03-22 17:39:00.000000','2025-03-20 13:40:07.001645','2025-03-22 10:10:00.000000','fbc988645d2e');
/*!40000 ALTER TABLE `trips_trip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` char(36) NOT NULL DEFAULT (uuid()),
  `username` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `role` enum('car_owner','driver') NOT NULL,
  `is_verified` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user`
--

DROP TABLE IF EXISTS `users_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user` (
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
  `user_id` char(32) NOT NULL,
  `role` varchar(20) DEFAULT NULL,
  `is_verified` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_groups`
--

DROP TABLE IF EXISTS `users_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_groups_user_id_group_id_b88eab82_uniq` (`user_id`,`group_id`),
  KEY `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_user_groups_user_id_5f6f5a90_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_groups`
--

LOCK TABLES `users_user_groups` WRITE;
/*!40000 ALTER TABLE `users_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_user_permissions`
--

DROP TABLE IF EXISTS `users_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_user_permissions_user_id_permission_id_43338c45_uniq` (`user_id`,`permission_id`),
  KEY `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_user_permissions_user_id_20aca447_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_user_permissions`
--

LOCK TABLES `users_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-24 16:08:54
