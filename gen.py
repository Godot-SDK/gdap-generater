import os
import os.path
import shutil
import json
import sys

localDependencies = []
remoteDependencies = []
def makeOutPutDir():
    os.mkdir(output)
    pass

#把aar插件本地复制过去
def copyLocalPlugin():
    workdir = "example/口袋工厂(旧版)/plugin"
    targetdir = "example/口袋工厂(旧版)/output"
    files = os.listdir(workdir)
    #这里需要重构
    for file in files:
        if file.endswith(".aar") or file.endswith(".jar"):
            srcFile = os.path.join(workdir,file)
            targetFile = os.path.join(targetdir,file)
            shutil.copyfile(srcFile,targetFile)
    print("任务：copyLocalPlugin：复制本地插件aar完成")
    pass

#把aar插件的本地依赖复制过去
def copyLocalDep():
    workdir = "example/口袋工厂(旧版)/dependencies/local"
    targetdir = "example/口袋工厂(旧版)/output"
    files = os.listdir(workdir)

    for file in files:
        if file.endswith(".aar") or file.endswith(".jar"):
            localDependencies.append(file)
            srcFile = os.path.join(workdir,file)
            targetFile = os.path.join(targetdir,file)
            shutil.copyfile(srcFile,targetFile)
    #print(localDependencies)
    print("任务：copyLocalDep：复制本地依赖aar完成")
    pass

def genGdap():
    #gdap[config行]
    config_name = ""
    binary_type = "local"
    binary = "PocketPlugin.aar"
    def readPluginConfig():
        with open("example/口袋工厂(旧版)/plugin/config.json") as f:
            data = json.load(f)
            #print(data)
            return data['name']
    def readRemoteDependencies():
        targetdir = "example/口袋工厂(旧版)/dependencies/remote/remotes.json"
        file = open(targetdir,encoding="utf-8")
        data = json.load(file)
        deps = data["remotes"]
        file.close()
        return deps
        pass

    def writePluginConfig():
        targetdir = "example/口袋工厂(旧版)/output/test.gdap"
        file = open(targetdir,"a+",encoding="utf-8")
        file.write("[config]\n")
        file.write("name="+ '"' + config_name +'"' + "\n")
        file.write('binary_type="local"\n')
        file.write('binary=' + '"' + binary + '"' +"\n")
        file.write("\n")
        file.close()

    def writeLocalDependencies():
        targetdir = "example/口袋工厂(旧版)/output/test.gdap"
        file = open(targetdir,"a+",encoding="utf-8")
        file.write("[dependencies]\n")
        file.write('custom_maven_repos=["https://jitpack.io"]\n')
        localLine = "local=["
        for f in localDependencies:
            #print("找到本地依赖：",f)
            localLine += '"'
            localLine += f
            localLine += '"'
            localLine += ","
            #print(localLine)
        #清除末尾的，
        result = localLine.rstrip(",")
        result += "]\n"
        file.write(result)
        file.write("\n")
        file.close()

    def writeRemoteDependencies():
        targetdir = "example/口袋工厂(旧版)/output/test.gdap"
        file = open(targetdir,"a+",encoding="utf-8")
        file.write('custom_maven_repos:["https://jitpack.io"]\n')
        remoteLine = "remote=["
        for f in remoteDependencies:
            remoteLine += '"'
            remoteLine += f
            remoteLine += '"'
            remoteLine += ","
        result = remoteLine.rstrip(",")
        result += "]"
        file.write(result)
        file.close()

    config_name = readPluginConfig()
    remoteDependencies = readRemoteDependencies()
    writePluginConfig()
    writeLocalDependencies()
    writeRemoteDependencies()
    print("任务：genGdap 已完成")
    pass

def clean():
    dirname = "example/口袋工厂(旧版)/output"
    shutil.rmtree(dirname,onerror=rmtreeError)
    print("任务：clean：已完成")
    pass

def rmtreeError(function, path, excinfo):
    print("错误！：output文件夹不存在: ", path)
    #print("Error at shutil.rmtree function call")
    function(path)
    pass
#main
#print(sys.argv)
#print(len(sys.argv))
if len(sys.argv) == 1:
    output = "example/口袋工厂(旧版)/output"
    if not os.path.exists(output):
        makeOutPutDir()
    else:
        os.remove(output+"/test.gdap")
    copyLocalPlugin()
    copyLocalDep()
    genGdap()
if len(sys.argv) == 2:
    if sys.argv[1] == "clean":
        clean()