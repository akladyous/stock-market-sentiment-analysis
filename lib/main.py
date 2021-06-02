import sys
import os

if os.path.basename(os.getcwd()) == 'capstone':
    sys.path.insert(1, os.getcwd() + '/lib/')


class Main(object):
    def __init__(self, modules):
        self._path = os.getcwd() + '/lib/'
        self.project_name = "Stock Market Sentiment Analysis"
        self.modules = modules
        sys.path.insert(1, self._path)

    def project_dir(self, folders):
        for folder in folders:
            folder = self._path + folder + '/'
            if not os.path.exists(folder):
                os.makedirs((folder))
    
# project = Main(['newsapi', 'finnhub'])
# project.project_dir(project.modules)
