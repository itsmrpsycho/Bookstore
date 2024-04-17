@echo off


:start
cls

set python_ver=39

python ./get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install mysql-connector-python
pip install prettytable
pip install validate_email

pause
exit