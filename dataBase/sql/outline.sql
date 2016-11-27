CREATE TABLE `runlian365_outline` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) NOT NULL,
  `first_grade` varchar(500) NOT NULL COMMENT '一级目录名',
  `second_grade` varchar(500) NOT NULL COMMENT '二级目录名',
  `third_grade` varchar(500) NOT NULL COMMENT '三级目录名',
  `created` int(10) DEFAULT NULL COMMENT '创建时间',
  `updated` int(10) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `url_UNIQUE` (`url`)
) ENGINE=InnoDB AUTO_INCREMENT=466 DEFAULT CHARSET=utf8mb4;