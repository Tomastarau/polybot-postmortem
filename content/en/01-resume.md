## Three months, one bot, and a result of zero

Between 20 April and 20 July 2026, a program bet on its own on the daily high
temperature in 48 cities. It read seven weather sources, compared their forecasts
against the odds on Polymarket, and bought whenever it judged the market too
expensive. It ran on a small server in Frankfurt, woken every five minutes by
systemd timers, and it produced 1.27 million lines of logs.

This site is the story of what it did, and why I shut it down.

The short answer is below: across 752 bets, it made **1.12 dollars**. Not 1,120 —
one dollar and twelve cents, on 1,504 dollars deployed. A return of 0.07 %, which
is to say roughly nothing at all.

The interesting part isn't that number, it's the win rate beside it: **88 % of
the bets were winners**. The kind of figure you'd happily put on a pitch deck,
and which is worth nothing here — because the bot was paying 88 cents for
something that pays out one dollar. Winning 88 times out of 100 *was* the
break-even line. Everything that follows is the story of understanding that,
trying to beat it, and failing honestly.
