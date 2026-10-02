-- ============================================================
-- OpenHealth Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS openhealth;

USE openhealth;


-- ============================================================
-- 1. USERS
-- ============================================================

CREATE TABLE `users` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `auth_provider` enum('local','google') NOT NULL DEFAULT 'local',
  `role` enum('patient','doctor') NOT NULL DEFAULT 'patient',
  `provider_id` varchar(255) DEFAULT NULL,
  `profile_image` varchar(500) DEFAULT NULL,
  `email_verified` tinyint(1) NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `terms_accepted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_login_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_email` (`email`),
  UNIQUE KEY `uq_users_provider` (`auth_provider`,`provider_id`)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


-- ============================================================
-- 2. DOCTORS
-- ============================================================

CREATE TABLE `doctors` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `registration_number` varchar(100) NOT NULL,
  `qualification` varchar(255) NOT NULL,
  `specialization` varchar(100) NOT NULL,
  `experience_years` int NOT NULL DEFAULT '0',
  `bio` text,
  `clinic_name` varchar(255) DEFAULT NULL,
  `clinic_address` varchar(500) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `consultation_fee` decimal(10,2) DEFAULT NULL,
  `consultation_types` varchar(100) DEFAULT NULL,
  `verification_status` enum('Pending','Approved','Rejected') NOT NULL DEFAULT 'Pending',
  `verified_at` datetime DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_id` (`user_id`),
  UNIQUE KEY `unique_registration_number` (`registration_number`),
  CONSTRAINT `fk_doctors_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


-- ============================================================
-- 3. APPOINTMENTS
-- ============================================================

CREATE TABLE `appointments` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `appointment_id` varchar(30) NOT NULL,
  `user_id` bigint unsigned NOT NULL,
  `doctor_id` varchar(20) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` varchar(20) NOT NULL,
  `consultation_type` varchar(30) NOT NULL,
  `reason` text,
  `status` varchar(20) NOT NULL DEFAULT 'Confirmed',
  `booking_created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `appointment_notes` text,
  `cancellation_reason` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `appointment_id` (`appointment_id`),
  KEY `fk_appointments_user` (`user_id`),
  CONSTRAINT `fk_appointments_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


-- ============================================================
-- 4. DOCTOR AVAILABILITY
-- ============================================================

CREATE TABLE `doctor_availability` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `doctor_id` varchar(20) NOT NULL,
  `day_of_week` enum(
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
  ) NOT NULL,
  `start_time` varchar(20) NOT NULL,
  `end_time` varchar(20) NOT NULL,
  `consultation_type` varchar(30) NOT NULL DEFAULT 'Both',
  `is_available` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_doctor_schedule`
    (`doctor_id`,`day_of_week`,`start_time`,`end_time`,`consultation_type`)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


-- ============================================================
-- 5. EMAIL VERIFICATION CODES
-- ============================================================

CREATE TABLE `email_verification_codes` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `otp_hash` varchar(255) NOT NULL,
  `expires_at` datetime NOT NULL,
  `attempts` int NOT NULL DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_verification_user` (`user_id`),
  CONSTRAINT `fk_verification_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;


-- ============================================================
-- 6. HEALTH PREDICTION RECORDS
-- ============================================================

CREATE TABLE `health_prediction_records` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `record_id` varchar(30) NOT NULL,
  `user_id` bigint unsigned NOT NULL,
  `disease_name` varchar(100) NOT NULL,
  `prediction_result` varchar(100) NOT NULL,
  `confidence` decimal(5,2) DEFAULT NULL,
  `prediction_type` varchar(50) NOT NULL,
  `input_data` json DEFAULT NULL,
  `result_details` json DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `record_id` (`record_id`),
  KEY `fk_health_prediction_user` (`user_id`),
  CONSTRAINT `fk_health_prediction_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;