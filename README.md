# fiap_tech_challenge_03

WSL

https://docs.localstack.cloud/user-guide/integrations/devcontainers/#vscode

https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04
sudo apt-get install firefox
sudo apt install libffi-dev
sudo ldconfig

https://gist.github.com/trongnghia203/9cc8157acb1a9faad2de95c3175aa875

git clone https://github.com/yyuu/pyenv-virtualenv.git $HOME/.pyenv/plugins/pyenv-virtualenv

pyenv install -l

pyenv install 3.13.0

pyenv virtualenv 3.13.0 venv_3.13.0

pyenv global 3.13.0

pip install --upgrade pip

pip3 install selenium
pip3 install bs4
pip3 install requests
pip3 install pandas
pip3 install lxml
pip3 install boto3
pip3 install awscli
pip3 install fastparquet

https://stackoverflow.com/questions/64086810/navigate-pagination-with-selenium-webdriver
https://stackoverflow.com/questions/63881801/element-is-not-clickable-at-point-because-another-element-obscures-it
https://stackoverflow.com/questions/75688714/python-selenium-how-to-click-element-in-pagination-that-is-not-a-button-a-hr
https://stackoverflow.com/questions/30002313/finding-elements-by-class-name-with-selenium-in-python

aws s3api create-bucket --bucket dados-brutos --endpoint=http://localhost:4566
aws s3 ls --endpoint=http://localhost:4566

aws configure
local | local
us-east-1
json

docker logs -f localstack-main

pip freeze > requirements.txt