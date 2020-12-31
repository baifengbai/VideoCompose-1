# VideoCompose
------

### 2020.12.31 Update

```python
"""
Test
centos使用docker开启4个容器单独在容器中编译ffmpeg,配合nginx负载均衡;
多线程4n请求时,在单独容器中tail可以看出ffmpeg可以同时处理视频,但是处理速度下降明显,处理过程中CPU100%,内存100%;
部分worker出现cannot allocate memory无法申请内存,返回release fail异常;
受限于服务器计算性能,每个请求的响应时长都几乎一致,如果是单个worker,每个请求的响应时长按照前后顺序几乎等差数列;
优化:本地使用windows+i7-CPU+多docker提高响应速度和并发量
"""
```

### Description

```python
"""
@Author: WSWSCSJ
@Description: 传入指定数量图片集和背景音乐,根据参数实现指定转场的商品静态短视频
@Project: Demo Backend
@Summary: 单个请求的情况两个框架的响应无差别,大部分时间都是消耗在服务端ffmpeg生成和合并上,多并发情况下log中可以看出Tornado响应较快
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
