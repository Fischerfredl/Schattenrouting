import numpy as np
from datetime import datetime


def get_solar_position(date):
    month, day, hour, minute = (date.month, date.day, date.hour, date.minute)

    lat, lon = (52.51, 13.41)
    const = np.pi/180.

    # Tageszahl

    t = int(date.strftime('%j'))
    # Jahresteil

    n = (t-1+(hour-12+minute/60.)/24.)/365.

    # Deklination
    decl = (0.006918
            - 0.399912 * np.cos(2*np.pi*n)
            + 0.070257 * np.sin(2*np.pi*n)
            - 0.006758 * np.cos(4*np.pi*n)
            + 0.000907 * np.sin(4*np.pi*n)
            - 0.002697 * np.cos(6*np.pi*n)
            + 0.00148 * np.sin(6*np.pi*n)) / const

    # Zeitgleichung
    zgl = 229.18 * (0.000075
                    + 0.001868 * np.cos(2*np.pi*n)
                    - 0.032077 * np.sin(2*np.pi*n)
                    - 0.014615 * np.cos(4*np.pi*n)
                    - 0.040849 * np.sin(4*np.pi*n))

    # Stundenwinkel
    stundenwinkel = 15 * (hour + minute/60. - (15.0 - lon)/15.0 - 12 + zgl/60.)

    x = np.sin(const*lat) * np.sin(const*decl) + \
        np.cos(const*lat) * np.cos(const*decl) * np.cos(const*stundenwinkel)

    elev = np.arcsin(x)/const

    y = -(np.sin(const*lat) * np.sin(const*elev) - np.sin(const*decl)) / \
        (np.cos(const*lat) * np.sin(np.arccos(np.sin(const*elev))))

    azimut = np.arccos(y)/const

    '''
    print 'Monat: ' + str(month)
    print 'Tag: ' + str(day)
    print 'Hour: ' + str(hour)
    print 'Minute: ' + str(minute)
    print 'Tageszahl: ' + str(t)
    print 'Jahresteil: ' + str(n)
    print 'Deklination: ' + str(decl)
    print 'Zeitgleichung: ' + str(zgl)
    print 'Stundenwinkel: ' + str(stundenwinkel)
    print 'Elevation: ' + str(elev)
    print 'Azimut: ' + str(azimut)
    '''
    return azimut, elev



