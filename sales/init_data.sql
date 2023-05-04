INSERT INTO sls_order(customer_id)
VALUES (1);
INSERT INTO sls_order(customer_id)
VALUES (2);

INSERT INTO sls_orderdetail(item_id, unit_price, quantity, order_id)
VALUES (1, 100.0, 1, 1);
INSERT INTO sls_orderdetail(item_id, unit_price, quantity, order_id)
VALUES (2, 50.0, 1, 1);
INSERT INTO sls_orderdetail(item_id, unit_price, quantity, order_id)
VALUES (2, 50.0, 1, 2);
INSERT INTO sls_orderdetail(item_id, unit_price, quantity, order_id)
VALUES (3, 70.0, 1, 2);
