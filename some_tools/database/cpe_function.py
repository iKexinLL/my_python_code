# encoding=utf-8
"""
Created on 2016/9/5 10:04
author: iKexinLL
先跑一下CPE的数据
"""



sql = '''
create table chkuser.tmp_wxkd_all_plan_dt  as -- drop table chkuser.tmp_wxkd_all_plan_dt; select * from chkuser.tmp_wxkd_all_plan_dt
select
    t.*
from
(
    select
        month_id || day_id as op_time,
        a.user_id,
        substr(a.eff_date,1,8) as begin_time,
        substr(a.exp_date,1,8) as end_time,
        substr(a.create_date,1,8) as order_day,
        a.login_no as emp_id,
        a.prc_id as plan_id,
        b.plan_type,
        a.status,
        row_number() over (partition by a.user_id ,b.plan_type ,substr(a.eff_date,1,8) order by  a.status  ) rm
    from dwi.dwi_d_kh_user_prod_1_prt_m201604_2_prt_d30 a
    inner join chkuser.temp_dim_cpe_he_table b on a.prc_id = b.mode_code
    left  join chkuser.dim_temp_mifi_emp c on a.login_no = c.emp_id and b.plan_type = 2 -- 没插入 plan_type为2的产品
    where c.emp_id is null
)  t
where rm = 1
DISTRIBUTED BY(user_id)
'''