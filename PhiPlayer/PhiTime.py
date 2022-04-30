def phiToSecond(phiTime, bpm):
    return (phiTime) / 32 * (60/bpm)


def secondToPhi(RTime, bpm):
    return RTime / (60 / bpm) * 32
