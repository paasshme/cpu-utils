// clear result reg
LDI r5 0
LDI r6 0
LDI r7 0
// Store and read Mem[r1 + 0] = 64
LDI r1 1
LDI r2 64
LDI r3 32
LDI r4 16
ST r1 r2 0
ST r1 r3 1
ST r1 r4 2
LB r1 r5 0
LB r1 r6 1
LB r1 r7 2