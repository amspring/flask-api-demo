#!/bin/bash
if [ -f config.yml ]; then
  pass
else
  cp "config/config.example.yml" config.yml
fi

echo "install requirements"
/opt/python3.10/bin/python -m pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

echo "copy *.ini to /opt/conf/supervisord.d"
cp "config/*.ini" /opt/conf/supervisord.d

echo "reload service"
supervisorctl reload

echo "Install Success!"