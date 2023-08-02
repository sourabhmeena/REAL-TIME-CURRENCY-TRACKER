from utils.currencies import currencies


class ValidCurrency:
    def __init__(self, currency_list) -> None:
        self.currency_list = currency_list

    async def currency_list_handler(self):

        symbols_list = self.currency_list.split(',')
        symbols_list = [item.upper() for item in symbols_list]
        invalid_symbols, valid_symbols = set(), set()

        for val in symbols_list:
            if val not in currencies:
                invalid_symbols.add(val)
            else:
                valid_symbols.add(val)

        invalid_symbols = list(invalid_symbols)
        valid_symbols = list(valid_symbols)

        return {'valid': valid_symbols,
                'invalid': invalid_symbols}
