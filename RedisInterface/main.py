import requests
import yaml

with open('../config.yaml', 'r') as config:
    data = yaml.safe_load(config)

print("Host:", data['redis']['host'])