# easytoyou_script
easytoyou批量解密脚本
【需要一个easy2you的会员帐号】
# 配置 (options)


```
ez2u.py
    class options:
        sourceFolder = "" # need decode path
        dstFolder = '' # save path
        ez2uURL = 'https://easytoyou.eu/decoder/ic10php56/'
        reqHeader = {}
        reqHeader['Cookie'] = '' #登录状态的会员账号的cookie
        reqHeader['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        errorLogPath = dstFolder + 'error.log' # errorlog path
        timeZone=-7 #CN to EU 
        reqTimeout=20 #request timeout
```
- sourceFolder：输入目录
- dstFolder：输出目录
- ez2uURL：解密站点路径
- reqHeader：header头
- timeZone：你所在的时区与欧洲相差的时间（例如：北京时间8点，那么欧洲时间为1点，相差7小时，故-7）
- reqTimeout：请求超时时间
配置好后执行`python3 ez2u.py`即可

# 需求
- python3
- bs4、requests、lxml

# Use
1. sign up a ez2u account
2. login ez2u and copy `Response Cookie`
3. paste cookie into ez2u.py `reqHeader['Cookie']`
4. set `timeZone` `dstFolder` `sourceFolder`to right value
5. run `python3 ez2u.py`
