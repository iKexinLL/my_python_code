#coding=utf-8

#利用正则,在SQL中找到表名

import re

#表名存在于 from, join, into 后面
p = re.compile('(from *\w*\.*\w*|into *\w*\.*\w*|join *\w*\.*\w*)',re.IGNORECASE)



V_SQL = '''
INSERT INTO temp_table
                              SELECT 
                                        CASE WHEN OLD_ROAM_TYPE = ''0'' 
                                                         THEN ''PE-01'' -- 非漫游通话用户数,计费时长
                                                 WHEN OLD_ROAM_TYPE = ''4'' 
                                                         THEN ''PE-02'' -- 国内出访漫游基本话费用户数,计费时长
                                                 WHEN OLD_ROAM_TYPE = ''8'' 
                                                         THEN ''PE-03'' -- 港、澳、台出访漫游基本用户数,计费时长
                                                 WHEN OLD_ROAM_TYPE IN (''6'',''7'') 
                                                         THEN ''PE-04'' -- 国际出访漫游基本话用户数, 计费时长
                                                 WHEN LONG_TYPE = ''05'' AND FEE_TYPE IN (''4,'',''5'',''6'',''7'')  
                                                         THEN ''PE-05'' -- 国际长话用户数, 计费时长
                                        ELSE ''OTHER'' END,
                                        COUNT(DISTINCT DEVICE_NUMBER) AS FIRST_VALUE,
                                        SUM(CALL_DURATION) AS SECOND_VALUE
                                FROM DWV.DWV_D_SY_S_SECOND_VOICE_ACCU_1_PRT_M'||V_MONTH||'_2_PRT_D'||V_LAST_DAY||'
                                WHERE SYSTEM_TYPE in(''vc'',''vn'',''vf'')
                                GROUP BY 1
                                UNION ALL
                                SELECT 
                                        CASE WHEN LONG_TYPE IN (''04'',''05'') AND FEE_TYPE IN (''5'',''6'',''7'')  
                                                THEN ''PE-06'' -- 国际及港澳台长话用户数,计费时长
                                        ELSE ''OTHER'' END,
                                        COUNT(DISTINCT DEVICE_NUMBER),
                                        SUM(CALL_DURATION)
                                FROM DWV.DWV_D_SY_S_SECOND_VOICE_ACCU_1_PRT_M'||V_MONTH||'_2_PRT_D'||V_LAST_DAY||'
                                WHERE SYSTEM_TYPE in(''vc'',''vn'',''vf'')
                                GROUP BY 1
                                UNION ALL
                                SELECT 
                                        ''PE-07'', -- 点对点短消息用户数,计费量
                                        COUNT(DISTINCT A.DEVICE_NUMBER),
                                        SUM(CDR_NUM)
                                FROM DWV.DWV_D_SY_S_SMS_ACCU_1_PRT_M'||V_MONTH||'_2_PRT_D'||V_LAST_DAY||' A  
                                WHERE A.SMS_DIRECT IN (''00'',''02'',''11'',''21'')
                                GROUP BY 1
                                UNION ALL
                                SELECT 
                                        CASE WHEN SUBSTR(SERV_CODE, 1, 4) IN (''1066'', ''1062'') 
                                                                OR SUBSTR(SERV_CODE, 1, 8) IN (''10658168'',''10658035'',''10658067'',''10658070'',''10658071'',''10658073'',''10658074'',''10658075'',''10658076'',''10658077'',''10658079'') 
                                                                OR SUBSTR(SERV_CODE, 1, 5) IN (''12590'') 
                                                                OR SUBSTR(SERV_CODE, 1, 5) IN (''12586'') 
                                                         THEN ''PE-08'' -- 梦网短信用户数,计费量
                                                 WHEN SUBSTR(SERV_CODE,1,5) IN (''10657'' ,''10650'',''10698'',''10699'') 
                                                                 OR SUBSTR(SERV_CODE,1,2) IN (''95'',''96'')
                                                         THEN ''PE-09'' -- 集团短信用户数,计费量
                                                 WHEN SERV_CODE IN (''10658221'',''12520'',''10658830'',''10658139'',''10658880'',''10658006'',''10658080'',''10658088'')
                                                         THEN ''PE-10'' -- 平台短信用户数,计费量
                                        ELSE ''OTHER'' END,
                                        COUNT(DISTINCT DEVICE_NUMBER),
                                        SUM(SP_NUM)
                                FROM DWV.DWV_D_SY_S_SP_ACCU_1_PRT_M'||V_MONTH||'_2_PRT_D'||V_LAST_DAY||'                
                                GROUP BY 1
                              UNION ALL
                              SELECT 
                                        CASE WHEN SERV_CODE IS NULL 
                                                         AND MM_TYPE = ''00''
                                                        AND APP_TYPE = ''0'' 
                                                 THEN ''PE-11'' -- 点对点彩信用户数,计费量
                                        ELSE ''OHTER'' END,
                                        COUNT(DISTINCT DEVICE_NUMBER),
                                        SUM(CDR_NUM)
                                FROM DWV.DWV_D_SY_S_MMS_ACCU_1_PRT_M'||V_MONTH||'_2_PRT_D'||V_LAST_DAY||'  
                                GROUP BY 1        
                                UNION ALL
                                SELECT 
                                        CASE WHEN A.SYSTEM_TYPE = ''cd'' 
                                                                 AND (SUBSTR (A.SERV_CODE,1,4) IN (''1062'',''1066'')  
                                                                                 OR SUBSTR (A.SERV_CODE,1,8) IN (''10658176'',''10658168'',''10658035'',''10658067'',''10658070'',''10658071'',
                                                                         ''10658072'',''10658073'',''10658074'',''10658075'',''10658076'',''10658077'',''10658079'')
                                                            OR SUBSTR(SERV_CODE,1,5) IN (''12590'') 
                                                            OR SUBSTR(SERV_CODE,1,5) IN (''12586'')
                                                        )
                                                 THEN ''PE-12'' -- 梦网彩信用户数,计费量
                                         WHEN (LENGTH(SERV_CODE)=5 
                                                                 AND (SERV_CODE LIKE ''100%'' OR SERV_CODE LIKE ''11%'' OR SERV_CODE LIKE ''12%'' OR SERV_CODE LIKE ''95%'' OR SERV_CODE LIKE ''96%'')
                                                   ) 
                                                      OR (LENGTH(SERV_CODE)=12 AND (SERV_CODE LIKE ''1069%'' OR SERV_CODE LIKE ''1063%'')) 
                                                      OR (LENGTH(SERV_CODE)=8 AND (SERV_CODE LIKE ''10690%'' OR SERV_CODE LIKE ''10699%'' OR SERV_CODE LIKE ''10630%'' OR SERV_CODE LIKE ''10639%''))
                                                 THEN ''PE-13'' -- 集团彩信用户数,计费量
                                         WHEN SERV_CODE IN (''10658221'',''12520'',''10658830'',''10658139'',''10658310'',''10658880'',''10658006'',''10658080'',''10658088'')
                                                 THEN ''PE-14'' -- 平台彩信用户数,计费量
                                        ELSE ''OTHER'' END,
                                        COUNT(DISTINCT DEVICE_NUMBER),
                                        SUM(CDR_NUM)
                                FROM DWV.DWV_D_SY_S_MMS_ACCU_1_PRT_M'||V_MONTH||'_2_PRT_D'||V_LAST_DAY||' A
                                GROUP BY 1
                                UNION ALL
                                SELECT 
                                        CASE WHEN PROD_PRC_NAME LIKE ''%主叫显示%'' 
                                                        THEN ''PE-15'' -- 主叫显示用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%手机邮箱%'' 
                                                         THEN ''PE-16'' -- 手机邮箱用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%飞信%'' 
                                                         THEN ''PE-17'' -- 飞信用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%咪咕音乐%'' 
                                                         THEN ''PE-18'' -- 咪咕音乐用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%手机报%'' 
                                                         THEN ''PE-19'' -- 手机报用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和阅读%'' 
                                                         THEN ''PE-20'' -- 和阅读用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和动漫%'' 
                                                         THEN ''PE-21'' -- 和动漫用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%农信通%'' 
                                                         THEN ''PE-22'' -- 农信通用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%语音杂志%'' 
                                                         THEN ''PE-23'' -- 语音杂志用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和彩印%'' 
                                                         THEN ''PE-24'' -- 和彩印用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和留言%'' 
                                                         THEN ''PE-25'' -- 和留言用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和生活%'' 
                                                         THEN ''PE-26'' -- 和生活用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%MobileMarket%'' 
                                                         THEN ''PE-27'' -- MobileMarket用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和游戏%'' 
                                                         THEN ''PE-28'' -- 和游戏用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%手机电视%'' 
                                                         THEN ''PE-29'' -- 手机电视用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和视频%'' 
                                                         THEN ''PE-30'' -- 和视频用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%位置服务%'' 
                                                         THEN ''PE-31'' -- 位置服务用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%手机证券%'' 
                                                         THEN ''PE-32'' -- 手机证券用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%来电提醒%'' 
                                                         THEN ''PE-33'' -- 来电提醒用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%移动气象%'' 
                                                         THEN ''PE-34'' -- 移动气象用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%物联网%'' 
                                                         THEN ''PE-35'' -- 物联网用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%梦网业务%'' 
                                                         THEN ''PE-36'' -- 梦网业务用户数
                                        ELSE ''OHTER'' END,
                                        COUNT(DISTINCT DEVICE_NUMBER),
                                        0
                                FROM DWI.DWI_M_KH_USER_PROD_1_PRT_P_'||V_MONTH||' A
                                INNER JOIN DIM.DIM_PD_PRC_DICT B
                                ON A.PRC_ID = B.PROD_PRCID 
                                INNER JOIN 
                                (
                                        SELECT
                                                USER_ID,
                                                DEVICE_NUMBER,
                                                IS_INNET
                                        FROM 
                                        (
                                                SELECT 
                                                        USER_ID,
                                                        DEVICE_NUMBER,
                                                        IS_INNET,
                                                        ROW_NUMBER() OVER(PARTITION BY DEVICE_NUMBER ORDER BY INNET_DATE) RN
                                                FROM DWV.DWV_M_KH_B_USER_INFO_1_PRT_P_'||V_MONTH||'
                                        ) T
                                        WHERE RN = 1
                                ) C
                                ON A.USER_ID = C.USER_ID 
                                GROUP BY 1
                                UNION ALL
                                SELECT 
                                        CASE WHEN PROD_PRC_NAME LIKE ''%手机邮箱%'' 
                                                        THEN ''PE-37''-- 手机邮箱活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%飞信%'' 
                                                         THEN ''PE-38'' -- 飞信活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%咪咕音乐%'' 
                                                         THEN ''PE-39'' -- 咪咕音乐活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%手机报%'' 
                                                         THEN ''PE-40'' -- 手机报活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和阅读%'' 
                                                         THEN ''PE-41'' -- 和阅读活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和动漫%'' 
                                                         THEN ''PE-42'' -- 和动漫活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%农信通%'' 
                                                         THEN ''PE-43'' -- 农信通活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%语音杂志%'' 
                                                         THEN ''PE-44'' -- 语音杂志活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和彩印%'' 
                                                         THEN ''PE-45'' -- 和彩印活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和留言%'' 
                                                         THEN ''PE-46'' -- 和留言活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和生活%'' 
                                                         THEN ''PE-47'' -- 和生活活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%MobileMarket%'' 
                                                         THEN ''PE-48'' -- MobileMarket
                                                 WHEN PROD_PRC_NAME LIKE ''%和游戏%'' 
                                                         THEN ''PE-49'' -- 和游戏活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%手机电视%'' 
                                                         THEN ''PE-50'' -- 手机电视活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%和视频%'' 
                                                         THEN ''PE-51'' -- 和视频活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%位置服务%'' 
                                                         THEN ''PE-52'' -- 位置服务活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%手机证券%'' 
                                                         THEN ''PE-53'' -- 手机证券活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%来电提醒%'' 
                                                         THEN ''PE-54'' -- 来电提醒活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%移动气象站%'' 
                                                         THEN ''PE-55'' -- 移动气象站活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%物联网%'' 
                                                         THEN ''PE-56'' -- 物联网活跃用户数
                                                 WHEN PROD_PRC_NAME LIKE ''%梦网业务%''  
                                                         THEN ''PE-58'' -- 梦网业务活跃用户数
                                        ELSE ''OHTER'' END,
                                        COUNT(DISTINCT DEVICE_NUMBER),
                                        0
                                FROM DWI.DWI_M_KH_USER_PROD_1_PRT_P_'||V_MONTH||' A
                                INNER JOIN DIM.DIM_PD_PRC_DICT B
                                ON A.PRC_ID = B.PROD_PRCID 
                                INNER JOIN 
                                (
                                        SELECT
                                                USER_ID,
                                                DEVICE_NUMBER,
                                                IS_INNET
                                        FROM 
                                        (
                                                SELECT 
                                                        USER_ID,
                                                        DEVICE_NUMBER,
                                                        IS_INNET,
                                                        ROW_NUMBER() OVER(PARTITION BY DEVICE_NUMBER ORDER BY INNET_DATE) RN
                                                FROM DWV.DWV_M_KH_B_USER_INFO_1_PRT_P_'||V_MONTH||'
                                        ) T
                                        WHERE RN = 1
                                ) C
                                ON A.USER_ID = C.USER_ID
                                INNER JOIN 
                                (
                                            SELECT 
                                                    USER_ID
                                        FROM DWV.DWV_M_ZW_S_ACCTBILL_KH_1_PRT_P_'||V_MONTH||' D
                                        INNER JOIN DIM.DIM_ACCT_ITEM_CLASS E
                                        ON D.ACCT_ITEM_CODE = E.ITEM_CODE
                                        WHERE D.ACCT_FEE - D.FAV_FEE > 0
                                        GROUP BY 
                                                USER_ID
                                ) D
                                ON C.USER_ID = D.USER_ID
                                GROUP BY 1
                                UNION ALL
                                SELECT 
                                        ''PE-59'', -- 手机上网用户数,已有SQL,但需要放到过程当中
                                        0,
                                        0
                                UNION ALL
                                SELECT
                                        ''PE-60'', -- 数据终端用户数
                                        0,
                                        0
                                UNION ALL
                                SELECT
                                        ''PE-61'', -- 物联网信息用户数
                                        COUNT(DISTINCT DEVICE_NUMBER),
                                        0
                                FROM DWV.DWV_M_KH_S_USER_WLW_1_PRT_'||V_MONTH||'
                                UNION ALL
                                SELECT
                                        ''PE-62'', -- CPE到达,未出,需要汇总
                                        0,
                                        0
                                UNION ALL
                                SELECT 
                                        ''PE-63'', -- WLAN用户数,上网流量
                                        COUNT(DISTINCT DEVICE_NUMBER),
                                        SUM(GPRS_FLOW)
                                FROM DWV.DWV_D_SY_S_WLAN_1_PRT_'||V_MONTH||'
                                UNION ALL
                                SELECT 
                                        ''PE-64'', -- WLAN上网单价
                                        SUM(GPRS_FLOW) / SUM(CFEE), -- 不确定,总流量/总费用
                                        0
                                FROM DWV.DWV_D_SY_S_WLAN_1_PRT_'||V_MONTH||'
                                UNION ALL        
                                SELECT
                                        ''PE-65'', -- 家庭宽带用户数
                                        COUNT(DISTINCT DEVICE_NUMBER)
                                        0                  
                                FROM DWV.DWV_D_KH_B_BAND_USER_INFO_1_PRT_'||V_MONTH||'                 
                                WHERE IS_ONNET = '1'
 '''



res = set(re.findall(p,V_SQL))

#去除"_1_PRT","FROM","JOIN"和一些空的结果

p_res = re.compile('(from +|into +|join +|_1_.*)',re.IGNORECASE)

for i in res:
    resu = re.sub(p_res,'',i)
    if resu:
        print(resu)
