#!/usr/bin/env python3
"""Compute sensitivity analysis for AI Platform Selection Scorecard."""

opt1 = {"F01":5,"F02":5,"F03":4,"F04":2,"F05":5,"F06":5,"F07":3,"F08":4,"F09":3,"F10":4,"F11":5,"F12":4}
opt2 = {"F01":3,"F02":3,"F03":4,"F04":4,"F05":5,"F06":5,"F07":4,"F08":4,"F09":5,"F10":4,"F11":3,"F12":4}
opt3 = {"F01":1,"F02":1,"F03":3,"F04":5,"F05":2,"F06":2,"F07":5,"F08":3,"F09":5,"F10":2,"F11":1,"F12":3}

base_w = {"F01":15,"F02":10,"F03":20,"F04":8,"F05":12,"F06":10,"F07":8,"F08":5,"F09":5,"F10":3,"F11":2,"F12":2}

def wscore(opt, w):
    return sum(opt[f] * w[f] / 100 for f in opt)

print("=== BASE ===")
print(f"Opt1: {wscore(opt1,base_w):.2f}  Opt2: {wscore(opt2,base_w):.2f}  Opt3: {wscore(opt3,base_w):.2f}")
print(f"Gap 1v2: {wscore(opt1,base_w)-wscore(opt2,base_w):.2f}")

# S1: Enterprise data matters more
s1_w = dict(base_w)
s1_w["F04"] = 18
s1_w["F01"] = 10
s1_w["F02"] = 5
print(f"\n=== S1: Enterprise data +10% (F04=18, F01=10, F02=5) ===")
print(f"Opt1: {wscore(opt1,s1_w):.2f}  Opt2: {wscore(opt2,s1_w):.2f}  Opt3: {wscore(opt3,s1_w):.2f}")
print(f"Gap 1v2: {wscore(opt1,s1_w)-wscore(opt2,s1_w):.2f}")
print(f"Flip? {'YES' if wscore(opt2,s1_w) > wscore(opt1,s1_w) else 'NO'}")

# S2: Cost matters less
s2_w = dict(base_w)
s2_w["F01"] = 5
s2_w["F07"] = 13
s2_w["F09"] = 10
print(f"\n=== S2: Cost -10% (F01=5, F07=13, F09=10) ===")
print(f"Opt1: {wscore(opt1,s2_w):.2f}  Opt2: {wscore(opt2,s2_w):.2f}  Opt3: {wscore(opt3,s2_w):.2f}")
print(f"Gap 1v2: {wscore(opt1,s2_w)-wscore(opt2,s2_w):.2f}")
print(f"Flip? {'YES' if wscore(opt2,s2_w) > wscore(opt1,s2_w) else 'NO'}")
print(f"Opt3 competitive (>3.5)? {'YES' if wscore(opt3,s2_w) > 3.5 else 'NO'}")

# S3: Option 3 quality improves to 4
s3_opt3 = dict(opt3)
s3_opt3["F03"] = 4
print(f"\n=== S3: Opt3 quality=4 ===")
print(f"Opt1: {wscore(opt1,base_w):.2f}  Opt2: {wscore(opt2,base_w):.2f}  Opt3: {wscore(s3_opt3,base_w):.2f}")
print(f"Opt3 change: {wscore(opt3,base_w):.2f} -> {wscore(s3_opt3,base_w):.2f}")

# S4: Copilot pricing change
s4_opt1 = dict(opt1)
s4_opt1["F01"] = 3
print(f"\n=== S4: Copilot pricing (Opt1 F01=3) ===")
print(f"Opt1: {wscore(s4_opt1,base_w):.2f}  Opt2: {wscore(opt2,base_w):.2f}  Opt3: {wscore(opt3,base_w):.2f}")
print(f"Gap 1v2: {wscore(s4_opt1,base_w)-wscore(opt2,base_w):.2f}")
print(f"Flip? {'YES' if wscore(opt2,base_w) > wscore(s4_opt1,base_w) else 'NO'}")

# S5: Combined worst case
print(f"\n=== S5: Combined (S1+S4) ===")
print(f"Opt1: {wscore(s4_opt1,s1_w):.2f}  Opt2: {wscore(opt2,s1_w):.2f}  Opt3: {wscore(opt3,s1_w):.2f}")
print(f"Gap 1v2: {wscore(s4_opt1,s1_w)-wscore(opt2,s1_w):.2f}")
print(f"Flip? {'YES' if wscore(opt2,s1_w) > wscore(s4_opt1,s1_w) else 'NO'}")
