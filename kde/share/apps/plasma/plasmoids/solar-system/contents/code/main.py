# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *
from PyKDE4.kdecore import i18n
from PyKDE4.kio import *
from PyKDE4.solid import *


import datetime, sys, os, commands
import math
from configparameters import ConfigParameters


class HelloPython(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)
 

    def fnrad(self, x):
        x = x * 3.141592653589793 / 180
        return x
 

    def fndeg(self, x):
        x = x * 180 / 3.141592653589793
        return x;
 

    def fnrange(self, x):
        x = x - int(x / 360) * 360
        return x
 

    def fnsin(self, x):
        x = math.sin(x * 3.141592653589793/ 180)
        return x
 

    def fncos(self, x):
        x = math.cos(x * 3.141592653589793/ 180)
        return x
 

    def fntan(self, x):
        sx = math.sin(x* 3.141592653589793/180)
        cx = math.cos(x* 3.141592653589793/180)
        x = sx/cx
        return x
 

    def predeg(self, x):
        m = x / 360
        m1 = int(abs(m)) * 360
        m2 = abs(x) - m1
        if x < 0:  x = 0 - m2
        if x > 0:  x = m2
        return x
 

    def sgn(self, x):
        if x > 0: ax = 1
        if x == 0: ax = 0
        if x < 0: ax = -1
        return ax
 
    def addzero(self, x):
        x = str(x)
        if len(x) == 1:
           x = "0" + x
        return x
 

    def calcjd(self):

        nowis = datetime.datetime.utcnow()
        se = nowis.second
        mi = nowis.minute
        ho = nowis.hour
        da = nowis.day
        mo = nowis.month
        ye = nowis.year
        # we get days from 12/21 last year
        yelast = ye - 1
        today = datetime.date.today()
        zeroday = datetime.date(yelast, 12, 21)
        diff = today - zeroday
        ndays = diff.days
        if ndays > 365:
            ndays = ndays - 365
        self.numberdays = ndays
        self.txt = "UTC: "+self.addzero(ho)+":"+self.addzero(mi)+":"+self.addzero(se)+"  "+str(da)+"."+str(mo)+"."+str(ye)
        # calculate julian date
        tim = float(ho) + float(mi)/60 + float(se)/3600
        tim = tim / 24
        # protection for leap year
        if mo==1 | mo==2: 
            ye = ye - 1
            mo = mo + 12
        day = da + tim
        mor = mo
        yer = ye
        jd = 367 * yer
        yerd = 100 * yer
        jd = jd - int((7*(yer+int((mor+9)/12)))/4)
        jd = jd + int(275*mor/9)+day+1721013.45833 - 0.5*self.sgn(yerd+mor-190002.5) + 0.5
        return jd
 
    def iterate(self, M, e):
       # we will iterate at least 9 times to ensure fair precision
       E1=M+e*math.sin(M)
       E2=M+e*math.sin(E1)
       E3=M+e*math.sin(E2)
       E4=M+e*math.sin(E3)
       E5=M+e*math.sin(E4)
       E6=M+e*math.sin(E5)
       E7=M+e*math.sin(E6)
       E8=M+e*math.sin(E7)
       E9=M+e*math.sin(E8)
       return E9
 

    def calcposition(self):
        jds = self.calcjd()
        d = jds - 2415020
        pi = 3.14159265358979323846
        #px = 210 # center of solar system on canvas - X position, for canvasx = 420
        #py = 210 # center of solar system on canvas - Y position, for canvasy = 420
        d = jds - 2415020.0 # (number of days since the epoch)
        TT = d/36525 # (number of Julian centuries from the epoch)
        DD = 3.6525*TT
        DD2 = DD*DD
        TT2 = TT*TT
        sin_e = 0.397777156
        cos_e = 0.917482062
        sin_e = 1
        cos_e = 1
        # mercury
        i1 = 7.002881 + 0.0018608 * TT - 0.0000183 * TT2
        W1 = 47.14594 + 1.1852083 * TT + 0.0001739 * TT2
        p1 = 75.89970 + 1.5554889 * TT + 0.0002947 * TT2
        a1 = 0.3870986
        e1 = 0.20561421 + 0.00002046 * TT - 0.00000003 * TT2
        L1 = 178.179078 + 4.0923770233*d + 0.0000226 * DD2
        M1 = (L1 - p1)/57.2957796 # radians
        EE1 = self.iterate(M1, e1)  #radians
        EE1d = EE1 * 57.2957796  #degrees
        mi1 = 2 * math.atan(math.sqrt((1+e1)/(1-e1))*math.tan(math.radians(EE1d/2))) * 57.2957796 # degrees
        # Ecliptic longitude:
        LL1d = p1 + mi1  # degrees
        LL1 = math.radians(LL1d)
        # Ecliptic latitude:
        B1d = i1 * math.sin(math.radians(LL1d-W1)) # degrees [where i = orbital inclination]
        B1 = math.radians(B1d)
        #Radius vector (AUs):
        r1 = a1 * (1-e1 * math.cos(EE1)) # [where a = semi-major axis of orbit]
        # we will rather use our own values of radius vector
        r1 = 1
        #coef1 = 64.583
        #coef1 = 25
        # coef1 based on self.px
        coef1 = self.px / 8.4
        self.r1 = int(r1 * coef1)
        # Heliocentric equatorial rectangular coordinates (AUs):
        x1 = r1 * math.cos(LL1)*math.cos(B1)
        y1 = r1 * (math.sin(LL1) * math.cos(B1) * cos_e - sin_e * math.sin(B1))
        z1 = r1 * (sin_e * math.sin(LL1) * math.cos(B1) + cos_e * math.sin(B1))
        self.x1 = int(x1* coef1) + self.px
        self.y1 = self.py - int(y1* coef1)

        # venus
        i2 = 3.393631 + 0.0010058 * TT - 0.000001 * TT2
        W2 = 75.77965 + 0.899850 * TT + 0.000410 * TT2
        p2 = 130.16383 + 1.4080361 * TT - 0.0009764 * TT2
        a2 = 0.7233322
        e2 = 0.00682069 - 0.00004774 * TT + 0.000000091 * TT2
        L2 = 342.767053 + 1.6021687039 * d + 0.000023212 * DD2
        M2 = (L2 - p2)/57.2957796 # radians
        EE2 = self.iterate(M2, e2)  #radians
        EE2d = EE2 * 57.2957796  #degrees
        mi2 = 2 * math.atan(math.sqrt((1+e2)/(1-e2))*math.tan(math.radians(EE2d/2))) * 57.2957796 # degrees
        # Ecliptic longitude:
        LL2d = p2 + mi2  # degrees
        LL2 = math.radians(LL2d)
        # Ecliptic latitude:
        B2d = i2 * math.sin(math.radians(LL2d-W2)) # degrees [where i = orbital inclination]
        B2 = math.radians(B2d)
        e2r = math.radians(e2)
        #Radius vector (AUs):
        r2 = a2*(1-e2*math.cos(EE2)) # [where a = semi-major axis of orbit]
        r2 = 1
        #coef2 = 55.299
        #coef2 = 40
        # coef2 based on self.px
        coef2 = self.px / 5.25
        self.r2 = int(r2 * coef2)
        # Heliocentric equatorial rectangular coordinates (AUs):
        x2 = r2* math.cos(LL2) * math.cos(B2)
        y2 = r2* (math.sin(LL2) * math.cos(B2) * cos_e - sin_e * math.sin(B2))
        z2 = r2* (sin_e * math.sin(LL2) * math.cos(B2) + cos_e * math.sin(B2))
        self.x2 = int(x2 * coef2) + self.px
        self.y2 = self.py - int(y2 * coef2)

        # mars
        i4 = 1.850333 - 0.0006750 * TT + 0.0000126 * TT2
        W4 = 48.78644 + 0.7709917*TT - 0.0000014*TT2
        p4 = 334.21820 + 1.8407583*TT + 0.0001299*TT2
        a4 = 1.5236915
        e4 = 0.09331290 + 0.000092064 * TT - 0.000000077 * TT2
        L4 = 293.747628 + 0.5240711638 * d + 0.000023287 * DD2
        M4 = (L4 - p4)/57.2957796 # radians
        EE4 = self.iterate(M4, e4)  #radians
        EE4d = EE4 * 57.2957796  #degrees
        mi4 = 2 * math.atan(math.sqrt((1+e4)/(1-e4))*math.tan(math.radians(EE4d/2))) * 57.2957796 # degrees
        # Ecliptic longitude:
        LL4d = p4 + mi4  # degrees
        LL4 = math.radians(LL4d)
        # Ecliptic latitude:
        B4d = i4 * math.sin(math.radians(LL4d-W4)) # degrees [where i = orbital inclination]
        B4 = math.radians(B4d)
        e4r = math.radians(e4)
        #Radius vector (AUs):
        r4 = a4*(1-e4*math.cos(EE4)) # [where a = semi-major axis of orbit]
        r4 = 1
        #coef4 = 48
        coef4 = 77
        # coef4 based on self.px
        coef4 = self.px / 2.727272
        self.r4 = int(r4 * coef4 )
        # Heliocentric equatorial rectangular coordinates (AUs):
        x4 = r4* math.cos(LL4) * math.cos(B4)
        y4 = r4* (math.sin(LL4) * math.cos(B4) * cos_e - sin_e * math.sin(B4))
        z4 = r4* (sin_e * math.sin(LL4) * math.cos(B4) + cos_e * math.sin(B4))
        self.x4 = int(x4 * coef4) + self.px
        self.y4 = self.py - int(y4 * coef4)

        # jupiter
        i5 = 1.30875 - 0.00565 * TT
        W5 = 99.4378 + 1.0111 * TT
        p5 = 12.7114 + 1.6113 * TT
        a5 = 5.2028039
        e5 = 0.048338 + 0.000162 * TT
        L5 = 238.0495 + 3036.3028 * TT
        M5 = (L5 - p5)/57.2957796 # radians
        EE5 = self.iterate(M5, e5)  #radians
        EE5d = EE5 * 57.2957796  #degrees
        mi5 = 2 * math.atan(math.sqrt((1+e5)/(1-e5))*math.tan(math.radians(EE5d/2))) * 57.2957796 # degrees
        # Ecliptic longitude:
        LL5d = p5 + mi5  # degrees
        LL5 = math.radians(LL5d)
        # Ecliptic latitude:
        B5d = i5 * math.sin(math.radians(LL5d-W5)) # degrees [where i = orbital inclination]
        B5 = math.radians(B5d)
        #Radius vector (AUs):
        r5 = a5*(1-e5*math.cos(EE5)) # [where a = semi-major axis of orbit]
        r5 = 1
        #coef5 = 20.1
        #coef5 = 97
        #coef5 based on self.px
        coef5 = self.px / 2.16494845361
        self.r5 = int(r5 * coef5)
        # Heliocentric equatorial rectangular coordinates (AUs):
        x5 = r5* math.cos(LL5) * math.cos(B5)
        y5 = r5* (math.sin(LL5) * math.cos(B5) * cos_e - sin_e * math.sin(B5))
        z5 = r5* (sin_e * math.sin(LL5) * math.cos(B5) + cos_e * math.sin(B5))
        self.x5 = int(x5 * coef5) + self.px 
        self.y5 = self.py - int(y5 * coef5)

        # saturn
        i6 = 2.49238 - 0.0041 * TT
        W6 = 112.7837 + 0.8730 * TT
        p6 = 91.0888 + 1.9595 * TT
        a6 = 9.5388437
        e6 = 0.055890 - 0.000347 * TT
        L6 = 266.5652 + 1223.5103 * TT
        M6 = (L6 - p6)/57.2957796 # radians
        EE6 = self.iterate(M6, e6)  #radians
        EE6d = EE6 * 57.2957796  #degrees
        mi6 = 2 * math.atan(math.sqrt((1+e6)/(1-e6))*math.tan(math.radians(EE6d/2))) * 57.2957796 # degrees
        # Ecliptic longitude:
        LL6d = p6 + mi6  # degrees
        LL6 = math.radians(LL6d)
        # Ecliptic latitude:
        B6d = i6 * math.sin(math.radians(LL6d-W6)) # degrees [where i = orbital inclination]
        B6 = math.radians(B6d)
        #Radius vector (AUs):
        r6 = a6*(1-e6*math.cos(EE6)) # [where a = semi-major axis of orbit]
        r6 = 1
        #coef6 = 13.5
        #coef6 = 127
        #coef6 based on self.px
        coef6 = self.px / 1.65354330709
        self.r6 = int(r6 * coef6)
        # Heliocentric equatorial rectangular coordinates (AUs):
        x6 = r6* math.cos(LL6) * math.cos(B6)
        y6 = r6* (math.sin(LL6) * math.cos(B6) * cos_e - sin_e * math.sin(B6))
        z6 = r6* (sin_e * math.sin(LL6) * math.cos(B6) + cos_e * math.sin(B6))
        self.x6 = int(x6 * coef6) + self.px
        self.y6 = self.py - int(y6 * coef6)

        # uranus
        i7 = 0.77268 + 0.00063 * TT
        W7 = 73.4899 + 0.5106 * TT
        p7 = 169.035 + 1.627 * TT
        a7 = 19.18228 - 0.000565 * TT
        e7 = 0.047046 + 0.000272 * TT
        L7 = 243.3584 + 429.911 * TT
        M7 = (L7 - p7)/57.2957796 # radians
        EE7 = self.iterate(M7, e7)  #radians
        EE7d = EE7 * 57.2957796  #degrees
        mi7 = 2 * math.atan(math.sqrt((1+e7)/(1-e7))*math.tan(math.radians(EE7d/2))) * 57.2957796 # degrees
        # Ecliptic longitude:
        LL7d = p7 + mi7  # degrees
        LL7 = math.radians(LL7d)
        # Ecliptic latitude:
        B7d = i7 * math.sin(math.radians(LL7d-W7)) # degrees [where i = orbital inclination]
        B7 = math.radians(B7d)
        #Radius vector (AUs):
        r7 = a7*(1-e7*math.cos(EE7)) # [where a = semi-major axis of orbit]
        r7 = 1
        #coef7 = 8.34107
        #coef7 = 7.95
        #coef7 = 155
        #coef7 based on self.px
        coef7 = self.px / 1.35483870968
        self.r7 = int(r7 * coef7)
        # Heliocentric equatorial rectangular coordinates (AUs):
        x7 = r7* math.cos(LL7) * math.cos(B7)
        y7 = r7* (math.sin(LL7) * math.cos(B7) * cos_e - sin_e * math.sin(B7))
        z7 = r7* (sin_e * math.sin(LL7) * math.cos(B7) + cos_e * math.sin(B7))
        self.x7 = int(x7 * coef7) + self.px
        self.y7 = self.py - int(y7 * coef7)

        # neptune
        i8 = 1.77927 - 0.0092 * TT
        W8 = 130.6786 + 1.102 * TT
        p8 = 43.746 + 0.88 * TT
        a8 = 30.057053 + 0.001210 * TT
        e8 = 0.008528 + 0.0000785 * TT
        L8 = 85.0277 + 219.8553 * TT
        M8 = (L8 - p8)/57.2957796 # radians
        EE8 = self.iterate(M8, e8)  #radians
        EE8d = EE8 * 57.2957796  #degrees
        mi8 = 2 * math.atan(math.sqrt((1+e8)/(1-e8))*math.tan(math.radians(EE8d/2))) * 57.2957796 # degrees
        # Ecliptic longitude:
        LL8d = p8 + mi8  # degrees
        LL8 = math.radians(LL8d)
        # Ecliptic latitude:
        B8d = i8 * math.sin(math.radians(LL8d-W8)) # degrees [where i = orbital inclination]
        B8 = math.radians(B8d)
        #Radius vector (AUs):
        r8 = a8*(1-e8*math.cos(EE8)) # [where a = semi-major axis of orbit]
        r8 = 1
        #coef8 = 5.9886
        #coef8 = 6.3
        #coef8 = 175
        #coef8 based on self.px
        coef8 = self.px / 1.2
        self.r8 = int(r8 * coef8)
        # Heliocentric equatorial rectangular coordinates (AUs):
        x8 = r8* math.cos(LL8) * math.cos(B8)
        y8 = r8* (math.sin(LL8) * math.cos(B8) * cos_e - sin_e * math.sin(B8))
        z8 = r8* (sin_e * math.sin(LL8) * math.cos(B8) + cos_e * math.sin(B8))
        self.x8 = int(x8 * coef8) + self.px
        self.y8 = self.py - int(y8 * coef8)

        # pluto
        d = jds - 2451545.0 # (number of days since the epoch)
        TT = d/36525 # (number of Julian centuries from the epoch)
        DD = 3.6525*TT
        DD2 = DD*DD
        TT2 = TT*TT
        i9 = 17.14001206 + 0.00004818 * TT
        W9 = 110.30393684 - 0.01183482 * TT
        p9 = 224.06891629 - 0.04062942 * TT
        a9 = 39.48211675 - 0.00031596 * TT
        e9 = 0.24882730 + 0.00005170 * TT
        L9 = 238.92903833 + 145.20780515 * TT
        M9 = (L9 - p9)/57.2957796 # radians
        EE9 = self.iterate(M9, e9)  #radians
        EE9d = EE9 * 57.2957796  #degrees
        mi9 = 2 * math.atan(math.sqrt((1+e9)/(1-e9))*math.tan(math.radians(EE9d/2))) * 57.2957796 # degrees
        # Ecliptic longitude:
        LL9d = p9 + mi9  # degrees
        LL9 = math.radians(LL9d)
        # Ecliptic latitude:
        B9d = i9 * math.sin(math.radians(LL9d-W9)) # degrees [where i = orbital inclination]
        B9 = math.radians(B9d)
        #Radius vector (AUs):
        r9 = a9*(1-e9*math.cos(EE9)) # [where a = semi-major axis of orbit]
        # pluto's trajectory is very eccentric and it would look strange if it is closer to the sun than neptune,
        # that's why we set fake radius vector to 40 AU
        #r9 = 41.2
        #we rather use our own radius vector
        r9 = 1
        #coef9 = 5.0655
        #coef9 = 175
        #coef9 based on self.px
        coef9 = self.px / 1.2
        self.r9 = int(r9 * coef9)
        # Heliocentric equatorial rectangular coordinates (AUs):
        x9 = r9* math.cos(LL9) * math.cos(B9)
        y9 = r9* (math.sin(LL9) * math.cos(B9) * cos_e - sin_e * math.sin(B9))
        z9 = r9* (sin_e * math.sin(LL9) * math.cos(B9) + cos_e * math.sin(B9))
        self.x9 = int(x9 * coef9) + self.px
        self.y9 = self.py - int(y9 * coef9)

        # earth, we compute it differently
        angle = 2 * pi * float(self.numberdays)/365 + pi/2 # degrees
        x3 = math.cos(angle);
        y3 = math.sin(angle);
        #coef3 = 60
        # coef3 based on self.px
        coef3 = self.px / 3.5
        self.r3 = coef3
        self.x3 = int(x3 * coef3) + self.px
        self.y3 = self.py - int(y3 * coef3)
 

    def init(self):
        self.setHasConfigurationInterface(True)
        self.appName = "solar-system"
        vers = {}
        vers["fr"] = "0.4.1"
        vers["ru"] = "0.4.1"
        vers["el"] = "0.4.1"
        vers["es"] = "0.4.1"
        vers["sk"] = "0.4.1"
        vers["it"] = "0.4.1"
        vers["cs"] = "0.4.1"
        vers["de"] = "0.4.1"

        self._settings = {}
        self.InitSettings()

        # Setup translations
        kdehome = unicode(KGlobal.dirs().localkdedir())
        self.installTranslation(vers, unicode(KGlobal.locale().language()), kdehome)
        KGlobal.locale().insertCatalog("solar-system")

        # load settings
        self.showOrbits = self._settings["showOrbits"]
        self.showLegend = self._settings["showLegend"]
        self.showPluto = self._settings["showPluto"]
        self.textcolor = self._settings["textcolor"]
        self.orbitcolor = self._settings["orbitcolor"]
        #self.mysize = self._settings["mysize"]
        self.mysize = int(self.applet.geometry().width())
        # center of solar system on canvas - X position, for canvasx = 420
        self.px = self.mysize / 2
        # center of solar system on canvas - Y position, for canvasy = 420
        self.py = self.mysize / 2
        # calculate positions
        self.calcposition()

        self.setAspectRatioMode(Plasma.KeepAspectRatio)
        self.theme = Plasma.Svg(self)
        self.setBackgroundHints(Plasma.Applet.NoBackground)
        # load all images
        self.suns = QImage(self)
        self.mercurys = QImage(self)
        self.venuss = QImage(self)
        self.earths = QImage(self)
        self.marss = QImage(self)
        self.jupiters = QImage(self)
        self.saturns = QImage(self)
        self.uranuss = QImage(self)
        self.neptunes = QImage(self)
        self.plutos = QImage(self)
        self.sun = QImage(self)
        self.mercury = QImage(self)
        self.venus = QImage(self)
        self.earth = QImage(self)
        self.mars = QImage(self)
        self.jupiter = QImage(self)
        self.saturn = QImage(self)
        self.uranus = QImage(self)
        self.neptune = QImage(self)
        self.pluto = QImage(self)
        # load small images
        self.suns.load(self.package().path()+"contents/images/sun_s.png")
        self.mercurys.load(self.package().path()+"contents/images/mercury_s.png")
        self.venuss.load(self.package().path()+"contents/images/venus_s.png")
        self.earths.load(self.package().path()+"contents/images/earth_s.png")
        self.marss.load(self.package().path()+"contents/images/mars_s.png")
        self.jupiters.load(self.package().path()+"contents/images/jupiter_s.png")
        self.saturns.load(self.package().path()+"contents/images/saturn_s.png")
        self.uranuss.load(self.package().path()+"contents/images/uranus_s.png")
        self.neptunes.load(self.package().path()+"contents/images/neptune_s.png")
        self.plutos.load(self.package().path()+"contents/images/pluto_s.png")
        # load normal images
        self.sun.load(self.package().path()+"contents/images/sun.png")
        self.mercury.load(self.package().path()+"contents/images/mercury.png")
        self.venus.load(self.package().path()+"contents/images/venus.png")
        self.earth.load(self.package().path()+"contents/images/earth.png")
        self.mars.load(self.package().path()+"contents/images/mars.png")
        self.jupiter.load(self.package().path()+"contents/images/jupiter.png")
        self.saturn.load(self.package().path()+"contents/images/saturn.png")
        self.uranus.load(self.package().path()+"contents/images/uranus.png")
        self.neptune.load(self.package().path()+"contents/images/neptune.png")
        self.pluto.load(self.package().path()+"contents/images/pluto.png")

        #self.resize(self.px*2, self.py*2)
        #no timer necessary, planets move slowly
        #self.startTimer(60000)
 

    def timerEvent(self,event):
        self.update()
 

    def paintInterface(self, painter, option, rect):
        painter.save()
        self.mysize = int(self.applet.geometry().width())
        # center of solar system on canvas - X position, for canvasx = 420
        self.px = self.mysize / 2
        # center of solar system on canvas - Y position, for canvasy = 420
        self.py = self.mysize / 2
        # calculate positions
        self.calcposition()
        # define fonts for legend 
        classic_legendfont = QFont("Sans Serif", 7)
        # let us paint orbits
        if self.showOrbits == "true":
            painter.setPen(QColor(self.orbitcolor))
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.drawEllipse(self.px-self.r1, self.py-self.r1, 2*self.r1, 2*self.r1)
            painter.drawEllipse(self.px-self.r2, self.py-self.r2, 2*self.r2, 2*self.r2)
            painter.drawEllipse(self.px-self.r3, self.py-self.r3, 2*self.r3, 2*self.r3)
            painter.drawEllipse(self.px-self.r4, self.py-self.r4, 2*self.r4, 2*self.r4)
            painter.drawEllipse(self.px-self.r5, self.py-self.r5, 2*self.r5, 2*self.r5)
            painter.drawEllipse(self.px-self.r6, self.py-self.r6, 2*self.r6, 2*self.r6)
            painter.drawEllipse(self.px-self.r7, self.py-self.r7, 2*self.r7, 2*self.r7)
            #painter.drawEllipse(self.px-self.r8, self.py-self.r8, 2*self.r8, 2*self.r8)
            #painter.drawEllipse(self.px-self.r9, self.py-self.r9, 2*self.r9, 2*self.r9)
            centre=QPointF(self.px,self.py)
            # because of eccentricity of neptune and pluto we calculate the circle from their apparent position
            # it's safer than to rely on radius
            r8s = math.sqrt((self.x8-self.px)*(self.x8-self.px) + (self.y8-self.py)*(self.y8-self.py))
            painter.drawEllipse(centre, r8s, r8s)
            if self.showPluto == "true":
               r9s = math.sqrt((self.x9-self.px)*(self.x9-self.px) + (self.y9-self.py)*(self.y9-self.py))
               painter.drawEllipse(centre, r9s, r9s)

        # paint sun and planets
        if (self.px<150):
            painter.drawImage(self.px-5,self.px-5, self.suns)
            painter.drawImage(self.x1 - 2, self.y1 - 2, self.mercurys)
            painter.drawImage(self.x2 - 2, self.y2 - 2, self.venuss)
            painter.drawImage(self.x3 - 2, self.y3 - 2, self.earths)
            painter.drawImage(self.x4 - 2, self.y4 - 2, self.marss)
            painter.drawImage(self.x5 - 4, self.y5 - 4, self.jupiters)
            painter.drawImage(self.x6 - 5, self.y6 - 2, self.saturns)
            painter.drawImage(self.x7 - 3, self.y7 - 3, self.uranuss)
            painter.drawImage(self.x8 - 3, self.y8 - 3, self.neptunes)
            if self.showPluto == "true":
                painter.drawImage(self.x9 - 2, self.y9 - 2, self.plutos)
        else:
            painter.drawImage(self.px-14,self.px-14, self.sun)
            painter.drawImage(self.x1 - 5, self.y1 - 5, self.mercury)
            painter.drawImage(self.x2 - 7, self.y2 - 7, self.venus)
            painter.drawImage(self.x3 - 7, self.y3 - 7, self.earth)
            painter.drawImage(self.x4 - 6, self.y4 - 6, self.mars)
            painter.drawImage(self.x5 - 12, self.y5 - 11, self.jupiter)
            painter.drawImage(self.x6 - 17, self.y6 - 7, self.saturn)
            painter.drawImage(self.x7 - 8, self.y7 - 8, self.uranus)
            painter.drawImage(self.x8 - 8, self.y8 - 8, self.neptune)
            if self.showPluto == "true":
                painter.drawImage(self.x9 - 5, self.y9 - 5, self.pluto)

        # draw legend if enabled
        if self.showLegend == "true":
            painter.setPen(QColor(self.textcolor))
            painter.setFont(classic_legendfont)
            painter.drawText(self.px-20, self.py-20, 40, 40, Qt.AlignCenter, i18nc("Name of the star at the center of Solar System", "Sun"))
            #painter.drawText(self.px-8, self.py-7, self.px+10, self.py+2, Qt.TextWordWrap, i18n("Sun"))
            painter.drawText(self.x1 - 25, self.y1-18, 50, 20, Qt.AlignHCenter, i18n("Mercury"))
            painter.drawText(self.x2 - 25, self.y2-19, 50, 20, Qt.AlignHCenter, i18n("Venus"))
            painter.drawText(self.x3 - 25, self.y3-19, 50, 20, Qt.AlignHCenter, i18n("Earth"))
            painter.drawText(self.x4 - 25, self.y4-19, 50, 20, Qt.AlignHCenter, i18n("Mars"))
            painter.drawText(self.x5 - 25, self.y5-25, 50, 20, Qt.AlignHCenter, i18n("Jupiter"))
            painter.drawText(self.x6 - 25, self.y6-20, 50, 20, Qt.AlignHCenter, i18n("Saturn"))
            painter.drawText(self.x7 - 25, self.y7-20, 50, 20, Qt.AlignHCenter, i18n("Uranus"))
            painter.drawText(self.x8 - 25, self.y8-20, 50, 20, Qt.AlignHCenter, i18n("Neptune"))
            if self.showPluto == "true":
                painter.drawText(self.x9 - 25, self.y9-18, 50, 20, Qt.AlignHCenter, i18n("Pluto"))
        painter.restore()
 

    def InitSettings(self):
        # Setup configuration
        self.gc = self.config()
        self._settings["showOrbits"] = self.gc.readEntry("showOrbits", "true").toString()
        self._settings["showLegend"] = self.gc.readEntry("showLegend", "false").toString()
        self._settings["showPluto"] = self.gc.readEntry("showPluto", "false").toString()
        self._settings["textcolor"] = self.gc.readEntry("textcolor", "#141414").toString()
        self._settings["orbitcolor"] = self.gc.readEntry("orbitcolor", "#A0A0A0").toString()
        #self._settings["mysize"] = self.gc.readEntry("mysize", "210").toString()


    # ---------- Configuration ----------
    def createConfigurationInterface(self, parent):
        self.configParameters = ConfigParameters(self,  self._settings)
        page = parent.addPage(self.configParameters, i18n("Configure Me"))
        page.setIcon(KIcon("preferences-other"))
        self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
        self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)

    # setup and show configuration dialog (called by plasma)
    def showConfigurationInterface(self):
        self.dialog = KPageDialog()
        self.dialog.setFaceType(KPageDialog.List)
        self.dialog.setButtons(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel))
        self.createConfigurationInterface(self.dialog)
        self.dialog.exec_()

    # configuration done (ok-button)
    def configAccepted(self):
        newSettings = {}
        self.configParameters.updateSettings(newSettings)
        self._settings = newSettings
        # save settings to kde-configuration
        self.gc.writeEntry("showOrbits", self._settings["showOrbits"] )
        self.gc.writeEntry("showLegend", self._settings["showLegend"] )
        self.gc.writeEntry("showPluto", self._settings["showPluto"] )
        self.gc.writeEntry("textcolor", self._settings["textcolor"] )
        self.gc.writeEntry("orbitcolor", self._settings["orbitcolor"] )
        #self.gc.writeEntry("mysize", self._settings["mysize"] )
        self.gc.sync()

        self._settings["showOrbits"] = newSettings["showOrbits"]
        self._settings["showLegend"] = newSettings["showLegend"]
        self._settings["showPluto"] = newSettings["showPluto"]
        self._settings["textcolor"] = newSettings["textcolor"]
        self._settings["orbitcolor"] = newSettings["orbitcolor"]
        #self._settings["mysize"] = newSettings["mysize"]

        self.configParameters.deleteLater()
        self.dialog.accept()

        self.showOrbits = self._settings["showOrbits"]
        self.showLegend = self._settings["showLegend"]
        self.showPluto = self._settings["showPluto"]
        self.textcolor = self._settings["textcolor"]
        self.orbitcolor = self._settings["orbitcolor"]
        #self.mysize = self._settings["mysize"]
        self.update()
 
    # configuration canceled
    def configDenied(self):
        self.configParameters.deleteLater()
        self.dialog.reject()
 
    def fixType(self, val):
        # FIXME: This is needed to take care of problems with KDE 4.3 bindings, but it should be removed
        # when things are fixed.
        if type(val) == QVariant:
            return str(val.toString())
        else:
            return val
 
    def createDirectory(self, d):
        if not os.path.isdir(d):
            try:
                os.mkdir(d)
            except:
                print "Problem creating directory: "+d
                print "Unexpected error:", sys.exc_info()[0]
 
    def writetolog(self, message):
        msg = "echo \""+message+"\" >>"+self.package().path()+"/solar-system.log"
        #cmds = str(msg)
        #outs = commands.getstatusoutput(cmds)
 
    def installTranslation(self, trans, lang, kdehome):
        if lang == "en_US":
            pass
        elif trans.has_key(lang):
            # Setup error message for each translation
            # This is hard coded so that a translated message is displayed even if the translation has not installed.
            transerror = {}
            transerror["default"] = "There was a problem installing a translation. Installing the translation requires the 'msgfmt' command, which is included in the 'gettext' package.\n\nPlease ensure that the 'gettext' package is installed."
            transerror["fr"] = "Il y a eu un problème lors de l'installation de la traduction française. L'installation de la traduction nécessite la commande 'msgfmt', qui est incluse dans le paquet 'gettext'\n\nVeuillez veiller à ce que le paquet 'gettext' soit installé"
            transerror["ru"] = "Не удалось установить русский перевод для виджета. Для установки требуется команда 'msgfmt' из пакета 'gettext'.\n\nПожалуйста, убедитесь, что пакет 'gettext' установлен."
            transerror["el"] = "Υπήρχε ένα πρόβλημα με την εγκατάσταση της Ελληνικής μετάφρασης για. Η εγκατάσταση της μετάφρασης χρειάζεται την εντολή 'msgfmt', που συμπεριλαμβάνετε στο πακέτο 'gettext'.\n\nΠαρακαλώ ελέγξτε εάν το πακέτο 'gettext' είναι εγκατεστημένο."
            transerror["es"] = "Hubo un problema instalando la traducción al español, pues se requiere el programa \"msgfmt\", incluido en el paquete \"gettext\".\n\nPor favor, asegúrese de que dicho paquete está instalado."
            transerror["it"] = "Si è verificato un errore nell'installazione della traduzione italiana del widget solar-system. Per installare la traduzione è necessario il comando 'msgfmt' contenuto nel pacchetto 'gettext'.\n\nVerifica che il pacchetto 'gettext' sia installato."
            transerror["sk"] = "Vyskytol sa problém pri inštalácii slovenského prekladu. Inštalácia prekladu vyžaduje príkaz 'msgfmt', ktorý sa nachádza v balíku 'gettext'.\n\n Prosím uistite sa, že balík 'gettext' je nainštalovaný."
            transerror["cs"] = "Vyskytl se problém při instalaci českého překladu pro solar-system widget. Instalace překladu vyžaduje příkaz 'msgfmt', který je obsažen v balíku 'gettext'.\n\n Prosím ujistěte se, že balík 'gettext' je nainstalován."
            transerror["de"] = "Während der Installation der deutschen Übersetzung für das Widget solar-system ist ein Problem aufgetreten. Die Installation erfordert den Befehl 'msgfmt', welcher im Paket 'gettext' enthalten ist.\n\nStellen Sie bitte sicher, daß das 'gettext'-Paket installiert ist."
            
            # Check if file already exists
            gc = self.config()
            if not os.path.exists(kdehome+"share/locale/"+lang+"/LC_MESSAGES/solar-system.mo"):
                msg = "Installing "+lang+" translations..."
                print msg
                self.writetolog(msg)
                # Create required directories
                self.createDirectory(kdehome+"share/locale")
                self.createDirectory(kdehome+"share/locale/"+lang)
                self.createDirectory(kdehome+"share/locale/"+lang+"/LC_MESSAGES")
                
                # Create .mo file (requires gettext package)
                cmd = unicode("msgfmt -f -o "+kdehome+"share/locale/"+lang+"/LC_MESSAGES/solar-system.mo"+" "+self.package().path()+"contents/code/i18n/"+lang+"/solar-system.po")
                self.writetolog(cmd)
                print "Command:", cmd
                out = commands.getstatusoutput(cmd)        
                if out[0] == 0:
                    msg = "Translation installed."
                    print msg
                    self.writetolog(msg+" "+lang)
                    gc.writeEntry("trans-"+lang, trans[lang])
                else:
                    msg = "Error installing translation: "+out
                    print msg
                    self.writetolog(msg)
                    if transerror.has_key(lang):
                        KMessageBox.informationWId(0, transerror[lang], "Error", "solar-system-translation-error")
                    else:
                        KMessageBox.informationWId(0, transerror["default"], "Error", "solar-system-translation-error")
            else:
                # Update the file version does not match
                ver = self.fixType(gc.readEntry("trans-"+lang, "0"))
                if ver <> trans[lang]:
                    msg = "Updating "+lang+" translation..."
                    print msg
                    self.writetolog(msg)
                    # Create .mo file (requires gettext package)
                    cmd = unicode("msgfmt -f -o "+kdehome+"share/locale/"+lang+"/LC_MESSAGES/solar-system.mo"+" "+self.package().path()+"contents/code/i18n/"+lang+"/solar-system.po")
                    self.writetolog(cmd)
                    print "Command:", cmd
                    out = commands.getstatusoutput(cmd)
                    if out[0] == 0:
                        msg = "Translation updated: "+lang
                        print msg
                        self.writetolog(msg)
                        gc.writeEntry("trans-"+lang, trans[lang])
                    else:
                        msg = "Error updating translation:"+out
                        print msg
                        self.writetolog(msg)
                        if transerror.has_key(lang):
                            KMessageBox.informationWId(0, transerror[lang], "Error", "solar-system-translation-error")
                        else:
                            KMessageBox.informationWId(0, transerror["default"], "Error", "solar-system-translation-error")
                else:
                    self.writetolog("Translation "+lang+" up to date.")
        else:
            msg = "No "+lang+" translations exist."
            print msg
            self.writetolog(msg)
 

def CreateApplet(parent):
   return HelloPython(parent)
 
