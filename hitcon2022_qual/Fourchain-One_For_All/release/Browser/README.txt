* Based on the following git commit hash
    - chromium : d237ccca7a39256f4e18eb7ec9292bd0aa69dd84
    - V8 : 63cb7fb817e60e5633fb622baf18c59da7a0a682
* Apply `add_hole.patch` to V8, and `sandbox.patch` to chromium.
* args.gn:
is_debug=false
dcheck_always_on=false
enable_nacl=false
symbol_level=1
blink_symbol_level=0
v8_symbol_level=0
