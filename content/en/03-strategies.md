## Hunting for a strategy

May is a run of ideas tried and dropped.

The first is the **yield scanner**. It starts from an observation: on these
markets some bets are all but settled already. When it is 8 p.m. and the day's
high is already known, betting "no, it will not be 9 °C" is no longer a
prediction, it is an observation. The bet costs 0.97 and pays 1.00: 3 % in a few
hours, almost risk-free. The bot's earliest traces, from 3 May, are 1,322 markets
scanned on exactly that logic.

The trouble with free money is that everyone can see it. The 3 % was already taken
by the time the bot arrived, and the "observed" strategy eventually stopped
trading altogether: over its last active days it declined 1,510 bets in a row for
being *too expensive*.

Hence the 12 May pivot, summed up by an unambiguous commit: `rm: everything but D0
yield`. Everything else is deleted. The bot keeps one strategy: betting **before**
the temperature is known, on the strength of the forecasts, against the
temperature bands the models judge unlikely. It moves from observing to
predicting — and so from no risk to real risk.

What the chart below shows is the direct consequence of that choice: a bot that
spends the overwhelming majority of its time refusing to play.
