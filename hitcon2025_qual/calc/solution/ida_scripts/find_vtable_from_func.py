import ida_segment
import ida_bytes
import ida_funcs
import json

def is_valid_rel_function(ea, vtable_base):
    """
    檢查這個相對 offset 是否指向一個合法函數。
    ea 是 offset entry 的地址（不是解出來的值）
    """
    offset = ida_bytes.get_dword(ea)
    target = vtable_base + offset
    return ida_funcs.get_func(target) is not None

def find_aarch64_relative_vtables(min_entries=2):
    vtables = []
    # 掃描 rodata 區段
    for seg in (ida_segment.get_segm_by_name(".rodata"), ida_segment.get_segm_by_name(".data.rel.ro")):
        
        if not seg:
            continue

        ea = seg.start_ea
        end = seg.end_ea

        while ea + 4 * (min_entries + 1) < end:
            # 第 0 個必為 0
            first = ida_bytes.get_dword(ea)
            if first != 0:
                ea += 4
                continue

            vtable_base = ea
            print(f"vtabl base:{hex(vtable_base)}")

            # 檢查第 1 個 offset 是否指向合法函數
            if not is_valid_rel_function(ea + 8, vtable_base):
                ea += 4
                continue

            # 檢查後續至少 min_entries 個 entries 是否也像是合法函數
            valid = True
            for i in range(3, 3 + min_entries):
                entry_ea = ea + i * 4
                offset = ida_bytes.get_dword(entry_ea)
                target = vtable_base + offset
                if not ida_funcs.get_func(target):
                    # valid = False
                    break

            if valid:
                vtables.append(vtable_base)
                ea += 4 * (min_entries + 1)  # 跳過整個 vtable
            else:
                ea += 4  # 繼續掃描

    return vtables


def get_rel_function(ea, vtable_base):
    offset = ida_bytes.get_dword(ea)
    return vtable_base + offset

# 🔍 執行並列出找到的 vtable 地址
vtables = find_aarch64_relative_vtables(min_entries=2)
print(f"✅ 找到可能的 vtable 數量: {len(vtables)}")
for i, v in enumerate(vtables):
    print(f"[{i+1}] vtable 位於 {hex(v)}")

def find_vtable_from_func(func_addr):
    """
    given a function address, return its vtable & entry address
    """
    for v in vtables:
        real_vtable = v + 8
        entry = real_vtable
        while is_valid_rel_function(entry, real_vtable):
            vf = get_rel_function(entry, real_vtable)
            if vf == func_addr:
                print(f"{hex(func_addr)} belongs to {hex(v)}, entry: {hex(entry)}")
                return v
            entry += 4                
target_vtable = find_vtable_from_func(0x36334)
print("Done.")