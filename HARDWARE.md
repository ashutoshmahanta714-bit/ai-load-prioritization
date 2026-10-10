# Low-voltage demonstration and site adaptation

## First physical prototype: five indicators
Use five independently controlled LED indicators to represent the five loads.
This demonstrates decisions only; LED brightness is not a measurement of actual
kW. The 100 kW slide example can be represented by normalized indicator levels.
An LED on represents full supply, off represents shedding, and dimmed LED
represents a demand-controlled branch. Keep any pump/motor demonstration
full-or-zero unless its driver explicitly supports demand control.

Required categories: development controller with suitable output pins, current-
limited LEDs, breadboard, USB power and USB cable. Select resistors and pin
currents using the actual board and LED specifications. No mains connection.

Interface contract for future firmware:
Host sends an integer sequence number and five output levels (0..255).
Controller validates ranges, acknowledges applied outputs, and reports errors.
Switchable channels accept only 0 or 255. Dimmable channels accept intermediate
values. Never equate dimming with safely reducing voltage to arbitrary devices.
A physical stop button, watchdog and operator override must be tested.
The safe response to timeout must be designed per application; disconnecting
all loads is not a universally safe response.

## Integration still required
Firmware, serial bridge, sensor calibration and measured supply feedback have
not been implemented or bench-tested in v0.1. Choose the available board before
wiring/firmware implementation. This package is a software prototype and a
hardware plan, not a completed physical device.

## From demo to a site
Homes, campuses and factories need different priorities and control ratings.
Real switching requires appropriately rated protection, isolation, metering and
switchgear, installed and validated by qualified electrical professionals.
Loads such as essential medical equipment need site-specific service guarantees.
Allocation cannot replace protection relays or emergency supply systems.
For network stability claims, introduce a validated electrical-network model
and then measure voltage and frequency during supervised experiments.
