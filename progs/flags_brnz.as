LDI r1 0
ADD r0 r0 r0
BRNZ .failure
LDI r1 128
.failure:
HALT