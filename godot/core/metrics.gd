extends Node
## Run metrics (autoload `Metrics`).
##
## Components report events; this node keeps counters and blocked/starved
## timers per station and writes them out as CSV at the end of a run
## (`runs/<timestamp>_<line>_<recipe>.csv`, a path the batch runner passes in).

var counts: Dictionary = {}       # station -> items passed
var blocked_time: Dictionary = {} # station -> seconds blocked (downstream full)
var starved_time: Dictionary = {} # station -> seconds starved (no upstream supply)
var _state: Dictionary = {}       # station -> "running" | "blocked" | "starved"


func _ready() -> void:
	SimClock.stepped.connect(_on_stepped)
	SimClock.reset_done.connect(clear)


func clear() -> void:
	counts.clear()
	blocked_time.clear()
	starved_time.clear()
	_state.clear()


func count(station: String, n: int = 1) -> void:
	counts[station] = counts.get(station, 0) + n


func set_state(station: String, state: String) -> void:
	_state[station] = state


func _on_stepped(_tick: int, dt: float) -> void:
	for s in _state:
		match _state[s]:
			"blocked":
				blocked_time[s] = blocked_time.get(s, 0.0) + dt
			"starved":
				starved_time[s] = starved_time.get(s, 0.0) + dt


## Throughput in items per minute for a station over the run so far.
func rate_per_min(station: String) -> float:
	if SimClock.sim_time <= 0.0:
		return 0.0
	return counts.get(station, 0) * 60.0 / SimClock.sim_time


func write_csv(path: String) -> void:
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f == null:
		push_error("Metrics: cannot write %s" % path)
		return
	f.store_line("station,count,rate_per_min,blocked_s,starved_s,sim_time_s")
	var stations := {}
	for d in [counts, blocked_time, starved_time]:
		for s in d:
			stations[s] = true
	for s in stations:
		f.store_line("%s,%d,%.3f,%.3f,%.3f,%.3f" % [
			s, counts.get(s, 0), rate_per_min(s),
			blocked_time.get(s, 0.0), starved_time.get(s, 0.0), SimClock.sim_time])
	f.close()
