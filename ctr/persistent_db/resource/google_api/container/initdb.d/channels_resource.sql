CREATE TABLE `channels_resource` (
  `url` varchar(100) NOT NULL,
  `create_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `channels_resource_UN` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci