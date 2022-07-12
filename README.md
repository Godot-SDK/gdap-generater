# gdap-generater
自动生成.gdap文件，解决依赖地狱，释放双手！

# 如何使用
1. 安装python >=3
2. git clone https://github.com/Godot-SDK/gdap-generater.git
3. 创建一个空工程
```
python init.py 工程名称
```
4. 将不同的文件分类，放到对应的文件夹内，并修改文件夹里的`remotes.json`和`config.json`
5. 使用类似下面的命令生成gdap配置文件
```
python gen.py example/Yomob
```