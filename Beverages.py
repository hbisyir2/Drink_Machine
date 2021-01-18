



class Beverage():
    def __init__(self, alcoholic, proof=0):
        logger.debug('Beverage: __init__')
        self.is_alcohol = alcoholic
        self.proof = proof