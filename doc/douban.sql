/*
SQLyog Ultimate v12.09 (64 bit)
MySQL - 5.7.17-log : Database - douban
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`douban` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

/*Table structure for table `follow_person_url` */

DROP TABLE IF EXISTS `follow_person_url`;

CREATE TABLE `follow_person_url` (
  `original_id` varchar(200) NOT NULL COMMENT '源豆瓣人的名字',
  `follow_id` varchar(200) NOT NULL COMMENT '关注人的名字',
  `follow_url` varchar(500) DEFAULT NULL COMMENT '关注人主页的url',
  PRIMARY KEY (`original_id`,`follow_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Table structure for table `movie` */

DROP TABLE IF EXISTS `movie`;

CREATE TABLE `movie` (
  `douban_id` varchar(16) NOT NULL COMMENT '豆瓣的标记id当主键,顺便用来去重',
  `title` varchar(1024) DEFAULT '' COMMENT '标题',
  `directors` text COMMENT '导演',
  `scriptwriters` text COMMENT '编剧',
  `actors` text COMMENT '演员',
  `types` text COMMENT '类别',
  `release_region` text COMMENT '上映地区',
  `release_date` text COMMENT '上映日期',
  `alias` text COMMENT '别名',
  `languages` text COMMENT '语言',
  `duration` text COMMENT '播放时长',
  `score` text COMMENT '评分',
  `description` text COMMENT '描述',
  `tags` text COMMENT '标签',
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `recommendMovie` text COMMENT '推荐电影',
  `vote_num` varchar(100) DEFAULT NULL COMMENT '电影评分人数',
  `rating_per_stars5` varchar(100) DEFAULT NULL COMMENT '电影5分百分比',
  `rating_per_stars4` varchar(100) DEFAULT NULL COMMENT '电影4分百分比',
  `rating_per_stars3` varchar(100) DEFAULT NULL COMMENT '电影3分百分比',
  `rating_per_stars2` varchar(100) DEFAULT NULL COMMENT '电影2分百分比',
  `rating_per_stars1` varchar(100) DEFAULT NULL COMMENT '电影1分百分比',
  `comment_num` varchar(100) DEFAULT NULL COMMENT '电影短评数',
  PRIMARY KEY (`douban_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Table structure for table `movie_comment` */

DROP TABLE IF EXISTS `movie_comment`;

CREATE TABLE `movie_comment` (
  `comment_id` varchar(100) NOT NULL COMMENT '短评的唯一id',
  `douban_id` varchar(100) DEFAULT NULL COMMENT '豆瓣的标记电影id',
  `comment_url` varchar(200) DEFAULT NULL COMMENT '该短评所在页面URL',
  `star` varchar(100) DEFAULT NULL COMMENT '评分',
  `content` text COMMENT '评论内容',
  `people_id` varchar(200) DEFAULT NULL COMMENT '评论者id（唯一）',
  `people` text COMMENT '评论者名字',
  `useful_num` varchar(100) DEFAULT NULL COMMENT '多少人认为评论有用',
  `time` varchar(200) DEFAULT NULL COMMENT '评论时间',
  `people_url` text COMMENT '评论者页面',
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Table structure for table `personal_info` */

DROP TABLE IF EXISTS `personal_info`;

CREATE TABLE `personal_info` (
  `pid` varchar(200) NOT NULL COMMENT '用户id',
  `name` varchar(200) DEFAULT NULL COMMENT '用户名',
  `location` varchar(200) DEFAULT NULL COMMENT '常居住地',
  `introduction` text COMMENT '简介',
  `follow_num` varchar(100) DEFAULT NULL COMMENT '关注人数目',
  `personUrl` varchar(200) DEFAULT NULL COMMENT '用户主页地址',
  `register_time` varchar(200) DEFAULT NULL COMMENT '注册时间',
  `follow_url` varchar(200) DEFAULT NULL COMMENT '所有关注人的url',
  `do` varchar(200) DEFAULT NULL COMMENT '在看的电影',
  `wish` varchar(200) DEFAULT NULL COMMENT '想看的电影',
  `collect` varchar(200) DEFAULT NULL COMMENT '看过的电影',
  `do_num` varchar(50) DEFAULT NULL COMMENT '在看的电影数目',
  `wish_num` varchar(50) DEFAULT NULL COMMENT '想看的电影数目',
  `collect_num` varchar(50) DEFAULT NULL COMMENT '看过的电影数目',
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Table structure for table `wish_movie` */

DROP TABLE IF EXISTS `wish_movie`;

CREATE TABLE `wish_movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `douban_id` varchar(100) DEFAULT NULL COMMENT '豆瓣的电影id',
  `people_id` varchar(200) DEFAULT NULL COMMENT '评论者id（唯一）',
  `time` varchar(200) DEFAULT NULL COMMENT '发表时间',
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1328 DEFAULT CHARSET=utf8mb4;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
