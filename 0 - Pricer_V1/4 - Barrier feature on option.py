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

from C_Vanilla_V1.Barrier import Barrier_Feature
from C_Vanilla_V1.Model import Barrier_Model

# Lets show how the new feature related to barrier option is working

# --- Parameters 

date_start = date(2010, 1, 1)
date_end = date(2011, 1, 1)
mid_date = date_start + (date_end - date_start) / 2

level_method = "relative"  # "absolute" or "relative"
basket_method = "uniform"
steps = 2
n_paths = 100_000

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

Barrier = Barrier_Feature(
    start_date=date_start,
    end_date=date_end,
    barrier_mecanism='D&I',
    barrier_exercise='EU',
    barrier_level=1.0,
    spot_price=Equity_1.spot,
    value_method=level_method,
    paths=new_paths,
    observation_dates=[date_start, mid_date, date_end],
    calendar=Calendar_Config
)

Barrier_model = Barrier_Model(
    barrier_feature=Barrier,
    config=Sim_Config
)

time_start = time.time()
Barrier_observation = Barrier_model.observe()
time_end = time.time()

print(f"Computation time for barrier observation: {time_end - time_start} seconds")

n_first = 10
print(f'Parameters: barrier_level={Barrier_model.level}, value_method={Barrier.value_method}') 
for i in range(n_first):
    print(f'Path {i} : {Barrier_observation[i]} , {new_paths[i]}' )
