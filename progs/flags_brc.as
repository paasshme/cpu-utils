LDI r1 0
LDI r2 200
ADD r2 255 r2
BRC .success
JMP 0
.success:
    LDI r1 128
