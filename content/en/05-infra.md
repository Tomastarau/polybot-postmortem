## Running a bot around the clock

The bot lived on a small rented machine in Frankfurt: two processors, two
gigabytes of memory. It never restarted on its own in three months.

Scheduling does not rely on a program looping forever, but on **sixteen systemd
timers** waking short tasks: find the day's markets, sample the order books, mark
open positions, reconcile against the blockchain, produce a daily digest. Each
task starts, does its job, and dies.

That choice has a very concrete practical consequence: because every run rereads
its configuration at startup, changing a parameter requires no service restart.
Switching the bot to simulation mode means editing one line in a file. The
next task to wake up honours it. A long-running loop would have demanded
signal handling and hot reloading.

The other structural decision was to log far too much. Twenty gigabytes of traces
for a bot staking two dollars: every decision, every order book, every forecast,
every official settlement. At the time it was disproportionate.

It is nonetheless the reason this site exists. The analyses that closed the
project (the city filter's overfitting, the demonstration that the win rate was
worthless) answer questions I was not asking when I wrote that logging. **You can
only analyse what you thought to record.** Storage costs pennies; the data you
failed to capture is gone forever.
