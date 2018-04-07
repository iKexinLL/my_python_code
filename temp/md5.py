import sys;    
import hashlib;    
import os.path;  
    
def GetFileMd5(strFile):  
    file = None;  
    bRet = False;  
    strMd5 = "";  
    strSha1 = "";  
    try:  
        file = open(strFile, "rb");  
        md5 = hashlib.md5();  
        sha1 = hashlib.sha1();  
        strRead = "";  
        while True:    
            strRead = file.read(8096);    
            if not strRead:  
                break;  
            else:  
                md5.update(strRead);  
                sha1.update(strRead);  
        #read file finish  
        bRet = True;  
        strMd5  = md5.hexdigest();  
        strSha1 = sha1.hexdigest();  
    except:  
        bRet = False;  
    finally:  
        if file:  
            file.close()  
    return [bRet, strMd5, strSha1];  
      
def writFile(strInfo):  
    file = None;  
    file = open("E:\\1.txt", 'w+');  
    file.write(strInfo);  
    file.write("\n");  
    if file:  
        file.close();  
  
    
if "__main__" == __name__:    
   bOK , md5str1, sha1str1 = GetFileMd5(r"E:\temp\temp_r\cn_windows_7_ultimate_with_sp1_x64_dvd_u_677408.iso");  
   print(md5str1);  
   md5All = md5str1 + "\t" + sha1str1;  
   md5All += "\n";  
     
   # bOK , md5str2, sha1str2 = GetFileMd5("E:\\2.mp3");  
   # print(md5str2);  
   # writFile(md5str2 + "\t" +sha1str2);  
   # md5All += (md5str2 + "\t" + sha1str2);  
   # md5All += "\n";  
   #   
   # bOK , md5str3, sha1str3 = GetFileMd5("E:\\3.mp3");  
   # print(md5str3);  
   # writFile(md5str3 + "\t" +sha1str3);  
   # md5All += (md5str2 + "\t" + sha1str3);  
   # md5All += "\n";  
   #   
   # writFile(md5All)