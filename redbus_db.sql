SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


CREATE TABLE `bus_details` (
  `id` int(11) NOT NULL,
  `trip_id` varchar(100) NOT NULL,
  `bus_owner` varchar(20) DEFAULT NULL,
  `states` varchar(255) DEFAULT NULL,
  `route_name` text NOT NULL,
  `route_link` text NOT NULL,
  `busname` text NOT NULL,
  `bustype` text NOT NULL,
  `departing_time` varchar(255) NOT NULL,
  `departing_loc` varchar(255) DEFAULT NULL,
  `duration` varchar(255) NOT NULL,
  `reaching_time` varchar(255) NOT NULL,
  `reaching_loc` varchar(255) DEFAULT NULL,
  `next_day` varchar(255) DEFAULT NULL,
  `seats_available` varchar(255) DEFAULT NULL,
  `seats_window` varchar(255) DEFAULT NULL,
  `old_price` varchar(255) NOT NULL,
  `price` varchar(255) NOT NULL,
  `star_rating` varchar(255) DEFAULT NULL,
  `amities` text NOT NULL,
  `no_pplaa` varchar(255) DEFAULT NULL,
  `deals_new` text NOT NULL,
  `other_details` text,
  `left_over` text
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


ALTER TABLE `bus_details`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `bus_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=712;COMMIT;
