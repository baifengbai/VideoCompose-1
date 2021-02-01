# VideoCompose
------

### Description

```python
"""
@Author: WSWSCSJ
@Description: 传入指定数量图片集和背景音乐,根据参数实现指定转场的商品静态短视频
@Project: Demo Backend
"""
```

+ TestCase
  + multi_post(多线程简单请求测试)
+ ByDjango(使用Django RESTful framework实现)
+ ByTornado(使用Tornado 单进程实现)
+ compose (服务端视频处理模块)
  + process (合成主逻辑)
  + handler (处理request)
  + render (转成特效)
  + video/audio/picture (图片和音频合成子模块)
+ nginx.conf(负载均衡configure)

### Install FFmpeg on Docker/Linux

```shell
docker pull centos
docker run -itd -p 7777:8080 --name video_compose centos
>>> abc1234
docker exec -it abc123 /bin/bash
# 进入abc123容器中
cd /root/
mkdir Downloads
cd /
mkdir ffmpeg
exit
# MacOS 下载FFmpeg压缩包 至/Users/xxx/Downloads
# 复制到abc123容器内/root/Downloads目录下
docker cp /Users/xxx/Downloads/FFmpeg-n4.1.4.tar abc123:/root/Downloads/
docker exec -it abc123 /bin/bash
# 安装gcc,gcc++,cmp,yasm等依赖
yum install gcc
yum install gcc automake autoconf libtool make
yum install gcc gcc-c++ kernel-devel
yum install gcc-gfortran
yum install gcc gcc-c++
yum install diffutils
cd /root/Downloads
curl http://www.tortall.net/projects/yasm/releases/yasm-1.2.0.tar.gz >yasm.tar.gz
tar xzvf yasm.tar.gz
cd yasm-1.2.0
./configure
make
make install
# 解压FFmpeg和安装
cd ..
tar xvf FFmpeg-n4.1.4.tar
move FFmpeg-4.1.4 /ffmpeg
cd /ffmpeg
./configure
make
make install 
ffmpeg
>>>
ffmpeg version 4.1.4 Copyright (c) 2000-2019 the FFmpeg developers
  built with gcc 8 (GCC)
  configuration:
  libavutil      56. 22.100 / 56. 22.100
  libavcodec     58. 35.100 / 58. 35.100
  libavformat    58. 20.100 / 58. 20.100
  libavdevice    58.  5.100 / 58.  5.100
  libavfilter     7. 40.101 /  7. 40.101
  libswscale      5.  3.100 /  5.  3.100
  libswresample   3.  3.100 /  3.  3.100
```
