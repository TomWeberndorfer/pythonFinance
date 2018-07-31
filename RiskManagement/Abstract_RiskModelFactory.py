from abc import abstractmethod


class Abstract_RiskModelFactory:
    def prepare(self, model_to_create, stock_data_container_list, parameter_dict):
        model = self._create_risk_model(model_to_create, stock_data_container_list, parameter_dict)
        # TODO checken ob des e ned vl so ghert:
        # result = model.read_data()
        return model

    @abstractmethod
    def _create_risk_model(self, model_to_create, stock_data_container_list, parameter_dict):
        raise Exception("Abstractmethod")
