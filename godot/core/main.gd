extends Node3D
## Entry point. Loads a line scene under $Line and starts the simulation clock.
##
## Which line to load comes from the command line (`--line line2`) or defaults
## to the test scene while the project is in Phase 0.

const DEFAULT_LINE := "res://scenes/test/conveyor_spike.tscn"


func _ready() -> void:
	var line_path := _line_from_args()
	if ResourceLoader.exists(line_path):
		var line: Node = load(line_path).instantiate()
		$Line.add_child(line)
		print("Loaded line: %s" % line_path)
	else:
		push_warning("No line scene at %s; running with an empty line." % line_path)
	SimClock.start()


func _line_from_args() -> String:
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--line" and i + 1 < args.size():
			return "res://scenes/lines/%s.tscn" % args[i + 1]
	return DEFAULT_LINE
