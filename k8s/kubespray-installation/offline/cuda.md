##### 安装显卡驱动
1. 禁用nouveau第三方驱动
```
sudo vim /etc/modprobe.d/blacklist-nouveau.conf
    blacklist nouveau
    options nouveau modeset=0
sudo update-initramfs -u
sudo reboot
sudo systemctl stop lightdm.service
```

2. 安装驱动
```
sudo ./cuda/NVIDIA-Linux-x86_64-384.59.run --no-opengl-files --disable-nouveau
```

3. 如果出现执行nvidia-smi速度特别慢的情况，执行以下命令
```
sudo nvidia-persistenced --persistence-mode
```

##### 安装cuda(非必需)
```
# 选择不安装显卡驱动
sudo ./cuda/cuda_9.1.85_387.26_linux.run
# 出现缺少相关库的情况
sudo apt-get install freeglut3-dev build-essential libx11-dev libxmu-dev libxi-dev libgl1-mesa-glx libglu1-mesa libglu1-mesa-dev

# 配置环境变量
sudo cat >> /etc/profile << EOF
export PATH=/usr/local/cuda-9.1/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-9.1/lib64:$LD_LIBRARY_PATH
EOF

# 配置cudnn
tar -xzvf ./cuda/cudnn-9.1-linux-x64-v7.tgz
sudo cp cuda/include/cudnn.h /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
```
