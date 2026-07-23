## Birth, and the first pivot

On 20 April 2026 the first commit is called `init: polybot live`. The idea fits in
one sentence: Polymarket runs markets on the daily high temperature in about fifty
cities, weather models publish forecasts for free, and where the two disagree
there is money to take.

The next five commits, all the same day, say the rest: `fix: slug date format`,
`fix: edge formulas, rounding, regex`, `fix: handle forecast weather api NaN
return`. The concept was simple; contact with reality less so.

The first structural decision came a week later. Rather than keep editing a bot
playing real money in production to find out whether an idea works, I built a
separate **replay laboratory**: nine months of market history, an engine replaying
decisions as if they were taken at the time, and one rule written down in the
project notes:

> Calibration must be built with a cutoff date strictly earlier than the replay
> period.

Without this rule, a backtest uses, to predict a given day, information that
did not exist yet on that day. The results are false, but the performance
curve stays good: nothing signals the error. It is called data leakage, and it
is the leading cause of strategies that succeed in simulation and fail in
production.

The chart below shows what six weeks of development actually looked like.
