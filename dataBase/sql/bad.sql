CREATE TABLE `runlian365_bad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `price` float DEFAULT NULL COMMENT '价格',
  `type` varchar(100) DEFAULT NULL COMMENT '型号',
  `pics` varchar(500) DEFAULT NULL COMMENT '图片，多张图片以“|”拼接',
  `detail` varchar(5000) DEFAULT NULL COMMENT '商品详情',
  `source_url` varchar(100) NOT NULL,
  `storage` varchar(50) DEFAULT NULL COMMENT '库存',
  `lack_period` varchar(10) DEFAULT NULL,
  `created` int(10) DEFAULT '0' COMMENT '记录创建时间',
  `updated` int(10) DEFAULT '0' COMMENT '记录更新时间',
  `is_contrast` int(5) DEFAULT '2',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;