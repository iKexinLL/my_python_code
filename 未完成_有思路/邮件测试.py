import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime
email = 'kongpahuixiao@sina.com'
passwd = 'ikexinll123456'
pop_server = 'pop.sina.com'

proxy_addr = proxy_ip = '10.161.72.126'
proxy_port = '808'

# 不好使....
import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,proxy_ip,proxy_port,True)
socket.socket = socks.socksocket
# socket.getaddrinfo('www.baidu.com',80,0,0,socket.SOL_TCP)

def get_email():
    server = poplib.POP3_SSL(pop_server,'995')
    # 可以打开或关闭调试信息:
    # server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))
    server.user(email)
    server.pass_(passwd)
    #邮件数量和占有空间
    print('Messages: %s. Size: %s' % server.stat())
    #list()返回所有邮件编号
    resp_one,mails,octets_one = server.list()
    #查看返回列表
    #print(mails)
    #获取最新的一封邮件，索引号为1开始
    index = len(mails)
    resp_two, lines, octets_two = server.retr(index)
    #lines存储邮件原始文本每行并进行解析
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    #可以根据邮件索引从服务器删除邮件
    #server.dele(index)
    #关闭邮件
    server.quit()
    print_info(msg)

