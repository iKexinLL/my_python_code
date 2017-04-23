

# 输出 营销和管理相关数据 
'''
由于在gp中,查询结果的行(没有order by)是随机排序的,所以需要转换成自己需要的格式
'''
import datetime
last_month = datetime.datetime.strftime(datetime.date.today().replace(day=1) - datetime.timedelta(1), '%Y%m')


chanpin_table_one_print_total_sql = '''		
        -- 表1 总 直接复制粘贴
        select
        product_code, billing_time, total_volume 
        from dwa_m_rpt_voice_pe_busi
		where acct_date = '201701'
		  and voice_pe_type = '总'
		order by 1
        '''

chanpin_table_one_print_tds_sql = '''		
        -- 表1 TDS 直接复制粘贴
        select 
        product_code, billing_time, total_volume 
        from dwa_m_rpt_voice_pe_busi
		where acct_date = '201701'
		  and voice_pe_type = 'TDS'
		order by 1
        '''
chanpin_table_two_print_zong_sql = '''	
     -- 表二 总
     -- p_dwa_m_rpt_nonvoice_pe_busi_zong
     select product_code, billing_volume, total_volume 
	 from DWA_M_RPT_NONVOICE_PE_BUSI 
     where acct_date = '201701'
	   and voice_pe_type ='总'
      '''

chanpin_table_two_print_tds_sql = '''	
    -- 表二 tds 直接复制粘贴
    select 
        product_code, total_volume 
	from DWA_M_RPT_NONVOICE_PE_BUSI 
	where acct_date = '201701'
	  and voice_pe_type ='TDS'
	order by 1
    '''

chanpin_table_two_print_lte_sql = '''	
    -- 表二 lte 直接复制粘贴
    select 
        product_code, total_volume 
	from DWA_M_RPT_NONVOICE_PE_BUSI 
	where acct_date = '201701'
	  and voice_pe_type ='LTE'
	order by 1
    '''
chanpin_table_three_print_zong_sql = '''
    -- 表三 总 直接复制粘贴
    select 
        wap_billing_time, wap_total_volume, '语音清单', data_card_billing_time, data_card_total_volume, '语音清单', fetion_billing_time, fetion_total_volume, '语音清单', billing_time_139, total_volume_139, '语音清单', wireless_music_billing_time, wireless_music_total_volume, '语音清单', mobile_news_billing_time, mobile_news_total_volume, '语音清单', and_read_billing_time, and_read_total_volume, '语音清单', and_game_billing_time, and_game_total_volume, '语音清单', and_vedio_billing_time, and_vedio_total_volume, '语音清单', and_cartoon_billing_time, and_cartoon_total_volume, '语音清单', and_pay_billing_time, and_pay_total_volume, '语音清单', mobile_tv_billing_time, mobile_tv_total_volume, '语音清单', billing_time_12580, total_volume_12580, '语音清单', nongxintong_billing_time, nongxintong_total_volume, '语音清单', black_berry_billing_time, black_berry_total_volume, '语音清单', and_addr_book_billing_time, and_addr_total_volume, '语音清单', mm_billing_time, mm_total_volume, '语音清单', and_map_billing_time, and_map_total_volume, '语音清单', and_vision_billing_time, and_vision_total_volume, '语音清单', billing_time_12590, total_volume_12590, '语音清单', billing_time_12585, total_volume_12585, '语音清单', and_work_billing_time, and_work_total_volume, '语音清单', and_pay_nfc_billing_time, and_pay_nfc_total_volume, '语音清单', traffic_flux_billing_time, traffic_flux_total_volume, '语音清单'
    from DWA_M_RPT_A_VOICE_PE_BUSI
    where acct_date = '201701'
    and nonvoice_pe_type = '总'
    order by product_code 
        '''
chanpin_table_three_print_tds_sql = '''
    -- 表三 TDS 直接复制粘贴
    select 
        wap_billing_time,  data_card_billing_time,  fetion_billing_time,  billing_time_139,  wireless_music_billing_time,  mobile_news_billing_time,  and_read_billing_time,  and_game_billing_time,  and_vedio_billing_time,  and_cartoon_billing_time,  and_pay_billing_time,  mobile_tv_billing_time,  billing_time_12580,  nongxintong_billing_time,  black_berry_billing_time,  and_addr_book_billing_time,  mm_billing_time,  and_map_billing_time,  and_vision_billing_time,  billing_time_12590,  billing_time_12585,  and_work_billing_time,  and_pay_nfc_billing_time,  traffic_flux_billing_time    from DWA_M_RPT_A_VOICE_PE_BUSI
    where acct_date = '201701'
    and nonvoice_pe_type = 'TDS'
    order by product_code 
        '''

chanpin_table_four_print_zong_sql = '''
    -- 表四 总
    -- p_dwa_m_rpt_a_nonvoice_pe_busi
	select 
		product_code,
        wap_billing_busi, wap_total_volume, '流量',nvl(data_card_billing_busi,'0'), nvl(data_card_total_volume,'0'), '流量',fetion_billing_busi, fetion_total_volume, '流量',billing_busi_139, total_volume_139, '流量',wireless_music_billing_busi, wireless_music_total_volume, '流量',mobile_news_billing_busi, mobile_news_total_volume, '流量',and_read_billing_busi, and_read_total_volume, '流量',and_game_billing_busi, and_game_total_volume, '流量',and_vedio_billing_busi, and_vedio_total_volume, '流量',and_cartoon_billing_busi, and_cartoon_total_volume, '流量',and_pay_billing_busi, and_pay_total_volume, '流量',mobile_tv_billing_busi, mobile_tv_total_volume, '流量',billing_busi_12580, total_volume_12580, '流量',nongxintong_billing_busi, nongxintong_total_volume, '流量',black_berry_billing_busi, black_berry_total_volume, '流量',and_addr_book_billing_busi, and_addr_total_volume, '流量',mm_billing_busi, mm_total_volume, '流量',and_map_billing_busi, and_map_total_volume, '流量',and_vision_billing_busi, and_vision_total_volume, '流量',billing_busi_12590, total_volume_12590, '流量',billing_busi_12585, total_volume_12585, '流量',and_work_billing_busi, and_work_total_volume, '流量',and_pay_nfc_billing_busi, and_pay_nfc_total_volume, '流量',traffic_flux_billing_busi, traffic_flux_total_volume, '流量'
	from DWA_M_RPT_A_NONVOICE_PE_BUSI
	where acct_date = '201701' 
	and nonvoice_pe_type = '总'
	order by product_code 
    '''

chanpin_table_four_print_tds_sql = '''
    -- 表四 TDS 直接复制粘贴
	select 
        wap_billing_busi, nvl(data_card_billing_busi,'0'), fetion_billing_busi, billing_busi_139, wireless_music_billing_busi, mobile_news_billing_busi, and_read_billing_busi, and_game_billing_busi, and_vedio_billing_busi, and_cartoon_billing_busi, and_pay_billing_busi, mobile_tv_billing_busi, billing_busi_12580, nongxintong_billing_busi, black_berry_billing_busi, and_addr_book_billing_busi, mm_billing_busi, and_map_billing_busi, and_vision_billing_busi, billing_busi_12590, billing_busi_12585, and_work_billing_busi, and_pay_nfc_billing_busi, traffic_flux_billing_busi
	from DWA_M_RPT_A_NONVOICE_PE_BUSI
	where acct_date = '201701' 
	and nonvoice_pe_type = 'TDS'
	order by product_code 
    '''

chanpin_table_four_print_lte_sql = '''
    -- 表四 LTE 直接复制粘贴
	select 
        wap_billing_busi, nvl(data_card_billing_busi,'0'), fetion_billing_busi, billing_busi_139, wireless_music_billing_busi, mobile_news_billing_busi, and_read_billing_busi, and_game_billing_busi, and_vedio_billing_busi, and_cartoon_billing_busi, and_pay_billing_busi, mobile_tv_billing_busi, billing_busi_12580, nongxintong_billing_busi, black_berry_billing_busi, and_addr_book_billing_busi, mm_billing_busi, and_map_billing_busi, and_vision_billing_busi, billing_busi_12590, billing_busi_12585, and_work_billing_busi, and_pay_nfc_billing_busi, traffic_flux_billing_busi
	from DWA_M_RPT_A_NONVOICE_PE_BUSI
	where acct_date = '201701' 
	and nonvoice_pe_type = 'LTE'
	order by product_code 
    '''
    
chanpin_table_five_sql = '''
# WLAN 时长合计, 直接复制粘贴
select round(sum(call_duration)/60,2) from dwv.DWV_M_SY_S_WLAN_1_prt_p_%s ; 
''' %last_month



yingxiao_table_one_print_sql = ''' 
    -- 营销和管理相关数据 表1
    -- p_dwa_m_key_prod_cust_grp_income
    select 
        product_code,
        p_01,
        p_02,
        p_05,
        p_03,
        p_04,
        p_06,
        p_17,
        p_09,
        p_10,
        p_07,
        p_12,
        p_13,
        p_18,
        p_19,
        p_21,
        p_22,
        p_23,
        p_24,
        p_25,
        p_26,
        p_27,
        p_28,
        p_29,
        p_30,
        p_32,
        p_33,
        p_34
    from dwa_m_key_prod_cust_grp_income
    where acct_date = '%s'
'''%last_month

yingxiao_table_three_print_sql = '''    
    -- 营销和管理相关数据 表3 
    -- p_dwa_m_key_prod_cust_number
    select 
        product_code,
        nvl(sum(case when acct_date = '201701' then kpi_value end),0) as a201701,
        nvl(sum(case when acct_date = '201702' then kpi_value end),0) as a201702,
        nvl(sum(case when acct_date = '201703' then kpi_value end),0) as a201703,
        nvl(sum(case when acct_date = '201704' then kpi_value end),0) as a201704,
        nvl(sum(case when acct_date = '201705' then kpi_value end),0) as a201705,
        nvl(sum(case when acct_date = '201706' then kpi_value end),0) as a201706,
        nvl(sum(case when acct_date = '201707' then kpi_value end),0) as a201707,
        nvl(sum(case when acct_date = '201708' then kpi_value end),0) as a201708,
        nvl(sum(case when acct_date = '201709' then kpi_value end),0) as a201709,
        nvl(sum(case when acct_date = '201710' then kpi_value end),0) as a201710,
        nvl(sum(case when acct_date = '201711' then kpi_value end),0) as a201711,
        nvl(sum(case when acct_date = '201712' then kpi_value end),0) as a201712
    from dwa_m_key_prod_cust_number
    group by 1'''


chanpin_table_two_title_zong = '''PE-30
PE-31
PE-32
PE-33
PE-34
PE-35
PE-36
PE-37
PE-38
PE-81
PE-82
PE-62
PE-63
PE-64
PE-65
PE-66
PE-67
PE-68
PE-69
PE-70
PE-71
PE-72
PE-73
PE-42
PE-43
PE-44
PE-45
PE-46
PE-47
PE-48
PE-49'''.split()

chanpin_table_four_title = '''PE-81 
PE-82 
PE-64 
PE-65 
PE-68 
PE-69 
PE-72 
PE-73 
PE-42 
PE-43 
PE-44 
PE-45 
PE-46 '''.split()

yingxiao_table_one_title = '''存量客户群收入
新增客户群收入
享受TD手机终端补贴的客户群收入
社会渠道发展的享受TD手机终端补贴的客户群收入
社会渠道发展的新增客户群收入
社会渠道发展的新增188号段客户群收入
社会渠道发展的客户群收入
享受LTE手机终端补贴的客户群收入
社会渠道发展的享受LTE手机终端补贴的客户群收入'''.split()


yingxiao_table_three_title = '''P-06 
P-17 
P-09 
P-07
P-12
P-13
P-18
P-19
P-21
P-22
P-23
P-24
P-25
P-26
P-27
P-28
P-29
P-30
P-32
P-33
P-34'''.split()


print(chanpin_table_one_print_total_sql)
print(chanpin_table_one_print_tds_sql)
print(chanpin_table_two_print_zong_sql)
print(chanpin_table_two_print_tds_sql)
print(chanpin_table_two_print_lte_sql)
print(chanpin_table_three_print_zong_sql)
print(chanpin_table_three_print_tds_sql)
print(chanpin_table_four_print_zong_sql)
print(chanpin_table_four_print_tds_sql)
print(chanpin_table_four_print_lte_sql)
print(yingxiao_table_one_print_sql)
print(yingxiao_table_three_print_sql)
print(chanpin_table_five_sql)
#end region

def the_print(data, title):
    tmp_res = data.split('\n')
    tmp_d = {}
    for i in tmp_res:
        tmp = i.split('\t')
        tmp_d[tmp[0]] = tmp[1:]

    for  i in title:
        for m in tmp_d[i]:
            print(m, end=' ')
        print()

# 产品 表二 总
def p_dwa_m_rpt_nonvoice_pe_busi_zong(b):
    the_print(b, chanpin_table_two_title_zong)

# 产品 表四 总
def p_dwa_m_rpt_a_nonvoice_pe_busi(b):
    the_print(b, chanpin_table_four_title)

# 营销和管理相关数据 表1
def p_dwa_m_key_prod_cust_grp_income(b):
    the_print(b, yingxiao_table_one_title)

# 营销和管理相关数据 表3 
def p_dwa_m_key_prod_cust_number(b):
    the_print(b, yingxiao_table_three_title)








