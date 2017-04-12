#encoding=utf-8
"""
Created on 2016/8/17 13:36
author: iKexinLL
"""

import re
p1 = re.compile('d\w*_+\w*\$*\w*')
p1 = re.compile(r'from[ +].* ')

a = '''
	select
				a.area_id,
				a.city_id,
				a.user_id,
				sum(total_flux) as total_flux, -- 流量
				sum(b.FEE) as fee,     -- 账单收入
				sum(b.FEE_118) as fee_118, -- 手机上网收入
				sum(FEE_TH) as FEE_TH,    -- 通话(税前)收入
				sum(fee) - sum(coalesce(c.DISCOUNT_FEE,0)) as SQ_ZKZR,  -- 税前折扣折让
				sum(SH_FEE) - sum(coalesce(c.DISCOUNT_FEE,0)) as SH_ZKZR -- 税后折扣折让
			from
				(
					SELECT
							a.user_id,
							a.area_id,
							a.city_id,
							a.total_flux
					FROM (
									SELECT
										q.product_no,
										q.flux,
										q.total_flux,
										coalesce(g.user_id, ''0'') as user_id,
										g.area_id,
										g.city_id
									FROM (
												SELECT
													x.msisdn AS product_no,
													0 AS city_id,
													sum(x.data_flowup + x.data_flowdn) AS gprs_flow,
													sum(x.call_duration) AS call_duration_m,
													sum(x.data_flowdn) AS flow_down,
													sum(x.data_flowup) AS flow_up,
													sum(CASE
															WHEN x.mns_type IN (''6'', ''7'') AND
																		y.service_code IS NULL
																THEN
																	(x.data_flowup + x.data_flowdn)
															ELSE
																0
															END) / 1024 / 1024 AS flux,
													sum(x.data_flowup + x.data_flowdn) / 1024 / 1024 total_flux
												FROM (SELECT
																a.device_number msisdn,
																a.system_type,
																a.old_mns_type mns_type,
																a.service_itme,
																a.old_roam_type roam_type,
																a.gprs_type apnni,
																a.discount_type,
																sum(a.up_flux) data_flowup,
																sum(a.down_flux) data_flowdn,
																sum(a.gprs_duration) call_duration
															FROM dwv.dwv_d_sy_s_second_gprs_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' a
															WHERE a.service_itme NOT IN
																		(''1010000001'',
																			''1010000002'',
																			''1020000001'',
																			''1020000002'',
																			''1020000003'',
																			''1030000004'',
																			''1030000013'',
																			''1030000014'',
																			''1030000016'',
																			''1030000019'',
																			''1030000020'',
																			''1040000007'',
																			''1040000011'',
																			''1040000016'',
																			''1050000002'',
																			''1300149901'',
																			''1710000018'',
																			''1710000023'',
																			''1710000035'',
																			''1990000005'',
																			''2000000000'',
																			''2000000009'',
																			''2032500001'',
																			''2035710001'',
																			''2042000001'',
																			''4000000002'',
																			''4000000005'',
																			''4000000006'')
															GROUP BY
																a.device_number,
																a.system_type,
																a.old_mns_type,
																a.service_itme,
																a.old_roam_type,
																a.gprs_type,
																a.discount_type
															UNION ALL
															SELECT
																b.device_number msisdn,
																b.system_type,
																b.old_mns_type mns_type,
																b.service_itme,
																b.old_roam_type roam_type,
																b.gprs_type apnni,
																b.discount_type,
																sum(b.up_flux) data_flowup,
																sum(b.down_flux) data_flowdn,
																sum(b.gprs_duration) call_duration
															FROM dwv.dwv_d_sy_s_second_gprs_wl_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' b
															GROUP BY
																b.device_number,
																b.system_type,
																b.old_mns_type,
																b.service_itme,
																b.old_roam_type,
																b.gprs_type,
																b.discount_type) x --dw_mis_gprs_flow_db_1
												LEFT JOIN dim.dim_yx_gprs_content y
													ON x.service_itme = y.service_code
												GROUP BY
													x.msisdn) q --jlcrm.dw_mis_gprs_flow_db_$yyyy$mm
									INNER JOIN (
															SELECT
																user_id,
																device_number,
																area_id,
																city_id,
																user_type,
																row_number()
																OVER (PARTITION BY device_number
																	ORDER BY innet_date DESC) rn
															FROM dwv.dwv_d_kh_b_user_info_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||') g --jlcrm.t_dw_product_ms
										ON q.product_no = g.device_number
									WHERE q.flux > 0
												AND g.user_type <> ''02'') a --zdmm803lte
					INNER JOIN (
												SELECT
													a.product_no,
													a.area_id,
													a.city_id --count(a.product_no)
												FROM (
															SELECT
																a.product_no,
																b.area_id,
																b.city_id --count(a.product_no)
															FROM (
																			SELECT
																				x.msisdn AS product_no,
																				0 AS city_id,
																				sum(x.data_flowup + x.data_flowdn) AS gprs_flow,
																				sum(x.call_duration) AS call_duration_m,
																				sum(x.data_flowdn) AS flow_down,
																				sum(x.data_flowup) AS flow_up,
																				sum(CASE
																						WHEN 1 = 1 AND
																								y.service_code IS NULL
																							THEN
																								x.data_flowup + x.data_flowdn
																						ELSE
																							0
																						END) AS hj_flow
																			FROM (SELECT
																							a.device_number msisdn,
																							a.system_type,
																							a.old_mns_type mns_type,
																							a.service_itme,
																							a.old_roam_type roam_type,
																							a.gprs_type apnni,
																							a.discount_type,
																							sum(a.up_flux) data_flowup,
																							sum(a.down_flux) data_flowdn,
																							sum(a.gprs_duration) call_duration
																						FROM dwv.dwv_d_sy_s_second_gprs_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' a
																						WHERE a.service_itme NOT IN
																									(''1010000001'',
																										''1010000002'',
																										''1020000001'',
																										''1020000002'',
																										''1020000003'',
																										''1030000004'',
																										''1030000013'',
																										''1030000014'',
																										''1030000016'',
																										''1030000019'',
																										''1030000020'',
																										''1040000007'',
																										''1040000011'',
																										''1040000016'',
																										''1050000002'',
																										''1300149901'',
																										''1710000018'',
																										''1710000023'',
																										''1710000035'',
																										''1990000005'',
																										''2000000000'',
																									''2000000009'',
																									''2032500001'',
																									''2035710001'',
																									''2042000001'',
																									''4000000002'',
																									''4000000005'',
																									''4000000006'')
																						GROUP BY
																							a.device_number,
																							a.system_type,
																							a.old_mns_type,
																							a.service_itme,
																							a.old_roam_type,
																							a.gprs_type,
																							a.discount_type
																						UNION ALL
																						SELECT
																							b.device_number msisdn,
																							b.system_type,
																							b.old_mns_type mns_type,
																							b.service_itme,
																							b.old_roam_type roam_type,
																							b.gprs_type apnni,
																							b.discount_type,
																							sum(b.up_flux) data_flowup,
																							sum(b.down_flux) data_flowdn,
																							sum(b.gprs_duration) call_duration
																						FROM dwv.dwv_d_sy_s_second_gprs_wl_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' b
																						GROUP BY
																							b.device_number,
																							b.system_type,
																							b.old_mns_type,
																							b.service_itme,
																							b.old_roam_type,
																							b.gprs_type,
																							b.discount_type) x --dw_mis_gprs_flow_db_1
																			LEFT JOIN dim.dim_yx_gprs_content y
																				ON x.service_itme = y.service_code
																			GROUP BY
																				x.msisdn) a, --jlcrm.dw_mis_gprs_flow_db_$op_time
															(
																SELECT
																	user_id,
																	device_number,
																	area_id,
																	city_id,
																	row_number()
																	OVER (PARTITION BY device_number
																		ORDER BY innet_date DESC) rn
																FROM dwv.dwv_d_kh_b_user_info_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||') b
															WHERE a.hj_flow > 0
																		AND b.rn = 1
																		AND a.product_no = b.device_number) a
												LEFT JOIN (
																		SELECT
																			a.device_number product_no --count(a.device_number)
																		FROM dwv.dwv_d_kh_s_user_wlw_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' a --jlcrm.stat_ent_wulianwang_$op_time
																		INNER JOIN (
																								SELECT
																									x.msisdn AS product_no,
																									0 AS city_id,
																									sum(x.data_flowup +
																											x.data_flowdn) AS gprs_flow,
																									sum(x.call_duration) AS call_duration_m,
																									sum(x.data_flowdn) AS flow_down,
																									sum(x.data_flowup) AS flow_up,
																									sum(CASE
																											WHEN 1 = 1 AND
																														y.service_code IS NULL
																												THEN
																													x.data_flowup +
																													x.data_flowdn
																											ELSE
																												0
																											END) AS hj_flow
																								FROM (SELECT
																												a.device_number msisdn,
																												a.system_type,
																												a.old_mns_type mns_type,
																												a.service_itme,
																												a.old_roam_type roam_type,
																												a.gprs_type apnni,
																												a.discount_type,
																												sum(a.up_flux) data_flowup,
																												sum(a.down_flux) data_flowdn,
																												sum(a.gprs_duration) call_duration
																											FROM dwv.dwv_d_sy_s_second_gprs_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' a
																											WHERE a.service_itme NOT IN
																														(''1010000001'',
																															''1010000002'',
																															''1020000001'',
																															''1020000002'',
																															''1020000003'',
																															''1030000004'',
																															''1030000013'',
																															''1030000014'',
																															''1030000016'',
																															''1030000019'',
																															''1030000020'',
																															''1040000007'',
																															''1040000011'',
																															''1040000016'',
																															''1050000002'',
																															''1300149901'',
																															''1710000018'',
																															''1710000023'',
																															''1710000035'',
																															''1990000005'',
																															''2000000000'',
																															''2000000009'',
																															''2032500001'',
																															''2035710001'',
																															''2042000001'',
																															''4000000002'',
																															''4000000005'',
																															''4000000006'')
																											GROUP BY
																												a.device_number,
																												a.system_type,
																												a.old_mns_type,
																												a.service_itme,
																												a.old_roam_type,
																												a.gprs_type,
																												a.discount_type
																											UNION ALL
																											SELECT
																												b.device_number msisdn,
																												b.system_type,
																												b.old_mns_type mns_type,
																												b.service_itme,
																												b.old_roam_type roam_type,
																												b.gprs_type apnni,
																												b.discount_type,
																												sum(b.up_flux) data_flowup,
																												sum(b.down_flux) data_flowdn,
																												sum(b.gprs_duration) call_duration
																											FROM dwv.dwv_d_sy_s_second_gprs_wl_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' b
																											GROUP BY
																												b.device_number,
																												b.system_type,
																												b.old_mns_type,
																												b.service_itme,
																												b.old_roam_type,
																												b.gprs_type,
																												b.discount_type) x --dw_mis_gprs_flow_db_1
																								LEFT JOIN dim.dim_yx_gprs_content y
																									ON x.service_itme =
																											y.service_code
																								GROUP BY
																									x.msisdn) b --jlcrm.dw_mis_gprs_flow_db_$op_time
																			ON a.device_number = b.product_no
																		WHERE b.hj_flow > 0
																					AND substr(a.brand, 5, 2) <> ''it'') b
													ON a.product_no = b.product_no
												LEFT JOIN (
																		SELECT
																			DISTINCT
																			a.product_no -- count(distinct a.product_no)
																		FROM (
																					SELECT
																						user_id,
																						device_number product_no,
																						area_id,
																						city_id,
																						row_number()
																						OVER (PARTITION BY device_number
																							ORDER BY innet_date DESC) rn
																					FROM dwv.dwv_d_kh_b_user_info_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||'
																					WHERE brand IN (''2230d0'', ''2230yk'')) a --jlcrm.tl_datacard_u
																		INNER JOIN (
																								SELECT
																									x.msisdn AS product_no,
																									sum(x.data_flowup +
																											x.data_flowdn) AS gprs_flow,
																									sum(x.call_duration) AS call_duration_m,
																									sum(x.data_flowdn) AS flow_down,
																									sum(x.data_flowup) AS flow_up,
																									sum(CASE
																											WHEN 1 = 1 AND
																														y.service_code IS NULL
																												THEN
																													x.data_flowup +
																													x.data_flowdn
																											ELSE
																												0
																											END) AS hj_flow
																								FROM (SELECT
																												a.device_number msisdn,
																												a.system_type,
																												a.old_mns_type mns_type,
																												a.service_itme,
																												a.old_roam_type roam_type,
																												a.gprs_type apnni,
																												a.discount_type,
																												sum(a.up_flux) data_flowup,
																												sum(a.down_flux) data_flowdn,
																												sum(a.gprs_duration) call_duration
																											FROM dwv.dwv_d_sy_s_second_gprs_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' a
																											WHERE a.service_itme NOT IN
																														(''1010000001'',
																															''1010000002'',
																															''1020000001'',
																															''1020000002'',
																															''1020000003'',
																															''1030000004'',
																															''1030000013'',
																															''1030000014'',
																															''1030000016'',
																															''1030000019'',
																															''1030000020'',
																															''1040000007'',
																															''1040000011'',
																															''1040000016'',
																															''1050000002'',
																															''1300149901'',
																															''1710000018'',
																															''1710000023'',
																															''1710000035'',
																															''1990000005'',
																															''2000000000'',
																															''2000000009'',
																															''2032500001'',
																															''2035710001'',
																															''2042000001'',
																															''4000000002'',
																															''4000000005'',
																															''4000000006'')
																											GROUP BY
																												a.device_number,
																												a.system_type,
																												a.old_mns_type,
																												a.service_itme,
																												a.old_roam_type,
																												a.gprs_type,
																												a.discount_type
																											UNION ALL
																											SELECT
																												b.device_number msisdn,
																												b.system_type,
																												b.old_mns_type mns_type,
																												b.service_itme,
																												b.old_roam_type roam_type,
																												b.gprs_type apnni,
																												b.discount_type,
																												sum(b.up_flux) data_flowup,
																												sum(b.down_flux) data_flowdn,
																												sum(b.gprs_duration) call_duration
																											FROM dwv.dwv_d_sy_s_second_gprs_wl_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' b
																											GROUP BY
																												b.device_number,
																												b.system_type,
																												b.old_mns_type,
																												b.service_itme,
																												b.old_roam_type,
																												b.gprs_type,
																												b.discount_type) x --dw_mis_gprs_flow_db_1
																								LEFT JOIN dim.dim_yx_gprs_content y
																									ON x.service_itme =
																											y.service_code
																								GROUP BY
																									x.msisdn) b --jlcrm.dw_mis_gprs_flow_db_$op_time
																			ON a.product_no = b.product_no
																		LEFT JOIN (
																								SELECT
																									DISTINCT
																									a.product_no --count(distinct a.product_no)
																								FROM (
																											SELECT
																												x.msisdn AS product_no,
																												0 AS city_id,
																												sum(x.data_flowup +
																														x.data_flowdn) AS gprs_flow,
																												sum(x.call_duration) AS call_duration_m,
																												sum(x.data_flowdn) AS flow_down,
																												sum(x.data_flowup) AS flow_up,
																												sum(CASE
																														WHEN 1 = 1 AND
																																	y.service_code IS NULL
																															THEN
																																x.data_flowup +
																																x.data_flowdn
																														ELSE
																															0
																														END) AS hj_flow
																											FROM (SELECT
																															a.device_number msisdn,
																															a.system_type,
																															a.old_mns_type mns_type,
																															a.service_itme,
																															a.old_roam_type roam_type,
																															a.gprs_type apnni,
																															a.discount_type,
																															sum(a.up_flux) data_flowup,
																															sum(a.down_flux) data_flowdn,
																															sum(a.gprs_duration) call_duration
																														FROM dwv.dwv_d_sy_s_second_gprs_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' a
																														WHERE a.service_itme NOT IN
																																	(''1010000001'',
																																		''1010000002'',
																																		''1020000001'',
																																		''1020000002'',
																																		''1020000003'',
																																		''1030000004'',
																																		''1030000013'',
																																		''1030000014'',
																																		''1030000016'',
																																		''1030000019'',
																																		''1030000020'',
																																		''1040000007'',
																																		''1040000011'',
																																		''1040000016'',
																																		''1050000002'',
																																		''1300149901'',
																																		''1710000018'',
																																		''1710000023'',
																																		''1710000035'',
																																		''1990000005'',
																																		''2000000000'',
																																		''2000000009'',
																																		''2032500001'',
																																		''2035710001'',
																																		''2042000001'',
																																		''4000000002'',
																																		''4000000005'',
																																		''4000000006'')
																														GROUP BY
																															a.device_number,
																															a.system_type,
																															a.old_mns_type,
																															a.service_itme,
																															a.old_roam_type,
																															a.gprs_type,
																															a.discount_type
																														UNION ALL
																														SELECT
																															b.device_number msisdn,
																															b.system_type,
																															b.old_mns_type mns_type,
																															b.service_itme,
																															b.old_roam_type roam_type,
																															b.gprs_type apnni,
																															b.discount_type,
																															sum(b.up_flux) data_flowup,
																															sum(b.down_flux) data_flowdn,
																															sum(b.gprs_duration) call_duration
																														FROM dwv.dwv_d_sy_s_second_gprs_wl_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' b
																														GROUP BY
																															b.device_number,
																															b.system_type,
																															b.old_mns_type,
																															b.service_itme,
																															b.old_roam_type,
																															b.gprs_type,
																															b.discount_type) x --dw_mis_gprs_flow_db_1
																											LEFT JOIN dim.dim_yx_gprs_content y
																												ON x.service_itme =
																														y.service_code
																											GROUP BY
																												x.msisdn) a --jlcrm.dw_mis_gprs_flow_db_$op_time
																								INNER JOIN (
																														SELECT
																															DISTINCT
																															device_number AS product_no
																														FROM dwv.dwv_d_sy_s_second_gprs_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' a
																														WHERE system_type = ''gl'') c
																									ON (a.product_no =
																											c.product_no)
																								WHERE a.hj_flow > 0) c --jlcrm.tl_gprs_flow_phone_u3
																			ON a.product_no = c.product_no
																		LEFT JOIN (
																								SELECT
																									a.device_number product_no --count(a.device_number)
																								FROM dwv.dwv_d_kh_s_user_wlw_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' a --jlcrm.stat_ent_wulianwang_$op_time
																								INNER JOIN (
																														SELECT
																															x.msisdn AS product_no,
																															0 AS city_id,
																															sum(x.data_flowup +
																																	x.data_flowdn) AS gprs_flow,
																															sum(x.call_duration) AS call_duration_m,
																															sum(x.data_flowdn) AS flow_down,
																															sum(x.data_flowup) AS flow_up,
																															sum(CASE
																																	WHEN 1 = 1 AND
																																				y.service_code IS NULL
																																		THEN
																																			x.data_flowup +
																																			x.data_flowdn
																																	ELSE
																																		0
																																	END) AS hj_flow
																														FROM (SELECT
																																		a.device_number msisdn,
																																		a.system_type,
																																		a.old_mns_type mns_type,
																																		a.service_itme,
																																		a.old_roam_type roam_type,
																																		a.gprs_type apnni,
																																		a.discount_type,
																																		sum(a.up_flux) data_flowup,
																																		sum(a.down_flux) data_flowdn,
																																		sum(a.gprs_duration) call_duration
																																	FROM dwv.dwv_d_sy_s_second_gprs_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' a
																																	WHERE a.service_itme NOT IN
																																				(''1010000001'',
																																					''1010000002'',
																																					''1020000001'',
																																					''1020000002'',
																																					''1020000003'',
																																					''1030000004'',
																																					''1030000013'',
																																					''1030000014'',
																																					''1030000016'',
																																					''1030000019'',
																																					''1030000020'',
																																					''1040000007'',
																																					''1040000011'',
																																					''1040000016'',
																																					''1050000002'',
																																					''1300149901'',
																																					''1710000018'',
																																					''1710000023'',
																																					''1710000035'',
																																					''1990000005'',
																																					''2000000000'',
																																					''2000000009'',
																																					''2032500001'',
																																					''2035710001'',
																																					''2042000001'',
																																					''4000000002'',
																																					''4000000005'',
																																					''4000000006'')
																																	GROUP BY
																																		a.device_number,
																																		a.system_type,
																																		a.old_mns_type,
																																		a.service_itme,
																																		a.old_roam_type,
																																		a.gprs_type,
																																		a.discount_type
																																	UNION ALL
																																	SELECT
																																		b.device_number msisdn,
																																		b.system_type,
																																		b.old_mns_type mns_type,
																																		b.service_itme,
																																		b.old_roam_type roam_type,
																																		b.gprs_type apnni,
																																		b.discount_type,
																																		sum(b.up_flux) data_flowup,
																																		sum(b.down_flux) data_flowdn,
																																		sum(b.gprs_duration) call_duration
																																	FROM dwv.dwv_d_sy_s_second_gprs_wl_accu_1_prt_m'||V_MONTH||'_2_prt_d'||V_LAST_DAY||' b
																																	GROUP BY
																																		b.device_number,
																																		b.system_type,
																																		b.old_mns_type,
																																		b.service_itme,
																																		b.old_roam_type,
																																		b.gprs_type,
																																		b.discount_type) x --dw_mis_gprs_flow_db_1
																														LEFT JOIN dim.dim_yx_gprs_content y
																															ON x.service_itme =
																																	y.service_code
																														GROUP BY
																															x.msisdn) b --jlcrm.dw_mis_gprs_flow_db_$op_time
																									ON a.device_number =
																										b.product_no
																								WHERE b.hj_flow > 0
																											AND substr(a.brand, 5, 2) <> ''it'') d --jlcrm.tl_gprs_flow_phone_u2
																			ON a.product_no = d.product_no
																		WHERE b.hj_flow > 0
																					AND a.rn = 1
																					AND c.product_no IS NULL
																					AND d.product_no IS NULL) c
													ON a.product_no = c.product_no
												WHERE b.product_no IS NULL
															AND c.product_no IS NULL) b
						ON a.product_no = b.product_no
				) a
				left join
				(
					SELECT
						USER_ID,
						coalesce(SUM(ACCT_FEE - FAV_FEE), 0) / 100 FEE,
						coalesce(SUM(ACCT_FEE - FAV_FEE - PAYED_TAX / 100), 0) / 100 SH_FEE,
						coalesce(SUM(CASE WHEN ITEM_CLASS = ''118''
							THEN ACCT_FEE - FAV_FEE END), 0) / 100 FEE_118,
            coalesce(SUM(CASE WHEN C.zhb_name LIKE ''%话%''
							THEN ACCT_FEE - FAV_FEE END), 0) / 100 FEE_TH
					FROM DWV.DWV_M_ZW_S_ACCTBILL_KH_1_PRT_P_'||V_MONTH||' A
					LEFT JOIN DIM.DIM_ACCT_ITEM_CLASS B
            ON A.ACCT_ITEM_CODE = B.ITEM_CODE
          LEFT JOIN (
                          SELECT
                            b.item_id,
                            a.zhb_name,
                            boss_item
                          FROM DWA.temp_cwdb_fee1_d_hkcwbsr_zhb_2005 a,
                          DWA.temp_cwdb_fee1_d_bill_subject_report b
                          WHERE (a.zhb_name LIKE ''移动网业务收入-港澳台长话%''
                                OR a.zhb_name LIKE ''移动网业务收入-国际长话%''
                                OR a.zhb_name LIKE ''移动网业务收入-基本通话%''
                                OR a.zhb_name LIKE ''移动网业务收入-省际长话%''
                                OR a.zhb_name LIKE ''移动网业务收入-省内长话%''
                                OR a.zhb_name LIKE ''%移动网业务收入-IP电话-手机用户一次拨号%''
                                OR a.zhb_name LIKE ''%移动网业务收入-月租费收入%'')
                                AND b.ywsr_id = a.zhb_id AND b.item_id <> ''010006'') C
                ON a.ACCT_ITEM_CODE = c.boss_item
					GROUP BY
							USER_ID
				) b--取每个用户的账单收入
				on a.user_id = b.user_id
				left join
				(
						SELECT
								A.USER_ID,
								SUM(A.PAYED_LATER+A.PAYED_PREPAY) / 100  AS DISCOUNT_FEE
						FROM DWI.DWI_M_ZW_WRITEOFF_INFO_1_PRT_P_'||V_MONTH||' A
						WHERE A.PAY_TYPE IN ( SELECT PAY_TYPE FROM DIM.DIM_BAL_BOOKTYPE_DICT WHERE SUBSTR(PAY_ATTR, 6, 1) = ''1'' )
						GROUP BY A.USER_ID
				) c
				on b.user_id = c.user_id
				GROUP BY
							a.area_id,
							a.city_id,
							a.user_id
'''

res = set()

b = a.split('\n')
for i in b:
    res1 = re.findall(p1, i)
    if res1:
        res.add(res1[0])

print(res)

