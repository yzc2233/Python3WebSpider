@rem 跳转到bat文件目录
cd /d %~dp0
@rem 个人安装了conda，activate mypython36进入Python3环境，可删除
call activate mypython36
@rem 执行SwaggerCompare.py，默认对比所有Services
python SwaggerCompare.py stage 0
pause