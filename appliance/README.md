# Appliance Code, Where Are You?

Right here, as it turns out.

Place your appliance code into `appliance.py`. Naturally, you can locate
portions of your code in other files and import them here.

## How the Framework Operates
The framework in `__main__.py` performs the tasks needed to support and run your
appliance code.

### Logger
We create and configure the system logger. We output all `INFO` or higher log
entries to the console and to `/home/pi/log/appliance.log`. The log file is
automatically rotated when it exceeds 128kb in size, and we keep four
previously-rotated logs.

This logger is available as `self.logger` inside the `Appliance` instance.

### The Lock File
The framework stores its PID in a lockfile at
`/var/run/user/1000/appliance.pid`. If this file exists when the framework
starts up, we assume we're already running and abort.

This file is deleted upon exit, and since it's in the tempfs, rebooting clears
it as well.

### The Main Loop
The framework wraps the main loop (see `run()` below) in a `try/except` block.
If we catch a SIGINT or Ctrl-C, we call `shutdown()` and exit. Any other
exception is logged, `shutdown()` is **NOT** called, and we exit. Please wrap
anything and everything which could raise an exception inside your `Appliance`
methods in `try/except` blocks!

### `Appliance` Instance
We construct an instance of the `Appliance` class defined in `appliance.py`.
This object encapsulates and defines the appliance's operations.

Add your code to the several methods therein (defined below) to make the
appliance work.

The framework will first call `Appliance.pre_flight_checks()`.

Then it calls `Appliance.run()` in an infinite loop, until `run()` returns
something Falsey. **Failing to return anything at all returns None, which will
terminate the loop, so always return `True` from `run()` unless you want to exit
the appliance.**

Finally, it calls `Appliance.shutdown()` **unless it encounters an unexpected exception.**

## Add Your Code
### `__init__()`
The appliance framework configures and passes a logger object, which
`__init__()` stores as `self.logger` for future use. You can, of course, use:
```python
import logging
logger = logging.getLogger()
```
and get similar results.

This is a good place to update the logger configuration for any libraries you
may use.

### `pre_flight_checks()`
Add any code needed to validate the environment.

This is useful if you need, for example, to test for the existence of external
resources or conditions before running.

Return True if we're ready to start; False if not.

### `run()`
This is the body of the main loop.

This will be called repeatedly by the framework code until you return something
Falsey.

This framework is designed to be single-threaded; if you want to implement a
multi-threaded appliance, you should NOT return from `run()` **AT ALL** until all
your threads are completed and joined.

### `shutdown()`
Add any cleanup or shutdown you need to do here. This MAY be called after a
keyboard interrupt (Ctrl-C) or SIGINT signal, which would have interrupted the
`run()` function, so be careful with possible state issues.
