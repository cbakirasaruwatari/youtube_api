CREATE DATABASE IF NOT EXISTS youtube;
USE youtube;

CREATE TABLE `channels` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `api_version` varchar(100) NOT NULL,
  `api_method` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `original_id` varchar(100) NOT NULL,
  `body` json NOT NULL,
  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

