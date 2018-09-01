class ObjectWithChangedListeners:
    def __init__(self, default_value=""):
        """
        Init the list with event listeners.
        """
        self._default_value = default_value
        self._object = default_value
        self._event_listeners = []

    def set(self, value):
        self._object = value
        self._data_changed()

    def clear(self):
        """
        Clears the variable with the implemented clear value or set the default value.
        :return:
        """
        if isinstance(self._object, dict) or isinstance(self._object, list):
            self._object.clear()
        else:
            self._object = self._default_value

        self._data_changed()

    def get(self):
        return self._object

    def add_event_listeners(self, listener_method):
        self._event_listeners.append(listener_method)

    def _data_changed(self):
        for event_listener_method in self._event_listeners:
            event_listener_method()  # execute the method


class ListWithChangedListeners(ObjectWithChangedListeners):
    def __init__(self):
        """
        Init the list with event listeners.
        """
        # the "[]" indicates python to create a list
        super().__init__([])

    def append(self, value):
        self._object.append(value)
        self._data_changed()

    def extend(self, another_list):
        self._object.extend(another_list)
        self._data_changed()


class DictWithChangedListeners(ObjectWithChangedListeners):
    def __init__(self):
        """
        Init the dict with event listeners.
        """
        # the "{}" indicates python to create a dict
        super().__init__({})

    def update(self, another_items_dict):
        """
        Update the given dict with a values of another dict instance and calls the data changed method.
        :param another_items_dict: dict instance with keys and values to insert into the list
        :return: -
        """
        assert (isinstance(another_items_dict, dict))
        for key, value in another_items_dict.items():
            self._object.update({key: value})
        self._data_changed()
