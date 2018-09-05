# todo umstellen auf abstract factory
# https://sourcemaking.com/design_patterns/factory_method
from Utils.Abstract_Factory import Abstract_Factory
import os
from pathlib import Path


class RiskModelFactory(Abstract_Factory):

    def __init__(self):
        path = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(path, './*/**/**/*.py', 'risk')
