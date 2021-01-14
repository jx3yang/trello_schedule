import yaml
from trello_api import *
from data_models import *
from parsing import *

def main():
    print(parse_courses_file('courses.yaml'))

if __name__ == '__main__':
    main()
