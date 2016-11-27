CREATE TABLE `runlian365_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `price` float NOT NULL COMMENT '价格',
  `type` varchar(100) NOT NULL COMMENT '型号',
  `pics` varchar(500) NOT NULL COMMENT '图片，多张图片以“|”拼接',
  `detail` varchar(5000) NOT NULL COMMENT '商品详情',
  `source_url` varchar(100) NOT NULL,
  `storage` varchar(50) DEFAULT NULL COMMENT '库存',
  `lack_period` varchar(10) DEFAULT NULL,
  `created` int(10) NOT NULL DEFAULT '0' COMMENT '记录创建时间',
  `updated` int(10) NOT NULL DEFAULT '0' COMMENT '记录更新时间',
  `is_contrast` int(5) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;