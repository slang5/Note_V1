from uuid import uuid4
from yfinance import Ticker

type_list = ['EQUITY', 'BOND', 'FUND', 'ETF', 'COMMODITY', 'CURRENCY']
ISIN_length = 12
symbol_max_length = 10
exchange_list = []
exchange_dict = {"XNYS": "New York Stock Exchange",
            "XNAS": "Nasdaq US",
            "XSHG": "Shanghai Stock Exchange",
            "XJPX": "Japan Exchange Group",
            "XHKG": "Hong Kong Stock Exchange",
            "XAMS": "Euronext Amsterdam",
            "XBRU": "Euronext Brussels",
            "XMSM": "Euronext Dublin",
            "XLIS": "Euronext Lisbon",
            "XMIL": "Euronext Milan",
            "XOSL": "Euronext Oslo",
            "XPAR": "Euronext Paris",}

class Underlying:
    def __init__(self, name: str, symbol: str, exchange: str, isin: str, type: str, description = None,id = None):
        
        if len(symbol) > symbol_max_length:
            raise ValueError(f"Symbol must be at most {symbol_max_length} characters long.")
        
        if len(isin) != ISIN_length:
            raise ValueError(f"ISIN must be {ISIN_length} characters long.")

        if type not in type_list:
            raise ValueError(f"Type '{type}' is not valid. Must be one of {type_list}.")
        
        if exchange not in exchange_dict.keys():
            raise ValueError(f"Exchange '{exchange}' is not recognized. Must be one of {list(exchange_dict.keys())}.")
        
        self.name = name.upper()
        self.symbol = symbol.upper()
        self.exchange = exchange.upper()
        self.type = type.upper()
        self.isin = isin.upper()
        self.description = Ticker(self.isin).info.get('longBusinessSummary', '') if description is None else description
        self.id = id if id is not None else str(uuid4())

    def get_info(self) -> str:
        return f"{self.name} ({self.symbol}) listed on {self.exchange} in the {self.type} market with ISIN {self.isin}."
    
    def __repr__(self) -> str:
        return f"Underlying(name={self.name}, symbol={self.symbol}, exchange={self.exchange}, isin={self.isin}, type={self.type}, id={self.id}, description={self.description})"
    
    def __dict__(self) -> dict:
        return {
            'name': self.name,
            'symbol': self.symbol,
            'exchange': self.exchange,
            'isin': self.isin,
            'type': self.type,
            'description': self.description,
            'id': self.id
        }
    
    