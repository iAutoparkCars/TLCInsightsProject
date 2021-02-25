class Format:
    def __init__(self):
        pass

    @staticmethod
    def price(price):
        if price == 0:
            return "no record"
        else:
            return f"${price}"

    @staticmethod
    def minutes(time):
        if time == 0:
            return "no record"
        else:
            return f"{time} minutes"
