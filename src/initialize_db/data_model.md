# Database: main
## H_ETORO_DEPOSITS_TRANSACTION
id INTEGER PRIMARY KEY AUTOINCREMENT,
amount REAL NOT NULL,              
currency TEXT NOT NULL DEFAULT 'USD',
deposited_at TEXT NOT NULL,
modified_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

## H_ETORO_DEPOSITS_SERIES
snapshot_date TEXT PRIMARY KEY NOT NULL,
value_usd REAL NOT NULL,
value_pen REAL NOT NULL,
fixed_value INT NOT NULL,
modified_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

## H_ETORO_BALANCE_SERIES
snapshot_date TEXT PRIMARY KEY NOT NULL,
value_usd REAL NOT NULL,
value_pen REAL NOT NULL,
fixed_value INT NOT NULL,
modified_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

## H_BCRP_EXCHANGE_RATE_SERIES
snapshot_date TEXT PRIMARY KEY NOT NULL,
pen_to_usd REAL NOT NULL,
usd_to_pen REAL NOT NULL,
fixed_value INT NOT NULL,
modified_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

## H_CREDITCARD__TRANSACTION
id INTEGER PRIMARY KEY AUTOINCREMENT,
amount REAL NOT NULL,              
currency TEXT NOT NULL DEFAULT 'PEN',
executed_at TEXT NOT NULL,
card_id TEXT NOT NULL,
modified_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

## H_CREDITCARD__TRANSACTION
id INTEGER PRIMARY KEY AUTOINCREMENT,
amount REAL NOT NULL,              
currency TEXT NOT NULL DEFAULT 'PEN',
executed_at TEXT NOT NULL,
creditcard_id TEXT NOT NULL,
modified_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

## M_CREDITCARD_DESCRIPTION
creditcard_id PRIMARY KEY TEXT NOT NULL,
creditcard_name TEXT NOT NULL,
entity TEXT NOT NULL,
max_credit TEXT NOT NULL

## H_CREDITCARD_SERIES  
### fields
snapshot_date TEXT PRIMARY KEY NOT NULL,
value_usd REAL NOT NULL,
value_pen REAL NOT NULL,
fixed_value INT NOT NULL,
creditcard_id TEXT NOT NULL,
modified_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
PRIMARY KEY (snapshot_date, creditcard_id)
### indices: 
idx_h_creditcard_series_snapshot_date ON h_creditcard_series(snapshot_date);
idx_h_creditcard_series_creditcard_id ON h_creditcard_series(creditcard_id,snapshot_date);
