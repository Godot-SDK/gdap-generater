import sys
import os
import json

rootDir = sys.argv[1]

os.mkdir(rootDir)
os.mkdir(rootDir + "/dependencies")
os.mkdir(rootDir + "/dependencies/local")
os.mkdir(rootDir + "/dependencies/remote")
os.mkdir(rootDir + "/plugin")

RemoteConfigFile = open(rootDir + "/dependencies/remote/remotes.json","w",encoding="utf-8")
remote_data = {"custom_maven_repos":[],"remotes":[]}
json_str = json.dumps(remote_data,indent=4)
RemoteConfigFile.write(json_str)
RemoteConfigFile.close()

PluginConfigFile = open(rootDir + "/plugin/config.json","w",encoding="utf-8")
config_data = {"name":""}
json_str = json.dumps(config_data,indent=4)
PluginConfigFile.write(json_str)
PluginConfigFile.close()
print("空工程已配置完成！")
