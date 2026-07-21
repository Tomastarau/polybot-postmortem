## Real money, then the crash

On 19 May the bot goes live for real. Two commits accompany the switch: migrating
to version 2 of the Polymarket client, then `fix: Polymarket order placement bugs
(min_order_size + tick_size)` — orders were being rejected for respecting neither
the minimum size nor the book's tick.

Eleven days of real trading follow, then the stop. On 6 June the bot returns to
simulation. The wallet is down to 36 dollars.

The diagnosis was wrong at first. Adding up every line of the on-chain ledger, I
got a loss of 57 dollars. The real figure was half that: I was counting
**stop-loss sales** as spending, when they are precisely the opposite — money
coming back in as a position is cut. The ledger holds three event types (buy,
sell, redeem) and I was treating two of them as one.

Once the arithmetic was right, the real problem appeared, and it is not the win
rate: **asymmetry**. A winning bet pays 0.68 dollars on average. A losing one
costs 4.27. So you need six wins to absorb one failure. At 88 % accuracy you get
roughly seven wins per failure. The margin rests on a hair, and one bad day
consumes it entirely.

More volume changes nothing — that is exactly the trap. Multiplying bets
multiplies both sides of the scale in proportion. When the payoff structure is
asymmetric, only **selection** can help: bet less often, but better. That is what
the next chapter attempts, and that is where it gets interesting.
