extends Node
## Named I/O signals (autoload `SignalBus`).
##
## Components publish sensor values and read actuator commands here by name,
## e.g. `filler.infeed_pe` or `conv_03.speed_cmd`. The PLC bridge maps names to
## PLC tags using `config/tagmaps/<line>.yaml`; a scripted controller can drive
## the same names without a PLC. Components never talk to the bridge directly.
##
## Direction is from the simulator's point of view:
##   - input:  written by a component (sensor), read by the controller
##   - output: written by the controller, read by a component (actuator)

enum Direction { INPUT, OUTPUT }

signal value_changed(name: String, value: Variant)

var _values: Dictionary = {}
var _directions: Dictionary = {}


## Register a signal. Components call this in `_ready()`.
func register(name: String, direction: Direction, initial: Variant) -> void:
	if _values.has(name):
		push_error("SignalBus: duplicate signal '%s'" % name)
		return
	_values[name] = initial
	_directions[name] = direction


func set_value(name: String, value: Variant) -> void:
	if not _values.has(name):
		push_error("SignalBus: unknown signal '%s'" % name)
		return
	if _values[name] != value:
		_values[name] = value
		value_changed.emit(name, value)


func get_value(name: String, default: Variant = null) -> Variant:
	return _values.get(name, default)


func has(name: String) -> bool:
	return _values.has(name)


## All signals of one direction, for the bridge to batch-read inputs or
## batch-write outputs each step.
func names(direction: Direction) -> PackedStringArray:
	var out := PackedStringArray()
	for n in _directions:
		if _directions[n] == direction:
			out.append(n)
	return out


func snapshot() -> Dictionary:
	return _values.duplicate()
