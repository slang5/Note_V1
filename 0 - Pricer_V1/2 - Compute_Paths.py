from os import name
from sys import path
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path.insert(0, str(ROOT))

from datetime import date
from numpy.typing import NDArray
import time

from B_Model_V1.bs_model import BS_Model, UnderlyingParams, PortfolioParams
from B_Model_V1.timegrid import Calendar
from B_Model_V1.base import SimulationConfig, BasketModel

Equity_1 = UnderlyingParams(
    isin="FR0000131104",
    spot=50.0,
    vol=0.2,
    rate=0.01,
    div=0.03
)

Equity_2 = UnderlyingParams(
    isin="FR0000130809",
    spot=100.0,
    vol=0.2,
    rate=0.01,
    div=0.03
)

Equity_3 = UnderlyingParams(
    isin="FR0000121014",
    spot=150.0,
    vol=0.2,
    rate=0.01,
    div=0.03
)

portfolio = PortfolioParams(
    underlyings={
        Equity_1.isin: Equity_1,
        Equity_2.isin: Equity_2,
        Equity_3.isin: Equity_3}
)

Calendar_Config = Calendar(
    start_date=date(2010, 1, 1),
    end_date=date(2011, 1, 1),
    n_steps=2,
    trading_days=365.0
)

Sim_Config = SimulationConfig(
    calendar=Calendar_Config,
    n_paths=1_000_000,
    seed=42,
    antithetic=True
)

BS = BS_Model(
    underlyings=portfolio.underlyings,
    calendar=Sim_Config.calendar,
    n_paths=Sim_Config.n_paths,
    seed=Sim_Config.seed,
    antithetic=Sim_Config.antithetic
) 

start = time.time()

Paths = BS.apply_bs_percentage()

Basket = BasketModel(
    config=Sim_Config,
    n_underlyings=len(portfolio.underlyings),
    basket_method="uniform",
    paths=Paths,
)

Basket_paths = Basket.apply_basket_method()
#print(Basket_paths)

end = time.time()
print(f"Computation Time: {end - start} seconds")

from C_Vanilla_V1.Model import Vanilla_Model
from C_Vanilla_V1.Option import Option_Call, Option_Put, Digital_Call, Digital_Put
from A_Underlying_V1.database import Database

All_dates = Calendar_Config.get_dates
dates = [date(2010, 1, 1), date(2011, 1, 1)]#, date(2010, 3, 18), date(2012, 5, 26), date(2012, 10, 27)]

DB = Database()
DB.start_connection(r"C:\\Users\\luang\\Documents\\Note_V1\\0 - Pricer_V1\\database.csv")
Eq1 = DB.get_underlying("FR0000131104")
DB.end_connection()

Call = Option_Call(
    start_date=date(2010, 1, 1), 
    end_date=date(2011, 1, 1), 
    option_type='EU', 
    strike_price=1, 
    value_method='relative', 
    underlyings=[Eq1], 
    basket_method="best-of",
    rebate=0
)

Vanilla = Vanilla_Model(
    option=Call,
    config=Sim_Config,
    paths=Basket_paths,
    strikes_dates=dates
)

Vanilla.update_strikes_dates()
price = Vanilla.price(spot=1)

print(price)