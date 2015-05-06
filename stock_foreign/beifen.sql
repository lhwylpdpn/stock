/*
SQLyog Ultimate v11.24 (32 bit)
MySQL - 5.6.21-log : Database - stock_foreign
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`stock_foreign` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `stock_foreign`;

/*Table structure for table `active_trade` */

DROP TABLE IF EXISTS `active_trade`;

CREATE TABLE `active_trade` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orderid_mt4_buy` varchar(40) DEFAULT NULL,
  `orderid_mt4_sell` varchar(40) DEFAULT NULL,
  `open_price_buy` float DEFAULT NULL,
  `open_price_sell` float DEFAULT NULL,
  `open_time_buy` datetime DEFAULT NULL,
  `open_time_sell` datetime DEFAULT NULL,
  `close_price_buy` float DEFAULT NULL,
  `close_price_sell` float DEFAULT NULL,
  `close_time_buy` datetime DEFAULT NULL,
  `close_time_sell` datetime DEFAULT NULL,
  `profit` float DEFAULT NULL,
  `class` varchar(40) DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `norm_data` */

DROP TABLE IF EXISTS `norm_data`;

CREATE TABLE `norm_data` (
  `stockidA` varchar(50) DEFAULT NULL,
  `stockidB` varchar(50) DEFAULT NULL,
  `stockidA_price` float DEFAULT NULL,
  `stockidB_price` float DEFAULT NULL,
  `normvalue_per_100` float DEFAULT NULL,
  `normvalue_per_500` float DEFAULT NULL,
  `normvalue_per_1000` float DEFAULT NULL,
  `normvalue_per_all` float DEFAULT NULL,
  `norm_avg_100` float DEFAULT NULL,
  `norm_avg_500` float DEFAULT NULL,
  `norm_avg_1000` float DEFAULT NULL,
  `norm_avg_all` float DEFAULT NULL,
  `norm_stdev_100` float DEFAULT NULL,
  `norm_stdev_500` float DEFAULT NULL,
  `norm_stdev_1000` float DEFAULT NULL,
  `norm_stdev_all` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `order` */

DROP TABLE IF EXISTS `order`;

CREATE TABLE `order` (
  `orderid` int(11) NOT NULL AUTO_INCREMENT,
  `order_stockA` varchar(45) DEFAULT NULL,
  `order_stockB` varchar(45) DEFAULT NULL,
  `order_time_send` datetime DEFAULT NULL,
  `order_priceA` float DEFAULT NULL,
  `order_priceB` float DEFAULT NULL,
  `order_time_trade` datetime DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `order_count_A` int(11) DEFAULT NULL,
  `order_count_B` int(11) DEFAULT NULL,
  `action` int(11) DEFAULT NULL,
  `except_buy_price` float DEFAULT NULL,
  `except_sell_price` float DEFAULT NULL,
  `action_buy_price` float DEFAULT NULL,
  `action_sell_price` float DEFAULT NULL,
  KEY `orderid` (`orderid`)
) ENGINE=InnoDB AUTO_INCREMENT=365 DEFAULT CHARSET=utf8;

/*Table structure for table `releation` */

DROP TABLE IF EXISTS `releation`;

CREATE TABLE `releation` (
  `stockidA` varchar(45) DEFAULT NULL,
  `stockidB` varchar(45) DEFAULT NULL,
  `relation_price_100` float DEFAULT NULL,
  `relation_price_1000` float DEFAULT NULL,
  `relation_price_all` float DEFAULT NULL,
  `relation_per_100` float DEFAULT NULL,
  `relation_per_1000` float DEFAULT NULL,
  `relation_per_all` float DEFAULT NULL,
  `all_count` varchar(45) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `stock` */

DROP TABLE IF EXISTS `stock`;

CREATE TABLE `stock` (
  `stockid` varchar(100) DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  `time` varchar(45) DEFAULT NULL,
  `open_` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `per` varchar(50) DEFAULT NULL,
  `tag` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `stock_code` */

DROP TABLE IF EXISTS `stock_code`;

CREATE TABLE `stock_code` (
  `code` varchar(45) NOT NULL,
  `class` varchar(45) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `comment` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `stock_test` */

DROP TABLE IF EXISTS `stock_test`;

CREATE TABLE `stock_test` (
  `stockid` varchar(100) DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  `time` varchar(45) DEFAULT NULL,
  `open_` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `per` varchar(50) DEFAULT NULL,
  `tag` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `temp` */

DROP TABLE IF EXISTS `temp`;

CREATE TABLE `temp` (
  `date` datetime DEFAULT NULL,
  `logdata` varchar(45) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
