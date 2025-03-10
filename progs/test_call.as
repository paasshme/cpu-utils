    LDI r1 1
    LDI r2 2
.start:
    CALL .fun
    HALT
    NOP
    NOP
.fun:
    ADI r1 2
    RET