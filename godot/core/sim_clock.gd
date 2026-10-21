extends Node
## Fixed-step simulation clock (autoload `SimClock`).
##
## The simulation advances only in `_physics_process`, which Godot runs at
## `physics/common/physics_ticks_per_second` (100 Hz). Nothing in the sim may
## read wall-clock time: every component derives timing from `tick` and `dt`
## so that a run is reproducible on any machine.

signal stepped(tick: int, dt: float)
signal started
signal paused
signal reset_done

## Step length in seconds. Matches the physics tick rate.
var dt: float = 1.0 / float(ProjectSettings.get_setting("physics/common/physics_ticks_per_second", 100))
## Number of steps since the last reset.
var tick: int = 0
## Simulated time in seconds since the last reset.
var sim_time: float = 0.0
var running: bool = false
## Seed for all randomness in the sim (jams, downtime). Set before `reset()`.
var rng_seed: int = 0
var rng := RandomNumberGenerator.new()


func start() -> void:
	running = true
	started.emit()


func pause() -> void:
	running = false
	paused.emit()


func reset(new_seed: int = rng_seed) -> void:
	rng_seed = new_seed
	rng.seed = rng_seed
	tick = 0
	sim_time = 0.0
	reset_done.emit()


func _physics_process(_delta: float) -> void:
	if not running:
		return
	tick += 1
	sim_time = tick * dt
	stepped.emit(tick, dt)
