from abc import abstractmethod


class Abstract_DataContainerDecorator:

    def __init__(self, shaped_data_container):
        self.shaped_data_container = shaped_data_container

    @abstractmethod
    def get_names_and_values(self):
        self.shaped_data_container.get_names_and_values()
