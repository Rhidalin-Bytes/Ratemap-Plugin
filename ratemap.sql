--
-- Ratemap Plugin
--
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- --------------------------------------------------------
--
-- Table structure for table `ratemap`
--
CREATE TABLE IF NOT EXISTS `ratemap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mapname` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 COMMENT='Map name storage' AUTO_INCREMENT=7 ;
--
-- Dumping data for table `ratemap`
--
INSERT INTO `ratemap` (`id`, `mapname`) VALUES
(1, 'testmap');
-- --------------------------------------------------------
--
-- Table structure for table `rating`
--
CREATE TABLE IF NOT EXISTS `rating` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `map` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `map_2` (`map`,`client_id`),
  KEY `client_id` (`client_id`),
  KEY `map` (`map`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 COMMENT='Map rating storage' AUTO_INCREMENT=32 ;
--
-- Dumping data for table `rating`
--
INSERT INTO `rating` (`id`, `map`, `rating`, `client_id`, `time`) VALUES
(1, 1, 1, 1, '2010-08-11 05:01:13');
