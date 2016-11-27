CREATE TABLE `runlian365_url` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) NOT NULL,
  `first_grade` varchar(500) NOT NULL COMMENT '一级类目名',
  `second_grade` varchar(500) NOT NULL COMMENT '二级类目名',
  `third_grade` varchar(500) NOT NULL,
  `source_url` varchar(100) NOT NULL COMMENT 'outline表中对应的url',
  `created` int(10) DEFAULT NULL COMMENT '创建时间',
  `updated` int(10) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `url_UNIQUE` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=615 DEFAULT CHARSET=utf8mb4;