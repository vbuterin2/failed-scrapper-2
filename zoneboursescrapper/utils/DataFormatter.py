class DataFormatter:
    @staticmethod
    def format(data_dict) -> {}:
        return data_dict

    @staticmethod
    def get_text(element, error='-'):
        try:
            return element.text
        except:
            return error
