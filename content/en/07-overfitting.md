## The overfitting trap

On 8 May a commit is called `fix: blacklisting cities that lose regularly`. The
intuition looks unassailable: some cities have unstable climates, forecasts do
badly there, the bot loses money there. Just stop playing them.

In June, after the real losses, I set out to formalise the idea: a rolling
per-city reliability score, recomputed over fourteen days, automatically declining
cities that had lost recently. The design was ready to implement.

Two months of data settled it before I wrote a single line.

The method is the one that should have been applied from the start. Cut the
history in two: May-June to **build** the filter, July to **test** it. The filter
is calibrated on the first half only, then applied untouched to the second, with
no readjustment whatsoever.

On the training data the return climbs from +0.14 % to **+7.24 %**. Nine
cities excluded, nearly every loss removed.

On July, the same filter returns **−0.40 %**.

The explanation is simple: the cities that were losing in June had had
difficult weather **in June**. The filter had memorised June's weather. This is
the very definition of overfitting, and it is all the more insidious here
because it confirmed an intuition I had held for two months.

A test that cannot fail proves nothing. A strategy has to be evaluated on data
that was not used to build it.
