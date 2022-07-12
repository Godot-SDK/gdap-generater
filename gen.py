import os
import os.path
import shutil
import json
import sys

localDependencies = []
remoteDependencies = []
pluginDir = "/plugin"
localDepDir = "/dependencies/local"
remoteDepDir = "/dependencies/remote"
outPutDir = "/output"

def makeOutPutDir():
    os.mkdir(output)
    pass

#把aar插件本地复制过去
def copyLocalPlugin(path):
    workdir = path + pluginDir
    targetdir = path + outPutDir
    files = os.listdir(workdir)

    for file in files:
        if file.endswith(".aar") or file.endswith(".jar"):
            srcFile = os.path.join(workdir,file)
            targetFile = os.path.join(targetdir,file)
            shutil.copyfile(srcFile,targetFile)
    print("任务：copyLocalPlugin：复制本地插件aar完成")
    pass

#把aar插件的本地依赖复制过去
def copyLocalDep(path):
    workdir = path + localDepDir
    targetdir = path + outPutDir
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

def genGdap(path):
    #gdap[config行]
    config_name = ""
    binary_type = "local"
    binary = "PocketPlugin.aar"
    custom_maven_repos = []
    def readPluginConfig():
        with open(path + pluginDir + "/config.json") as f:
            data = json.load(f)
            #print(data)
            return data['name']

    def readCustomMavenRepos():
        targetdir = path + remoteDepDir + "/remotes.json"
        file = open(targetdir,encoding="utf-8")
        data = json.load(file)
        file.close()
        #print("custom maven ",data)
        mavens = data["custom_maven_repos"]
        return mavens

    def readRemoteDependencies():
        targetdir = path + remoteDepDir + "/remotes.json"
        file = open(targetdir,encoding="utf-8")
        data = json.load(file)
        deps = data["remotes"]
        file.close()
        return deps
        pass

    def writePluginConfig():
        targetdir = path + outPutDir + "/test.gdap"
        file = open(targetdir,"a+",encoding="utf-8")
        file.write("[config]\n")
        file.write("name="+ '"' + config_name +'"' + "\n")
        file.write('binary_type="local"\n')
        file.write('binary=' + '"' + binary + '"' +"\n")
        file.write("\n")
        file.close()

    def writeLocalDependencies():
        targetdir = path + outPutDir + "/test.gdap"
        file = open(targetdir,"a+",encoding="utf-8")
        file.write("[dependencies]\n")
        #开始写自定义maven仓库数组
        if len(custom_maven_repos) != 0:
            #print(custom_maven_repos)
            maven = "custom_maven_repos=["
            for item in custom_maven_repos:
                maven += '"'
                maven += item
                maven += '"'
                maven += ","
            maven_result = maven.rstrip(",")
            maven_result += "]\n"
            file.write(maven_result)
        #开始写本地依赖数组
        localLine = "local=["
        for f in localDependencies:
            #print("找到本地依赖：",f)
            localLine += '"'
            localLine += f
            localLine += '"'
            localLine += ","
            #print(localLine)
        result = localLine.rstrip(",")
        result += "]\n"
        file.write(result)
        file.close()

    def writeRemoteDependencies():
        targetdir = path + outPutDir + "/test.gdap"
        file = open(targetdir,"a+",encoding="utf-8")
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
    custom_maven_repos = readCustomMavenRepos()
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

if len(sys.argv) == 2:
    #这个我就不修复了，暂时有问题，勿用！请手动删除output文件夹！
    if sys.argv[1] == "clean":
        clean()
    else:
        sys_path = sys.argv[1]
        output = sys.argv[1] + "/output"
        if not os.path.exists(output):
            makeOutPutDir()
        else:
            os.remove(output+"/test.gdap")
        copyLocalPlugin(sys_path)
        copyLocalDep(sys_path)
        genGdap(sys_path)