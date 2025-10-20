-- Copy 3 BLOCK SQL này và chạy TỪNG BLOCK một trong Railway

-- ========== BLOCK 1: Tạo bảng users ==========
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(120) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `is_verified` TINYINT(1) NOT NULL DEFAULT 0,
  `has_paid` TINYINT(1) NOT NULL DEFAULT 0,
  `is_admin` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `verified_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_email` (`email`),
  KEY `ix_users_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========== BLOCK 2: Tạo bảng payments ==========
CREATE TABLE IF NOT EXISTS `payments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `payos_order_id` VARCHAR(255) NOT NULL,
  `payos_transaction_id` VARCHAR(255) DEFAULT NULL,
  `amount` INT NOT NULL,
  `currency` VARCHAR(3) NOT NULL DEFAULT 'VND',
  `status` VARCHAR(50) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `completed_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_payments_payos_order_id` (`payos_order_id`),
  UNIQUE KEY `uq_payments_payos_tx` (`payos_transaction_id`),
  KEY `ix_payments_user_id` (`user_id`),
  CONSTRAINT `fk_payments_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ========== BLOCK 3: Tạo admin ==========
INSERT INTO `users` (`email`, `password_hash`, `is_verified`, `has_paid`, `is_admin`)
VALUES (
  'admin@gmail.com',
  'pbkdf2:sha256:600000$ASzA2jXKfRXrDGKk$6c7d9b00af237a7520ebf47979ce40bbd9b3a2867e7fbfe62a24ef304073dfe2',
  1, 1, 1
)
ON DUPLICATE KEY UPDATE
  `password_hash` = VALUES(`password_hash`),
  `is_admin` = 1,
  `is_verified` = 1,
  `has_paid` = 1;
