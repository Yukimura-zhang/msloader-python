## 安装

- 在python3.6下完成测试，请安装好python3.6的解释器；
- 使用需要依赖第三方python包Requests，python-librtmp,以及C库librtmp，依赖项放在了3rdparty目录中,请提前安装；

## 运行说明
- 请在__main__.py同级目录下运行程序，运行需读取同级config目录中的配置文件；
- 程序不支持运行中动态配置，请在config/msloader.xml中提前写好拉流配置；
- 目前支持测试rtmp直播，http-flv直播，hls直播，高码时移回看，mp4vod点播，默认测试时间600s可配置；