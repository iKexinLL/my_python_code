import psycopg2 as psy

def get_gpfunc(func_name):
    conn = psy.connect(database = 'jlbdbi', host = '10.163.170.33', user = 'dwa', password = 'D#wa29bonc', port = '5432')
    cur = conn.cursor()

    sql = '''
        select distinct p.proname, p.prosrc
        from pg_catalog.pg_namespace n
        join pg_catalog.pg_proc p
        on p.pronamespace = n.oid
        where p.proname = '%s' -- 这里修改
    order by 1'''%func_name

    cur.execute(sql)
    res = cur.fetchall()

    path = r'e:\%s.sql'%func_name

    with open(path, 'w', encoding = 'utf-8') as f:
        f.write(res[0][1])

    print(path)

    cur.close()
    conn.close()


