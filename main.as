    LDI r1 2
.start:
    CALL 8
    ADI r1 1
    CALL .fun
    # le commetaire
    // et oui
    HALT
    NOP
    NOP
    NOP
.fun:
    ADI r1 2
    JMP .start
    BRC .fun
    BRNC .start
    RET