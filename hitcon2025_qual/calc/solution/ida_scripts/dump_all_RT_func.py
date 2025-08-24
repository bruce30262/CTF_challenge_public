import idautils
import idaapi
import idc
import ida_segment
import ida_bytes
import ida_funcs
import json

def calls_realloc(func_addr):
    """
    check if function call realloc
    """
    # 確保 func_addr 是函式開頭
    func = idaapi.get_func(func_addr)
    if not func:
        print(f"0x{func_addr:x} 不是有效的 function 起點")
        return False

    # 取得 realloc 的地址
    realloc_addr = idc.get_name_ea_simple("realloc")
    if realloc_addr == idc.BADADDR:
        print("找不到 realloc 符號，請確保有符號資料或重命名正確")
        return False

    # 遍歷整個 function 中的所有指令
    for ea in idautils.FuncItems(func.start_ea):
        if idaapi.is_call_insn(ea):
            # 確認 call 的目標
            callee = idc.get_operand_value(ea, 0)
            if callee == realloc_addr:
                return True

            # fallback: 用函數名比較（若間接呼叫或經過 PLT）
            name = idc.get_name(callee)
            if name == "realloc":
                return True

    return False
    
def is_valid_rel_function(ea, vtable_base):
    """
    check if ea is a valid relative vtable entry
    """
    offset = ida_bytes.get_dword(ea)
    target = vtable_base + offset
    return ida_funcs.get_func(target) is not None

def get_rel_function(ea, vtable_base):
    offset = ida_bytes.get_dword(ea)
    return vtable_base + offset

def find_aarch64_relative_vtables(min_entries=2):
    vtables = []
    # scan rodata section
    for seg in (ida_segment.get_segm_by_name(".rodata"), ida_segment.get_segm_by_name(".data.rel.ro")):
        
        if not seg:
            continue

        ea = seg.start_ea
        end = seg.end_ea

        while ea + 4 * (min_entries + 1) < end:
            # 0th must be 0
            first = ida_bytes.get_dword(ea)
            if first != 0:
                ea += 4
                continue

            vtable_base = ea
            print(f"vtabl base:{hex(vtable_base)}")

            # check if 1st entry is valid
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
                    break

            if valid:
                vtables.append(vtable_base)
                ea += 4 * (min_entries + 1)  # 跳過整個 vtable
            else:
                ea += 4  # 繼續掃描

    return vtables


# find all possible relative vtables
vtables = find_aarch64_relative_vtables(min_entries=2)
print(f"✅ 找到可能的 vtable 數量: {len(vtables)}")
for i, v in enumerate(vtables):
    print(f"[{i+1}] vtable 位於 {hex(v)}")

# find all relative virtual functions
vfs = set()
for v in vtables:
    real_vtable = v + 8
    entry = real_vtable
    while is_valid_rel_function(entry, real_vtable):
        vf = get_rel_function(entry, real_vtable)
        if not calls_realloc(vf): # filter out the one that calls realloc
            vfs.add(vf)
        entry += 4

print(f"vfs number: {len(vfs)}")
vfs_json = json.dumps(sorted(list(vfs)), indent=4)
# Writing to sample.json
with open("vfs.json", "w") as outfile:
    outfile.write(vfs_json)
    
print("Done.")