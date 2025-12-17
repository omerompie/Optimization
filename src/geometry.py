# src/geometry.py

"""
Geodesy utilities: distance and bearing on WGS-84.
Wraps the provided Vincenty implementations.
"""

from math import atan2, cos, radians, sin, sqrt, degrees


def v_direct(coord1, coord2, maxIter=200, tol=10**-12):
    """
    Vincenty inverse: distance and initial bearing from coord1 to coord2.

    coord1, coord2: (lat_deg, lon_deg)
    Returns:
        distance_m (float), bearing_deg (float)
    """
    if coord1 == coord2:
        return 0.0, 0.0

    a = 6378137.0
    f = 1 / 298.257223563
    b = (1 - f) * a

    phi_1, L_1 = coord1
    phi_2, L_2 = coord2

    from math import atan, tan, pi

    u_1 = atan((1 - f) * tan(radians(phi_1)))
    u_2 = atan((1 - f) * tan(radians(phi_2)))

    L = radians(L_2 - L_1)
    Lambda = L

    sin_u1 = sin(u_1)
    cos_u1 = cos(u_1)
    sin_u2 = sin(u_2)
    cos_u2 = cos(u_2)

    iters = 0
    for _ in range(maxIter):
        iters += 1
        cos_lambda = cos(Lambda)
        sin_lambda = sin(Lambda)
        sin_sigma = sqrt(
            (cos_u2 * sin_lambda) ** 2
            + (cos_u1 * sin_u2 - sin_u1 * cos_u2 * cos_lambda) ** 2
        )
        cos_sigma = sin_u1 * sin_u2 + cos_u1 * cos_u2 * cos_lambda
        sigma = atan2(sin_sigma, cos_sigma)
        sin_alpha = (cos_u1 * cos_u2 * sin_lambda) / sin_sigma
        cos_sq_alpha = 1 - sin_alpha**2
        cos2_sigma_m = cos_sigma - (2 * sin_u1 * sin_u2) / cos_sq_alpha
        C = (f / 16) * cos_sq_alpha * (4 + f * (4 - 3 * cos_sq_alpha))
        Lambda_prev = Lambda
        Lambda = L + (1 - C) * f * sin_alpha * (
            sigma
            + C
            * sin_sigma
            * (cos2_sigma_m + C * cos_sigma * (-1 + 2 * cos2_sigma_m**2))
        )
        if abs(Lambda - Lambda_prev) <= tol:
            break

    u_sq = cos_sq_alpha * ((a**2 - b**2) / b**2)
    A = 1 + (u_sq / 16384) * (4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq)))
    B = (u_sq / 1024) * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))
    delta_sig = (
        B
        * sin_sigma
        * (
            cos2_sigma_m
            + 0.25
            * B
            * (
                cos_sigma * (-1 + 2 * cos2_sigma_m**2)
                - (B / 6)
                * cos2_sigma_m
                * (-3 + 4 * sin_sigma**2)
                * (-3 + 4 * cos2_sigma_m**2)
            )
        )
    )

    distance_m = b * A * (sigma - delta_sig)

    y_amm = cos_u2 * sin_lambda
    x_amm = cos_u1 * sin_u2 - sin_u1 * cos_u2 * cos_lambda
    alpha1_amm = atan2(y_amm, x_amm)
    if alpha1_amm < 0:
        alpha1_amm = alpha1_amm + 2 * pi
    bearing_deg = degrees(alpha1_amm)

    return distance_m, bearing_deg


def v_inverse(lat1, lon1, az12, s):
    """
    Vincenty direct: endpoint given start, azimuth, and distance.

    lat1, lon1: degrees
    az12: forward azimuth in degrees
    s: distance in meters
    Returns:
        lat2_deg, lon2_deg
    """
    from math import pi, tan, atan, acos

    d2r = 180 / pi
    twopi = 2 * pi
    a = 6378137
    flat = 298.257222101

    f = 1 / flat
    b = a * (1 - f)
    e2 = f * (2 - f)
    ep2 = e2 / (1 - e2)

    phi1 = lat1 / d2r
    lambda1 = lon1 / d2r

    alpha1 = az12 / d2r
    from math import sin as msin, cos as mcos

    sin_alpha1 = msin(alpha1)
    cos_alpha1 = mcos(alpha1)

    psi1 = atan((1 - f) * tan(phi1))
    psi0 = acos(mcos(psi1) * sin_alpha1)
    u2 = ep2 * (msin(psi0) ** 2)
    sigma1 = atan((tan(psi1)) / cos_alpha1)
    sin_alphaE = mcos(psi0)
    A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    sigma = s / (b * A)

    while True:
        two_sigma_m = 2 * sigma1 + sigma
        s1 = msin(sigma)
        c1 = mcos(sigma)
        c1_2m = mcos(two_sigma_m)
        c2_2m = c1_2m * c1_2m
        t1 = 2 * c2_2m - 1
        t2 = -3 + 4 * s1 * s1
        t3 = -3 + 4 * c2_2m
        delta_sigma = B * s1 * (
            c1_2m + B / 4 * (c1 * t1 - B / 6 * c1_2m * t2 * t3)
        )
        sigma_new = s / (b * A) + delta_sigma
        if abs(sigma_new - sigma) < 1e-12:
            break
        sigma = sigma_new

    s1 = msin(sigma)
    c1 = mcos(sigma)
    y = msin(psi1) * c1 + mcos(psi1) * s1 * cos_alpha1
    x = (1 - f) * sqrt(
        sin_alphaE**2
        + (msin(psi1) * s1 - mcos(psi1) * c1 * cos_alpha1) ** 2
    )
    phi2 = atan2(y, x)
    lat2 = phi2 * d2r

    y = s1 * sin_alpha1
    x = mcos(psi1) * c1 - msin(psi1) * s1 * cos_alpha1
    domega = atan2(y, x)

    x = 1 - sin_alphaE**2
    C = f / 16 * x * (4 + f * (4 - 3 * x))
    two_sigma_m = 2 * sigma1 + sigma
    c1_2m = mcos(two_sigma_m)
    c2_2m = c1_2m * c1_2m
    dlambda = domega - (1 - C) * f * sin_alphaE * (
        sigma + C * s1 * (c1_2m + C * c1 * (-1 + 2 * c2_2m))
    )
    dlon = dlambda * d2r
    lon2 = lon1 + dlon

    return lat2, lon2


def distance_and_bearing(coord1, coord2):
    """Wrapper for clarity."""
    return v_direct(coord1, coord2)


