from sys import path
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path.insert(0, str(ROOT))

from typing import Literal
from datetime import date

from Underlying_V1.underlying_class import Underlying
from Underlying_V1.database import Database

rounding_precision = 5

class Option:
    def __init__(self, start_date, end_date, option_type, strike_price, strike_method):

        if option_type not in ['EU', 'US']:
            raise ValueError("option_type must be either 'EU' or 'US'")
        if start_date >= end_date:
            raise ValueError("start_date must be earlier than end_date") # no intraday options
        if strike_price <= 0:
            raise ValueError("strike_price must be positive") # no null or negative strike price
        if strike_method not in ['absolute', 'relative']:
            raise ValueError("strike_method must be either 'absolute' or 'relative'")

        self.start_date:date = start_date
        self.end_date:date = end_date
        self.maturity_days:int = (end_date - start_date).days
        self.strike_price:float = round(strike_price, rounding_precision)
        self.strike_method: Literal['absolute', 'relative'] = strike_method
        self.option_type: Literal['EU', 'US'] = option_type

    def __repr__(self):
        return (f"Option(type={self.option_type}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"strike_price={self.strike_price})")
    
class Option_Call(Option):
    def __init__(self, start_date, end_date, option_type, strike_price, strike_method, underlyings, basket_method, rebate=0.0):
        super().__init__(start_date, end_date, option_type, strike_price, strike_method)
        self.basket_method: Literal['uniform', 'worst-of', 'best-of'] = basket_method
        self.underlyings:list[Underlying] = underlyings
        self.rebate: float = rebate
    
    def __repr__(self):
        return (f"Option_Call(type={self.option_type}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"strike_price={self.strike_price}, "
                f"basket_method={self.basket_method}, "
                f"underlyings={self.underlyings}), "
                f"rebate={self.rebate})")
    
class Option_Put(Option):
    def __init__(self, start_date, end_date, option_type, strike_price, strike_method, underlyings, basket_method, rebate=0.0):
        super().__init__(start_date, end_date, option_type, strike_price, strike_method)
        self.basket_method: Literal['uniform', 'worst-of', 'best-of'] = basket_method
        self.underlyings:list[Underlying] = underlyings
        self.rebate: float = rebate
    
    def __repr__(self):
        return (f"Option_Put(type={self.option_type}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"strike_price={self.strike_price}, "
                f"basket_method={self.basket_method}, "
                f"underlyings={self.underlyings}), "
                f"rebate={self.rebate})")
    