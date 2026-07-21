## Data and method

This site contains no hand-written figures. Everything is recomputed at load time
from four Parquet files published in the repository, themselves distilled from
1.27 million lines of raw logs.

### The tables

| File | Rows | Contents |
|---|---|---|
| `decisions.parquet` | 48,826 | Every evaluated opportunity: forecast, disagreement between models, estimated probability, price, rejection reason |
| `market_snapshots.parquet` | 133,559 | The state of the order book at decision time |
| `resolutions.parquet` | 2,392 | The official settlement temperature, per city and date |
| `real_trades.parquet` | 127 | On-chain movements, anonymised |
| `commits.parquet` | 52 | The bot's git history |

### How P&L is reconstructed

The bot bet **no** on a temperature band. It wins when the official temperature
lands outside that band. At a fixed 2 dollar stake, a winning bet pays
`2 / price − 2` and a losing one costs 2 dollars. Each decision is joined to the
official settlement for its city and date, and summed.

### Reduction and anonymisation

Settlements were recorded every five minutes: 822,000 rows for 2,392 real events.
Only the final state of each `(city, date)` is kept. On-chain records are stripped
of wallet address, pseudonym and transaction hashes — a test fails if any of them
reappears.

### What locks the numbers

The figures quoted in the story are covered by tests that recompute them from the
published data. If a table changes and a number moves, the suite breaks. That is
deliberate: the text cannot drift from the data without something complaining.

The extraction code, the conversion and the tests are all in the repository.
Everything is verifiable without trusting me.
