chronostat
==========

Usage
-----

```
import chronostat, time
stats = chronostat.ChronoStat('me@mydomain.com')

with stats.timer('context_manager'):
  time.sleep(1)
  
# or

@stats.timer('decorator')
def sleepy():
  time.sleep(1)
  
```
   
