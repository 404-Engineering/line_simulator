extends Node
## Link to the Python PLC bridge (`bridge/`).
##
## Protocol (see docs/DESIGN.md §3): one UDP datagram per direction per step.
##   Godot → bridge:  {"tick": N, "inputs": {name: value, ...}}
##   bridge → Godot:  {"tick": N, "outputs": {name: value, ...}}
## JSON for Phase 0–2; switch to a packed binary layout if latency numbers
## demand it. The bridge is optional: with no bridge running, outputs keep
## whatever a scripted controller last wrote.

@export var host: String = "127.0.0.1"
@export var send_port: int = 7401
@export var listen_port: int = 7402

var _udp := PacketPeerUDP.new()
var _connected := false


func _ready() -> void:
	var err := _udp.bind(listen_port)
	if err != OK:
		push_warning("BridgeClient: could not bind UDP %d (%s)" % [listen_port, error_string(err)])
		return
	_udp.set_dest_address(host, send_port)
	_connected = true
	SimClock.stepped.connect(_on_stepped)


func _on_stepped(tick: int, _dt: float) -> void:
	if not _connected:
		return
	_send_inputs(tick)
	_receive_outputs()


func _send_inputs(tick: int) -> void:
	var inputs := {}
	for n in SignalBus.names(SignalBus.Direction.INPUT):
		inputs[n] = SignalBus.get_value(n)
	var msg := JSON.stringify({"tick": tick, "inputs": inputs})
	_udp.put_packet(msg.to_utf8_buffer())


func _receive_outputs() -> void:
	while _udp.get_available_packet_count() > 0:
		var text := _udp.get_packet().get_string_from_utf8()
		var parsed = JSON.parse_string(text)
		if typeof(parsed) != TYPE_DICTIONARY or not parsed.has("outputs"):
			push_warning("BridgeClient: bad packet: %s" % text)
			continue
		for n in parsed["outputs"]:
			if SignalBus.has(n):
				SignalBus.set_value(n, parsed["outputs"][n])
