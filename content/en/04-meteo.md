## Weather is a data problem

Forecasting temperature looks like a meteorology problem. In practice it is
plumbing.

The bot ended up reading seven sources: the ECMWF and GFS models for forecasts,
then real observations through aviation METARs, Japan's AMEDAS network, the US
NWS, and Wunderground for the official history. Each has its own format, timezone,
frequency and gaps.

Three bugs are worth telling, because they are all the same bug.

**Tokyo did not match.** The weather station used to forecast was not the one used
to settle the market. Two thermometers a few kilometres apart, and lost bets that
had nothing to do with the forecast.

**Yesterday polluted today.** The code read `reportTime`, when an observation is
published, instead of `obsTime`, when it was measured. A reading taken at 23:50
and published at 00:10 landed in the wrong day and corrupted the daily maximum.

**And above all, the degrees.** Eleven US cities settle their markets in
Fahrenheit; forecasts arrived in Celsius. Compared without conversion they
produced a forecast error of 54 degrees — a number so absurd it should have been
obvious, and which stayed invisible as long as nobody looked at the distribution.

That is what the chart below shows, and it is the most useful lesson of the
project: **a broken metric is more dangerous than a missing one**. A missing
metric, you know you don't have. A broken metric, you read, you trust, and you
make decisions with.
