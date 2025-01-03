
class ConsumerResponse(dict):
    def __init__(self, data: dict, status: str = 'success', message: str = 'perform success'):
        super().__init__(data=data, status=status, message=message)