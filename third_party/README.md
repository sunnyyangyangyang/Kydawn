# third_party
#
# 本地构建依赖放在这里。WebPSharp.0.5.1.nupkg 不再提交进仓库,
# 它随其它构建工具一起存放在本仓库的 build-tools release 里。
# 本地构建前, 从 build-tools release 下载 WebPSharp.0.5.1.nupkg 放到本目录:
#   curl -L -o WebPSharp.0.5.1.nupkg https://github.com/sunnyyangyangyang/Kydawn/releases/download/build-tools/WebPSharp.0.5.1.nupkg
#
# NuGet.config 里的 MyNuget 源指向本目录 (../third_party)。
