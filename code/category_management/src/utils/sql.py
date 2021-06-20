"""
Bu dosyada SQL sorguları bulunmakta
"""

category_viewed = """
SELECT
	categoryid,
	productid
FROM
	(
	SELECT
		ROW_NUMBER() OVER (PARTITION BY distinc_user.categoryid
	ORDER BY
		count(distinc_user.userid)) AS rownum,
		distinc_user.categoryid,
		distinc_user.productid,
		count(distinc_user.userid)
	FROM
		(
		SELECT
			op.categoryid,
			table_alias.userid,
			table_alias.productid
		FROM
			product_view table_alias,
			order_product op
		WHERE
			table_alias.productid = op.productid
		GROUP BY
			op.categoryid,
			table_alias.userid,
			table_alias.productid
		ORDER BY
			op.categoryid,
			table_alias.userid,
			table_alias.productid ) AS distinc_user
	GROUP BY
		distinc_user.categoryid,
		distinc_user.productid
	ORDER BY
		distinc_user.categoryid,
		count(distinc_user.userid) DESC ) tmp
WHERE
	rownum <= 10
ORDER BY
	categoryid,
	rownum;
"""

category_bought = """
SELECT
	categoryid,
	productid
FROM
	(
	SELECT
		ROW_NUMBER() OVER (PARTITION BY distinc_user.categoryid
	ORDER BY
		count(distinc_user.userid)) AS rownum,
		distinc_user.categoryid,
		distinc_user.productid,
		count(distinc_user.userid)
	FROM
		(
		SELECT
			op.categoryid,
			table_alias.userid,
			table_alias.productid
		FROM
			orders table_alias,
			order_product op
		WHERE
			table_alias.productid = op.productid
		GROUP BY
			op.categoryid,
			table_alias.userid,
			table_alias.productid
		ORDER BY
			op.categoryid,
			table_alias.userid,
			table_alias.productid ) AS distinc_user
	GROUP BY
		distinc_user.categoryid,
		distinc_user.productid
	ORDER BY
		distinc_user.categoryid,
		count(distinc_user.userid) DESC ) tmp
WHERE
	rownum <= 10
ORDER BY
	categoryid,
	rownum;
"""

conversion_rates = '''
SELECT
	o.categoryid,
	(o.order_count / v.view_count) AS "0"
FROM
	(
	SELECT
		op.categoryid,
		count(*) AS order_count
	FROM
		product_view pv,
		order_product op
	WHERE
		pv.productid = op.productid
	GROUP BY
		op.categoryid
	ORDER BY
		op.categoryid ) AS o,
	(
	SELECT
		op.categoryid,
		count(*) AS view_count
	FROM
		orders o,
		order_product op
	WHERE
		o.productid = op.productid
	GROUP BY
		op.categoryid
	ORDER BY
		op.categoryid ) AS v
WHERE
	o.categoryid = v.categoryid;
'''