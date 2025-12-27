from os import name
from sys import path
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path.insert(0, str(ROOT))

from datetime import date
import time

from B_Model_V1.bs_model import BS_Model, UnderlyingParams, PortfolioParams
from B_Model_V1.timegrid import Calendar
from B_Model_V1.base import SimulationConfig, BasketModel

from C_Vanilla_V1.Model import Vanilla_Model
from C_Vanilla_V1.Option import Option_Call
from A_Underlying_V1.database import Database

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
        Equity_1.isin: Equity_1,})
        #Equity_2.isin: Equity_2,
        #Equity_3.isin: Equity_3}
#)

date_start = date(2010, 1, 1)
date_end = date(2011, 1, 1)
mid_date = date_start + (date_end - date_start) / 2

basket_method = "uniform"
steps = 5
n_paths = 100_000

Calendar_Config = Calendar(
    start_date=date_start,
    end_date=date_end,
    n_steps=steps,
    trading_days=365.0
)

Sim_Config = SimulationConfig(
    calendar=Calendar_Config,
    n_paths=n_paths,
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

Paths = BS.apply_bs_value() 

Basket = BasketModel(
    config=Sim_Config,
    n_underlyings=len(portfolio.underlyings),
    basket_method=basket_method,
    paths=Paths,
)

Basket_paths = Basket.apply_basket_method()
dates = [mid_date, date_end]

DB = Database()
db_path = ROOT / "0 - Pricer_V1" / "database.csv"
DB.start_connection(str(db_path))
Eq1 = DB.get_underlying("FR0000131104")
Eq2 = DB.get_underlying("FR0000130809")
Eq3 = DB.get_underlying("FR0000121014")
DB.end_connection()

# Call Opttion from "start_date" to "end_date" with strike price 1.1 (relative i.e 110% of spot value) 
# European exercise, and equaly weighted basket of the three equities
# No rebate 
# use relative value method due to several underlyings with different spot prices i.e we only use the spot variation since inception

Call = Option_Call(
    start_date=date_start, 
    end_date=date_end, 
    option_type='EU', 
    strike_price=50, 
    value_method='absolute', 
    underlyings=[Eq1],# Eq2, Eq3], 
    basket_method=basket_method,
    rebate=0.0,
    levier=1.0
)

Vanilla = Vanilla_Model(
    option=Call,
    config=Sim_Config,
    paths=Basket_paths,
    strikes_dates=dates,
)

start_timer = time.time()

Vanilla.update_strikes_dates()
price = Vanilla.price()

end_timer = time.time()

print("Pricing results:")
for k, v in price.items():
    print(f"  Date: {k}, Price: {v['price']:.4f}, Std: {v['std']:.4f}")
print(f"Computation Time: {end_timer - start_timer} seconds")