LDI r1 0
ADD r0 r0 r0
BRNC .success
HALT
.success:
    LDI r1 128
