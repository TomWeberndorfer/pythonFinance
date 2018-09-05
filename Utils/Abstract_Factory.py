from abc import abstractmethod
import os
from pathlib import Path
from Utils.CommonUtils import CommonUtils


class Abstract_Factory:

    @abstractmethod
    def __init__(self, file_path, path_pattern, keyword):
        """
        Init method for all inheritance
        :param file_path: fil path as pathlib Path-type, ex: Path(os.path.dirname(os.path.abspath(__file__)))
        :param path_pattern: string with file pattern, ex: all files of subfolder: './*/**/**/*.py'
        :param keyword: keyword in every file, ex: risk --> for risk models
        """
        self.file_path = file_path
        self.path_pattern = path_pattern
        self.keyword = keyword

    def prepare(self, class_to_create, **kwargs):
        model = self._create(class_to_create, **kwargs)
        return model

    def get_implemented_classes(self):
        classes_dict = CommonUtils.get_implemented_items_dict(self.file_path, self.path_pattern, self.keyword)
        return classes_dict

    def _create(self, class_to_create, **kwargs):
        classes_dict = self.get_implemented_classes()

        if class_to_create in classes_dict:
            # get the class from class dict and create the concrete object then
            class_object = classes_dict[class_to_create]
            risk_model = class_object(**kwargs)
            return risk_model
        else:
            raise NotImplementedError(str(class_to_create) + " is not implemented!")
