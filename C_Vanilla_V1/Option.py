from sys import path
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path.insert(0, str(ROOT))

from typing import Literal, Union
from datetime import date

from A_Underlying_V1.underlying_class import Underlying

rounding_precision = 5

class Option:
    def __init__(self, start_date: date, end_date: date, option_type: Literal['EU', 'US'], strike_price: float, value_method: Literal['absolute', 'relative'], underlyings: list[Underlying], basket_method: Literal['uniform', 'worst-of', 'best-of']):
        
        if start_date >= end_date:
            raise ValueError("start_date must be earlier than end_date") # no intraday options
        
        if strike_price <= 0:
            raise ValueError("strike_price must be positive") # no null or negative strike price
        
        self.start_date:date = start_date
        self.end_date:date = end_date
        self.maturity_days:int = (end_date - start_date).days
        self.strike_price:float = round(strike_price, rounding_precision)
        self.value_method: Literal['absolute', 'relative'] = value_method
        self.option_type: Literal['EU', 'US'] = option_type
        self.underlyings:list[Underlying] = underlyings
        self.basket_method: Literal['uniform', 'worst-of', 'best-of'] = basket_method

    def __repr__(self):
        return (f"Option(type={self.option_type}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"strike_price={self.strike_price}), "
                f"value_method={self.value_method}, "
                f"basket_method={self.basket_method}, "
                f"underlyings={self.underlyings}) "
                f"basket_method={self.basket_method}) ")
    
class Option_Call(Option):
    def __init__(self, start_date, end_date, option_type, strike_price, value_method, underlyings, basket_method, rebate=0.0, levier=1.0):
        super().__init__(start_date, end_date, option_type, strike_price, value_method, underlyings, basket_method)
        self.rebate: float = rebate
        self.levier: float = levier
    
    def __repr__(self):
        return (f"Option_Call(type={self.option_type}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"strike_price={self.strike_price}), "
                f"value_method={self.value_method}, "
                f"basket_method={self.basket_method}, "
                f"underlyings={self.underlyings}) "
                f"basket_method={self.basket_method}) ",
                f"rebate={self.rebate})",
                f"levier={self.levier})",
        )
    
class Option_Put(Option):
    def __init__(self, start_date, end_date, option_type, strike_price, value_method, underlyings, basket_method, rebate=0.0, levier=1.0):
        super().__init__(start_date, end_date, option_type, strike_price, value_method, underlyings, basket_method)
        self.rebate: float = rebate
        self.levier: float = levier
    
    def __repr__(self):
        return (f"Option_Put(type={self.option_type}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"strike_price={self.strike_price}), "
                f"value_method={self.value_method}, "
                f"basket_method={self.basket_method}, "
                f"underlyings={self.underlyings}) "
                f"basket_method={self.basket_method}) ",
                f"rebate={self.rebate})",
                f"levier={self.levier})",
        )
    

class Digital_Option(Option):
    def __init__(self, start_date, end_date, option_type, strike_price, value_method, underlyings, basket_method, payout=0.0, rebate=0.0):
        super().__init__(start_date, end_date, option_type, strike_price, value_method, underlyings, basket_method)
        self.payout: float = payout
        self.rebate: float = rebate
    
    def __repr__(self):
        return (f"Digital_Option(type={self.option_type}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"strike_price={self.strike_price}), "
                f"value_method={self.value_method}, "
                f"basket_method={self.basket_method}, "
                f"underlyings={self.underlyings}) "
                f"basket_method={self.basket_method}) ",
                f"rebate={self.rebate}) ",
                f"payout={self.payout})")
    
class Digital_Call(Digital_Option):
    def __init__(self, start_date, end_date, option_type, strike_price, value_method, underlyings, basket_method, payout=0.0, rebate=0.0):
        super().__init__(start_date, end_date, option_type, strike_price, value_method, underlyings, basket_method, payout, rebate)
    
    def __repr__(self):
        return (f"Digital_Call(type={self.option_type}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"strike_price={self.strike_price}), "
                f"value_method={self.value_method}, "
                f"basket_method={self.basket_method}, "
                f"underlyings={self.underlyings}) "
                f"basket_method={self.basket_method}) ",
                f"rebate={self.rebate}) ",
                f"payout={self.payout})")
    
class Digital_Put(Digital_Option):
    def __init__(self, start_date, end_date, option_type, strike_price, value_method, underlyings, basket_method, payout=0.0, rebate=0.0):
        super().__init__(start_date, end_date, option_type, strike_price, value_method, underlyings, basket_method, payout, rebate)
    def __repr__(self):
        return (f"Digital_Put(type={self.option_type}, "
                f"start_date={self.start_date}, "
                f"end_date={self.end_date}, "
                f"strike_price={self.strike_price}), "
                f"value_method={self.value_method}, "
                f"basket_method={self.basket_method}, "
                f"underlyings={self.underlyings}) "
                f"basket_method={self.basket_method}) ",
                f"rebate={self.rebate}) ",
                f"payout={self.payout})")