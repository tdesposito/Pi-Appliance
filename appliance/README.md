# Appliance Code, Where Are You?

Right here, as it turns out.

Place your appliance code into `appliance.py`. Naturally, you can location
portions of your code in other files and import them here.

## `__init__()`
The appliance framework configures and passes a logger object, which
`__init__()` stores for future use. You can, of course, use:
```python
import logging
logger = logging.getLogger()
```
and get similar results.

## `pre_flight_checks()`
Add any code needed to validate the environment.

This is useful if you need, for example, to test for the existence of external
resources or conditions before running.

Return True if we're ready to start; False if not.

## `run()`
This is the body of the main loop.

You don't have to put any looping in if you don't want to. This will be called
repeatedly by the framework code until you return False.

## `shutdown()`
Add any cleanup or shutdown you need to do here.
