LDI r5 5
LDI r1 0
.loop:
    CALL .fun
    ADI r5 255
    BRNZ .loop
HALT
.fun:
    ADD r1 r5 r1
    RET