import os
from pathlib import Path
from Utils.Abstract_Factory import Abstract_Factory


class BacktestingFactory(Abstract_Factory):

    def __init__(self):
        path = Path(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(path, './*/**/**/*.py', 'back')
