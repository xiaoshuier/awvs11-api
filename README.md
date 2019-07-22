linux学习笔记

（1）对于适应ctrl z命令将进程放到后台，，可以使用 jobs命令查看，然后使用bg <job id>的放到后台运行，，使用fg <job id>的方式放到前台运行
  
（2）显示某个目录或文件的大小：
#du -sh xxx  显示总目录的大小，但是不会列出目录中的每一个文件
#du -sh xxx/*  列出xxx下每个目录和文件所占的容量
Linux 查找占用空间最大的文件与目录：du -h --max-depth=1

#df -h 查看目前在Linux系统上的文件系统的磁盘使用情况统计

（3）常用快捷键
<p>javascript:# Ctrl + l - 清屏</p>
# Ctrl + a - 光标移到行首
# Ctrl + e - 光标移到行尾"><div title="\"2356<svg>"></div>
# Ctrl + w - 清除光标之前一个单词
# Ctrl + k - 清除光标到行尾的字符
# Ctrl + t - 交换光标前两个字符
# Ctrl + v - 输入控制字符 如Ctrl+v ,会输入^M
# Ctrl + f - 光标后移一个字符
# Ctrl + b - 光标前移一个字符
# Ctrl + h - 删除光标前一个字符
# Alt + u  把当前词转化为大写
# Alt + l  把当前词转化为小写
# Alt + c  把当前词汇变成首字符大写
#ctrl s 停止终端输入。使用ctrl q 恢复输入
#Ctrl + c 中止当前正在执行的程序。
#Ctrl + d 相当于exit命令，退出当前会话。

(4)添加用户 
#useradd xxx
#passwd xxx 修改用户的密码

（5） tar命令
z代表gz，j代表bx2，J代表xz
tar -zxvf xx。解压xx
tar -zcvf xx.gz	 压缩xx
（6）corn
分钟 时 日 月 周 【用户名】命令
*/15 12 1 8 * echo "niubi"  #表示 在8月1日中午12点，每隔15分钟，会执行命令echo “niubi”
*   代表任意时间
，   2，3代表2和3都行
-    2-3 表示2到3
*/n  没隔n执行一次
crontab -u //设定某个用户的cron服务
crontab -l //列出某个用户cron服务的详细内容
crontab -r //删除没个用户的cron服务
crontab -e //编辑某个用户的cron服务
(7)软件安装 
rpm -ivh xxx.rpm
dpkg -i xxx.deb

卸载 
rpm -e  python 
dpkg -e python
  
