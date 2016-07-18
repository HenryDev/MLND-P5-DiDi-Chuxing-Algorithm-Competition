/* Run only after the create_order_info script */
/* Creates partitions for each district in the table */
/* Run on empty table for faster partitioning */

ALTER TABLE order_info
PARTITION BY KEY(start_dist_no)
PARTITIONS 66;
