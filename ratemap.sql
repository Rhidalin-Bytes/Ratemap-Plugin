-- phpMyAdmin SQL Dump
-- version 3.3.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 08, 2010 at 09:22 PM
-- Server version: 5.1.48
-- PHP Version: 5.3.2

--
-- Ratemap plugin required insertions
--
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `b3_v4`
--

-- --------------------------------------------------------

--
-- Table structure for table `ratemap`
--

CREATE TABLE IF NOT EXISTS `ratemap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mapname` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 COMMENT='Map name storage' AUTO_INCREMENT=2 ;

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
  `map` text NOT NULL,
  `rating` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 COMMENT='Map rating storage' AUTO_INCREMENT=2 ;

--
-- Dumping data for table `rating`
--

INSERT INTO `rating` (`id`, `map`, `rating`) VALUES
(1, '1', 1);
