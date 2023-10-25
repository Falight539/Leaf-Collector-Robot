def pid_forward(l: tuple, r: tuple, Max_speed: int, p: float, i: float, d: float) -> [tuple, tuple]:

    pid = p + i + d

    L_speed = (l[0]*l[1]) + pid
    R_speed = (r[0]*r[1]) - pid

    L_dir = 1
    R_dir = 1

    if L_speed < 0:
        L_dir = -1
    L_speed = abs(L_speed) if abs(L_speed) <= Max_speed else Max_speed

    if R_speed < 0:
        R_dir = -1
    R_speed = abs(R_speed) if abs(R_speed) <= Max_speed else Max_speed

    return (L_speed, L_dir), (R_speed, R_dir)

