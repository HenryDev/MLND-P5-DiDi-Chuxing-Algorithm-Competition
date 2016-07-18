/* Creates a table "order_info" to represent the order_info data */

CREATE TABLE `order_info` (
  `order_id` varchar(63) DEFAULT NULL,
  `driver_id` varchar(63) DEFAULT NULL,
  `passenger_id` varchar(63) DEFAULT NULL,
  `start_district_hash` varchar(63) DEFAULT NULL,
  `dest_district_hash` varchar(63) DEFAULT NULL,
  `Price` double DEFAULT NULL,
  `Time` datetime DEFAULT NULL,
  `start_dist_no` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
