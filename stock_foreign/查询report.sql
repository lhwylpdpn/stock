/*详情*/
SELECT 
b.`open_time`,a.`orderid`,b.`orderid`,a.`open_price`,a.`close_price`,b.`open_price`,b.`close_price` ,a.`profit`,b.`profit`
FROM report_order a , report_order b WHERE 
a.`buyprice_except_open`=b.`buyprice_except_open` AND a.`sellprice_except_open`=b.`sellprice_except_open`
AND a.`id`>b.`id`  ORDER BY a.`open_time`
 /*统计*/
SELECT 

a.`open_time`,
a.`profit`+b.`profit` AS 收益,
TIMESTAMPDIFF(HOUR, a.`open_time`, a.`close_time`)  AS 交易时长（小时）,
TIMESTAMPDIFF(MINUTE, a.`open_time`, a.`close_time`)  AS 交易时长（分钟）,
(a.`open_price`-a.`buyprice_except_open`+a.`sellprice_except_open`-b.`open_price`) AS 交易差额,
(a.`open_price`-a.`buyprice_except_open`+a.`sellprice_except_open`-b.`open_price`)/(a.`open_price`+b.`open_price`) AS 交易差额比,
(a.`open_price`-a.`sellprice_except_open`+a.`buyprice_except_open`-b.`open_price`) AS 29日逆反交易差额,
(a.`open_price`-a.`sellprice_except_open`+a.`buyprice_except_open`-b.`open_price`)/(a.`open_price`+b.`open_price`) AS 29日逆反交易差额比



FROM report_order a , report_order b WHERE 

a.`buyprice_except_open`=b.`buyprice_except_open` AND a.`sellprice_except_open`=b.`sellprice_except_open`
AND a.`id`>b.`id`  
AND a.open_time>'2015-04-29 12:01:31'
ORDER BY a.`open_time`