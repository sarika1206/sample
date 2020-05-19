### aws-tool
##This is for sample aws-tool with python
#create a venv 
pip install virtualenv
virtualvenv %name of the enviornment%
#Activate the enviornment
source %name of the enviornment%/bin/activate
#install requirements.txt
pip install requirement.txt
# configure aws credentials
aws configure  (provide the secret key and access key)
# Set PYTHONPATH
export PYTHONPATH=%pythonpath%
# now run the aws-tool.py file
run aws-tool.py -h (it will print the help, where you can check all other options to be run)
