/* View - district_traffic_info
Joins the traffic_info with the district_info
to relay district_id for each district.
The traffic_info can now be related to the district it corresponds to. */

CREATE VIEW district_traffic_info AS 
SELECT dr.district_id AS district_id,
tr.district_hash AS district_hash,
tr.traffic_level_1 AS traffic_level_1,
tr.traffic_level_2 AS traffic_level_2,
tr.traffic_level_3 AS traffic_level_3,
tr.traffic_level_4 AS traffic_level_4,
tr.Time AS Time 
FROM traffic_info tr LEFT JOIN district_info dr 
ON tr.district_hash = dr.district_hash;



/* View - null_orders_by_district_time_slot
Provides information on the number of orders that were not attended
grouped by District and further by by time_slot.
Essentially the GAP r(ij) - a(ij) for the ith destrict and jth timeslot.
*/

CREATE VIEW null_orders_by_district_time_slot AS
SELECT
start_dist_no as District_Id,
FROM_UNIXTIME(FLOOR(UNIX_TIMESTAMP(time)/600)*600) as time_slot, 
count(order_id) as Null_orders,
sum(Price) as Total_Price
FROM null_orders
GROUP BY start_dist_no,DATE_FORMAT(time,"%j"), UNIX_TIMESTAMP(time) DIV 600;

/* View - null_orders
Provides order_info for all unattended orders in all districts.
*/

CREATE VIEW null_orders As
SELECT *
FROM order_info
WHERE driver_id is NULL;

/* View - fulfilled_orders_by_district_time_slot
Provides information on the number of orders that were attended
grouped by District and further by by time_slot.
Essentially the Supply for the ith destrict and jth timeslot.
*/

CREATE VIEW fulfilled_orders_by_district_time_slot AS
SELECT
start_dist_no as District_Id,
FROM_UNIXTIME(FLOOR(UNIX_TIMESTAMP(time)/600)*600) as time_slot, 
count(order_id) as Fulfilled_orders,
sum(Price) as Total_Price
FROM fulfilled_orders
GROUP BY start_dist_no,DATE_FORMAT(time,"%j"), UNIX_TIMESTAMP(time) DIV 600;

/* View - null_orders
Provides order_info for all fuilfilled orders in all districts.
*/

CREATE VIEW fulfilled_orders As
SELECT *
FROM order_info
WHERE driver_id is NOT NULL;

