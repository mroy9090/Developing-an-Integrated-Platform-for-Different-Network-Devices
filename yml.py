import yaml
import ipaddress
from pprint import pprint


def show_spud(filename="ipaddress.yml"):
    with open('ipaddress.yml') as file:
        result = yaml.safe_load(file)
        # pprint(result,indent=2,sort_dicts=False)
        print(result)



