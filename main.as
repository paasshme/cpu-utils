.init:   
    LDI r1 0
    LDI r2 0
    LDI r4 0
    LDI r3 0
    ADI r2 64
    ADD r1 r0 r3
    ADI r1 1
    # Store m[2] = 64
.ram:    
    ST r1 r2 1
    ADI r2 10
    # Store m[9] = 74
    ST r1 r2 8
.load:
    LB r1 r3 1
    LB r1 r4 8
    JMP .init