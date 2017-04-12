
import import_test

cls = import_test.ConnectGP()


print(cls.execute('select 3'))

cls.close_all()