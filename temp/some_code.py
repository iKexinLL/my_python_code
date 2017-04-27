


# if len(sys.argv == 1 or sys.argv[1] in {'-h','--help'})
# 程序的工作目录(work path) os.getcwd() 
# 更改工作目录(work path) os.chdir()
# os.walk() 遍历, os.listdir()不会

import sys 

def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h","--help"}:
        print('usage :{0} [en|fr] number'.format(sys.argv[0]))
        sys.exit()

    args = sys.argv[1:]
    if args[0] in {'en','fr'}:
        global Language
        Language = args.pop(0)
        print(args)
        print('Language is ' + Language)

    print('after ' + Language)



main()
