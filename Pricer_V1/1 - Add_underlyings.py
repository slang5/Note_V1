from sys import path
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path.insert(0, str(ROOT))

from Underlying_V1.underlying_class import Underlying
from Underlying_V1.database import Database

db = Database()

# Create some underlying instances only in equity (engine supports only equity for now)

ul_1 = Underlying(name="BNP PARIBAS ACT.A",
                  symbol="BNP FP",
                  exchange="XPAR",
                  isin="FR0000131104",
                  type="EQUITY", 
                  )

ul_2 = Underlying(name="SOCIETE GENERALE",
                  symbol="GLE FP",
                  exchange="XPAR",
                  isin="FR0000130809",
                  type="EQUITY", 
                  )

ul_3 = Underlying(name="LVMH",
                  symbol="MC FP",
                  exchange="XPAR",
                  isin="FR0000121014",
                  type="EQUITY", 
                  )

ul_4 = Underlying(name="TOTALENERGIES",
                  symbol="TTE FP",
                  exchange="XPAR",
                  isin="FR0000120271",
                  type="EQUITY", 
                  )

list_underlyings = [ul_1, ul_2, ul_3, ul_4]

db_path = ROOT / "Pricer_V1" / "database.csv"

db = Database()
db.create_database(str(db_path))
db.start_connection(str(db_path))
db.add_underlyings(list_underlyings)

print(db.get_all_underlyings())

db.end_connection()
