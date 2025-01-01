
![HTB Banner](https://github.com/hackthebox/writeup-templates/blob/master/machine/assets/images/banner.png?raw=true)


- URL : 
- #easy 
- OS : #Linux 
- Machine Author(s): [nirza](https://app.hackthebox.com/users/800960)
- Hack Date: 2024-12-29,16:36

---

# Enumeration
ポートは20番、80番、3000番が空いてる
3000番は、well knownポートではない
- 
```bash

```

whatweb
- `http://greenhorn.htb/?file=welcome-to-greenhorn`
	- ディレクトリトラバーサルとかできないかな
```bash
└──╼ [★]$ whatweb http://greenhorn.htb
http://greenhorn.htb [302 Found] Cookies[PHPSESSID], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][nginx/1.18.0 (Ubuntu)], IP[10.129.207.200], RedirectLocation[http://greenhorn.htb/?file=welcome-to-greenhorn], nginx[1.18.0]
http://greenhorn.htb/?file=welcome-to-greenhorn [200 OK] Cookies[PHPSESSID], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][nginx/1.18.0 (Ubuntu)], IP[10.129.207.200], MetaGenerator[pluck 4.7.18], Pluck-CMS[4.7.18], Title[Welcome to GreenHorn ! - GreenHorn], nginx[1.18.0]

```

feroxbuster
- docsディレクトリの中のいくつか
```bash
└──╼ [★]$ feroxbuster -u http://greenhorn.htb
...
200      GET       41l      266w     1811c http://greenhorn.htb/docs/README
200      GET      676l     5644w    35068c http://greenhorn.htb/docs/COPYING
200      GET      182l     1236w     8535c http://greenhorn.htb/docs/CHANGES

```

dirbuster
robots.txtにアクセス出来る。
/data/・/docs/にはアクセスして欲しくなさそう
![[Pasted image 20241229171606.png]]
```bash
└──╼ [★]$ sudo dirsearch --url=http://greenhorn.htb

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/snowyowl644/HTBScript/reports/http_greenhorn.htb/_24-12-29_01-55-28.txt

Target: http://greenhorn.htb/

[01:55:28] Starting: 
[01:55:31] 200 -   93B  - /+CSCOT+/oem-customization?app=AnyConnect&type=oem&platform=..&resource-type=..&name=%2bCSCOE%2b/portal_inc.lua
[01:55:31] 200 -   93B  - /+CSCOT+/translation-table?type=mst&textdomain=/%2bCSCOE%2b/portal_inc.lua&default-language&lang=../
[01:55:32] 404 -  564B  - /.css
[01:55:32] 404 -  564B  - /.gif
[01:55:32] 404 -  564B  - /.ico
[01:55:33] 404 -  564B  - /.jpg
[01:55:33] 404 -  564B  - /.jpeg
[01:55:33] 404 -  564B  - /.png
[01:55:36] 404 -  564B  - /adm/style/admin.css
[01:55:36] 200 -    4KB - /admin.php
[01:55:37] 404 -  564B  - /admin_my_avatar.png
[01:55:41] 404 -  564B  - /bundles/kibana.style.css
[01:55:43] 301 -  178B  - /data  ->  http://greenhorn.htb/data/
[01:55:43] 200 -   48B  - /data/
[01:55:44] 200 -   93B  - /docpicker/common_proxy/http/www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com
[01:55:44] 301 -  178B  - /docs  ->  http://greenhorn.htb/docs/
[01:55:44] 403 -  564B  - /docs/
[01:55:45] 200 -   93B  - /faces/javax.faces.resource/web.xml?ln=../WEB-INF
[01:55:45] 200 -   93B  - /faces/javax.faces.resource/web.xml?ln=..\\WEB-INF
[01:55:45] 404 -  564B  - /favicon.ico
[01:55:45] 301 -  178B  - /files  ->  http://greenhorn.htb/files/
[01:55:45] 403 -  564B  - /files/
[01:55:47] 404 -  564B  - /IdentityGuardSelfService/images/favicon.ico
[01:55:47] 301 -  178B  - /images  ->  http://greenhorn.htb/images/
[01:55:47] 403 -  564B  - /images/
[01:55:47] 200 -    4KB - /install.php
[01:55:48] 200 -    4KB - /install.php?profile=default
[01:55:48] 200 -   93B  - /jmx-console/HtmlAdaptor?action=inspectMBean&name=jboss.system:type=ServerInfo
[01:55:49] 200 -    1KB - /login.php
[01:55:49] 404 -  564B  - /logo.gif
[01:55:50] 200 -   93B  - /manager/jmxproxy/?get=java.lang:type=Memory&att=HeapMemoryUsage
[01:55:50] 200 -   93B  - /manager/jmxproxy/?invoke=Catalina%3Atype%3DService&op=findConnectors&ps=
[01:55:54] 200 -   93B  - /plugins/servlet/gadgets/makeRequest?url=https://google.com
[01:55:55] 200 -   93B  - /proxy.stream?origin=https://google.com
[01:55:55] 200 -    2KB - /README.md
[01:55:55] 200 -   93B  - /remote/fgt_lang?lang=/../../../..//////////dev/cmdb/sslvpn_websession
[01:55:55] 200 -   93B  - /remote/fgt_lang?lang=/../../../../////////////////////////bin/sslvpnd
[01:55:55] 404 -  564B  - /resources/.arch-internal-preview.css
[01:55:56] 200 -   47B  - /robots.txt
[01:55:57] 404 -  564B  - /skin1_admin.css
[01:55:58] 404 -  997B  - /solr/admin/file/?file=solrconfig.xml
[01:56:03] 200 -   93B  - /wps/myproxy/http/www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com
[01:56:03] 200 -   93B  - /wps/contenthandler/!ut/p/digest!8skKFbWr_TwcZcvoc9Dn3g/?uri=http://www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com
[01:56:03] 200 -   93B  - /wps/common_proxy/http/www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com
[01:56:03] 200 -   93B  - /wps/cmis_proxy/http/www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com
[01:56:03] 200 -   93B  - /wps/proxy/http/www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com

Task Completed

```

いくつか、ディレクトラバーサルなどのwebリンクが見つかったので、アクセスするも、こんな文章が表示される
![[Pasted image 20241229171035.png]]


```bash

└──╼ [★]$ sudo dirsearch -u http://greenhorn.htb -t 50 -i 200

Target: http://greenhorn.htb/

[02:04:25] Starting: 
[02:04:25] 200 -   93B  - /+CSCOT+/translation-table?type=mst&textdomain=/%2bCSCOE%2b/portal_inc.lua&default-language&lang=../
[02:04:25] 200 -   93B  - /+CSCOT+/oem-customization?app=AnyConnect&type=oem&platform=..&resource-type=..&name=%2bCSCOE%2b/portal_inc.lua
[02:04:32] 200 -    4KB - /admin.php
[02:04:39] 200 -   48B  - /data/
[02:04:40] 200 -   93B  - /docpicker/common_proxy/http/www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com
[02:04:41] 200 -   93B  - /faces/javax.faces.resource/web.xml?ln=../WEB-INF
[02:04:41] 200 -   93B  - /faces/javax.faces.resource/web.xml?ln=..\\WEB-INF
[02:04:44] 200 -    4KB - /install.php
[02:04:44] 200 -    4KB - /install.php?profile=default
[02:04:44] 200 -   93B  - /jmx-console/HtmlAdaptor?action=inspectMBean&name=jboss.system:type=ServerInfo
[02:04:45] 200 -    1KB - /login.php
[02:04:46] 200 -   93B  - /manager/jmxproxy/?invoke=Catalina%3Atype%3DService&op=findConnectors&ps=
[02:04:46] 200 -   93B  - /manager/jmxproxy/?get=java.lang:type=Memory&att=HeapMemoryUsage
[02:04:50] 200 -   93B  - /plugins/servlet/gadgets/makeRequest?url=https://google.com
[02:04:51] 200 -   93B  - /proxy.stream?origin=https://google.com
[02:04:51] 200 -    2KB - /README.md
[02:04:51] 200 -   93B  - /remote/fgt_lang?lang=/../../../../////////////////////////bin/sslvpnd
[02:04:51] 200 -   93B  - /remote/fgt_lang?lang=/../../../..//////////dev/cmdb/sslvpn_websession
[02:04:52] 200 -   47B  - /robots.txt
[02:04:59] 200 -   93B  - /wps/cmis_proxy/http/www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com
[02:04:59] 200 -   93B  - /wps/contenthandler/!ut/p/digest!8skKFbWr_TwcZcvoc9Dn3g/?uri=http://www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com
[02:04:59] 200 -   93B  - /wps/myproxy/http/www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com
[02:04:59] 200 -   93B  - /wps/proxy/http/www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com
[02:04:59] 200 -   93B  - /wps/common_proxy/http/www.redbooks.ibm.com/Redbooks.nsf/RedbookAbstracts/sg247798.html?Logout&RedirectTo=http://example.com

```

ffufでサブドメインを探したが、見つからなかった
```bash
ffuf -w /usr/share/wordlists/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt -u http://greenhorn.htb -H "Host: FUZZ.greenhorn.htb" -mc 200
```

/login.phpで、このサイトが、pluck cms 4.7.18を利用していることがわかる。
- https://github.com/pluck-cms/pluck
![[Pasted image 20241229173129.png]]

- 脆弱性があるのかなと思って調べたが、Pluck CMS 4.7.18の脆弱性はなさそう？
```bash
└──╼ [★]$ searchsploit pluck
------------------------------------------------------------------------------------------------------------------------------------------------ ---------------------
 Exploit Title                                                                                                                                  |  Path
------------------------------------------------------------------------------------------------------------------------------------------------ ---------------------
Pluck CMS 4.5.1 (Windows) - 'blogpost' Local File Inclusion                                                                                     | php/webapps/6074.txt
Pluck CMS 4.5.2 - Multiple Cross-Site Scripting Vulnerabilities                                                                                 | php/webapps/32168.txt
Pluck CMS 4.5.2 - Multiple Local File Inclusions                                                                                                | php/webapps/6300.txt
Pluck CMS 4.5.3 - 'g_pcltar_lib_dir' Local File Inclusion                                                                                       | php/webapps/7153.txt
Pluck CMS 4.5.3 - 'update.php' Remote File Corruption                                                                                           | php/webapps/6492.php
Pluck CMS 4.6.1 - 'module_pages_site.php' Local File Inclusion                                                                                  | php/webapps/8271.php
Pluck CMS 4.6.2 - 'langpref' Local File Inclusion                                                                                               | php/webapps/8715.txt
Pluck CMS 4.6.3 - 'cont1' HTML Injection                                                                                                        | php/webapps/34790.txt
Pluck CMS 4.7 - Directory Traversal                                                                                                             | php/webapps/36986.txt
Pluck CMS 4.7 - HTML Code Injection                                                                                                             | php/webapps/27398.txt
Pluck CMS 4.7 - Multiple Local File Inclusion / File Disclosure Vulnerabilities                                                                 | php/webapps/36129.txt
Pluck CMS 4.7.13 - File Upload Remote Code Execution (Authenticated)                                                                            | php/webapps/49909.py
Pluck CMS 4.7.16 - Remote Code Execution (RCE) (Authenticated)                                                                                  | php/webapps/50826.py
Pluck CMS 4.7.3 - Cross-Site Request Forgery (Add Page)                                                                                         | php/webapps/40566.py
Pluck CMS 4.7.3 - Multiple Vulnerabilities                                                                                                      | php/webapps/38002.txt
Pluck v4.7.18 - Remote Code Execution (RCE)                                                                                                     | php/webapps/51592.py
pluck v4.7.18 - Stored Cross-Site Scripting (XSS)                                                                                               | php/webapps/51420.txt
------------------------------------------------------------------------------------------------------------------------------------------------ ---------------------
Shellcodes: No Results

```


- いや、Pluckは、Pluck CMSを指してるらしい
	- Pluck v4.7.18 - Remote Code Execution (RCE)  を試してみる
 ![[Pasted image 20241229180356.png]]

PoCをミラーダウンロードする
```bash
searchsploit -m php/webapps/51592.py
```

コードの調整が必要な部分を調整する
```bash

```
- 
- 
- 
- **Tactics**:
    - #Tactic_情報収集
    - #Tactic_探索
- **Techniques**:
    - #T1016_システムネットワーク構成の探索
    - #T1046_ネットワークサービススキャン
    - #T1057_プロセス探索`
    - #T1018_リモートシステム探索`
    - その他のDiscovery関連技術...



---

# Foothold
<最初の侵入ポイントをここに書いてください>
```bash

```

```bash

```

```bash

```

```bash

```

```bash

```


- **Tactics**:
    - #Tactic_初期アクセス
    - #Tactic_Escution_実行
- **Techniques**:
    - #T1190_公開アプリケーションのエクスプロイト
    - #T1059_コマンドとスクリプトインタープリタ
    - #T1078_有効なアカウント
    - その他のInitial Access/Execution関連技術...



---

# Lateral Movement
<横方向の動きに関する説明をここに書いてください>
```bash

```

```bash

```

```bash

```

```bash

```

```bash

```



- **Tactics**:
    - #Tactic_横移動
- **Techniques**:
    - #T1021_リモートサービス
    - #T1078_有効なアカウント




---

# Privilege Escalation
<特権昇格の詳細をここに記載してください>
```bash

```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```

```bash

```



- **Tactics**:
    - #Tactic_特権昇格
- **Techniques**:
    - #T1068_特権昇格のためのエクスプロイト
    - #T1055_プロセス注入
    - #T1053_スケジュールされたタスク/ジョブ
    - その他のPrivilege Escalation関連技術...



---

## Notes

- **Tactics**:
    - #Tactic_永続化
    - #Tactic_防御回避
- **Techniques**:
    - #T1098_アカウント操作
    - #T1553_信頼制御の転覆
    - #T1070_ホスト上の痕跡削除
    - その他のPersistence/Defense Evasion関連技術...

<このWriteupで特に重要な点や学んだことを追加で記載するセクション>

---
## Flags

- **User**: `<md5>`
- **Root**: `<md5>`
---

### ポイント


- 簡単なポイントあったら