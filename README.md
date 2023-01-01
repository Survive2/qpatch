# qpatch
A really convenient tool to patch an elf。
qpatch使用起来非常方便，他会自动探测你已经有点libc，并以列表的形式输出，你仅仅输入想要的版本的序号，即可完成patch，可以省去你一个一个输入名字的过程。
## 前言

该工具是我自用的一个小工具（针对于做pwn题的辅助工具）（本工具的实现非常简单，而且这个工具的核心是依赖patchelf和glibc-all-in-one这两个工具），用于快速修改本地`ELF`文件的libc使其与远程服务器那边所运行的程序依赖的`libc`库一样
从而避免了因为 `libc` 问题，而导致本地打通了但是远程没打通的尴尬情况。因为每次都手动 `patch libc` 的过程太过于重复，并且文件夹名字太长，手动patch的过程太过于繁琐。

## Deploy

由于这个小工具依赖的核心依然是 `patchelf` 和 `glibc-all-in-one` ，能让它以命令行工具的身份出现，还少不了python中的 `click` 模块。
因此你应该有如下东西 `patchelf`   `glibc-all-in-one` ，如果有的话请直接看下面的 [install patchup](#install-patchup) 部分，如果没有的话下文就是相关部署。

### install patchelf

#### 直接使用预编译的二进制文件

```bash
wget https://github.com/NixOS/patchelf/releases/download/0.14.5/patchelf-0.14.5-x86_64.tar.gz
tar -xzvf patchelf-0.14.5-x86_64.tar.gz
cd bin
sudo mv patchelf /bin/patchelf
```

#### 手动编译 patchelf

```bash
git clone https://github.com/NixOS/patchelf

cd patchelf
# 安装autoreconf
sudo apt install -y autoconf
# 赋予执行权限
chmod +x bootstrap.sh
# 使用预设脚本配置编译环境
./bootstrap.sh
./configure
make
make check
sudo make install
```



### install glibc-all-in-one

```bash
git clone https://github.com/matrix1001/glibc-all-in-one
cd glibc-all-in-one
mkdir libs
chmod +x  extract  update_list download
./update_list
```

cd 到上级目录

## install patchup
ok，假设你现在有了 `patchelf` 和 `glibc-all-in-one`  那么你就可以输入以下命令来安装 `qpatch` 这个小工具了 
```bash
git clone https://github.com/p](https://github.com/Survive2/qpatch.git

cd qpatch/qpatch

sudo pip install --editable .

```

可以输入qpatch --help命令查看帮助，并进行使用。
