def exposure_quality(exposure_raw):

    # symetryczna funkcja wokół 0.5

    quality = 1 - 2 * abs(
        exposure_raw - 0.5
    )

    if quality < 0:
        quality = 0.0

    return quality