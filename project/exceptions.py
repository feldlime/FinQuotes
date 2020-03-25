class GettingQuoteError(Exception):
    pass


class TickerNotFoundError(GettingQuoteError):
    pass


class PriceNotFoundError(GettingQuoteError):
    pass
