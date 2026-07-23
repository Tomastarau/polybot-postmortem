## Three months of automated trading

Between 20 April and 20 July 2026, a program bet on its own on the daily high
temperature in 48 cities. It read seven weather sources, compared their forecasts
against the odds on Polymarket, and bought whenever it judged the market too
expensive. It ran on a small server in Frankfurt, woken every five minutes by
systemd timers. It produced 1.27 million lines of logs.

This site tells what it did, and why I shut it down.

Across 752 bets, it made **1.12 dollars**. Not 1,120. One dollar and twelve
cents, on 1,504 dollars deployed, a return of 0.07 %.

The win rate that goes with this result is **88 %**. The bot was buying at 88
cents something that pays out one dollar, so winning 88 times out of 100 was
exactly its break-even threshold. The rest of this story is how I understood
that, tried to beat it, and failed.
