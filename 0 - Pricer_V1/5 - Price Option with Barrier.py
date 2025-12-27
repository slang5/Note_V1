from os import name
from sys import path
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path.insert(0, str(ROOT))

from datetime import date
import time

from B_Model_V1.base import SimulationConfig, BasketModel
from B_Model_V1.bs_model import BS_Model, UnderlyingParams, PortfolioParams
from B_Model_V1.timegrid import Calendar

from A_Underlying_V1.database import Database
from C_Vanilla_V1.Model import Vanilla_Barrier_Model
from C_Vanilla_V1.Option import Option_Call
from C_Vanilla_V1.Barrier import Barrier_Feature

# Lets show how price a call option with a D&I barrier feature (ideal path is down first then huge up)

# --- Parameters 

date_start = date(2010, 1, 1)
date_end = date(2011, 1, 1)
mid_date = date_start + (date_end - date_start) / 2

level_method = "absolute"  # "absolute" or "relative"
basket_method = "uniform"
steps = 5
n_paths = 1_000_000
barrier_type = 'D&I'
barrier_obs = 'EU'
barrier_method = "Last"

Equity_1 = UnderlyingParams(
    isin="FR0000131104",
    spot=50.0,
    vol=0.2,
    rate=0.01,
    div=0.03
)

Portfolio = PortfolioParams(
    underlyings={Equity_1.isin: Equity_1}
)

DB = Database()
db_path = ROOT / "0 - Pricer_V1" / "database.csv"
DB.start_connection(str(db_path))
Eq1 = DB.get_underlying("FR0000131104")
DB.end_connection()

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
    underlyings=Portfolio.underlyings,
    calendar=Sim_Config.calendar,
    n_paths=Sim_Config.n_paths,
    seed=Sim_Config.seed,
    antithetic=Sim_Config.antithetic
) 

if level_method == "absolute":
    Paths = BS.apply_bs_value()
else: # level_method == "relative"
    Paths = BS.apply_bs_percentage()

Basket = BasketModel(
    config=Sim_Config,
    n_underlyings=len(Portfolio.underlyings),
    basket_method=basket_method,
    paths=Paths
) 

new_paths = Basket.apply_basket_method()

Call = Option_Call(
    start_date=date_start,
    end_date=date_end,
    option_type="EU",
    strike_price=50.0,
    value_method="absolute",
    underlyings=[Eq1],
    basket_method=basket_method,
    rebate=0.0,
    levier=1.0
)

Barrier = Barrier_Feature(
    start_date=date_start,
    end_date=date_end,
    barrier_mecanism=barrier_type,
    barrier_exercise=barrier_obs,
    barrier_level=50.0,
    spot_price=Equity_1.spot,
    value_method=level_method,
    observation_dates=[mid_date],
    calendar=Calendar_Config
)

Call_DownIn_Option = Vanilla_Barrier_Model(
    option=Call,
    barrier_feature=Barrier,
    barrier_method=barrier_method,
    config=Sim_Config,
    paths=new_paths,
    strikes_dates=[mid_date, date_end],
    rebate_if_not_activated=False
)

start_time = time.time()

pricing = Call_DownIn_Option.price(spot=Equity_1.spot)

end_time = time.time()

print(f"Pricing took {end_time - start_time} seconds")

print("Pricing results:")
for k, v in pricing.items():
    print(f"  Date: {k}, Price: {v['price']:.4f}, Std: {v['std']:.4f}")