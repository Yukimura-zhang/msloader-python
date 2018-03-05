基本依赖：
确保系统已安装python3.6,下文中我们将简称python3；
确保系统已安装gcc-4.8.5（或以上更高版本gcc）

1.安装C库librtmp
tar xzvf rtmpdump-2.3.tgz
cd rtmpdump-2.3
make
make install			#使用超级用户权限来安装，在centos中本库的默认安装路径为/use/local/lib
ldconfig

2.安装requests包
tar xzvf kennethreitz-requests-v2.8.1-45-g2128321.tar.gz
cd kennethreitz-requests-2128321
python3 setup.py install

3.安装python-librtmp包
tar xzvf python-librtmp.tar.gz
cd python-librtmp
python3 setup.py install




