# coding=utf-8           # -*- coding: utf-8 -*-
#!/usr/bin/env python
""" generated source for module WGS84_SK42_Translator """
import math
import numpy as np
#
#
# resource from www.gis-lab.info
# http://gis-lab.info/qa/wgs84-sk42-wgs84-formula.html
# http://gis-lab.info/qa/datum-transform-methods.html
# @author Raven
#
class Translator(object):
    """ generated source for class WGS84_SK42_Translator """

    #
    # convert from WGS-84 to SK-42.
    # @param Bd longitude
    # @param Ld latitude
    # @param H altitude
    # @return  longitude in SK-42
    #
    ro = np.float64(206264.8062) # Число угловых секунд в радиане

    # Эллипсоид Красовского
    aP = np.float64(6378245) # Большая полуось
    alP = np.float64(1 / 298.3) # Сжатие
    e2P = np.float64(2 * alP - math.pow(alP, 2)) # Квадрат эксцентриситета

    # Эллипсоид WGS84 (GRS80, эти два эллипсоида сходны по большинству параметров)
    aW = np.float64(6378137) # Большая полуось
    alW = np.float64(1 / 298.257223563) # Сжатие
    e2W = np.float64(2 * alW - math.pow(alW, 2)) # Квадрат эксцентриситета

    # Вспомогательные значения для преобразования эллипсоидов
    a = np.float64((aP + aW) / 2)
    e2 = np.float64((e2P + e2W) / 2)
    da = np.float64(aW - aP)
    de2 = np.float64(e2W - e2P)

    # Линейные элементы трансформирования, в метрах
    dx = np.float64(23.92)
    dy = np.float64(-141.27)
    dz = np.float64(-80.9)

    # Угловые элементы трансформирования, в секундах
    wx = np.float64(0)
    wy = np.float64(0)
    wz = np.float64(0)

    # Дифференциальное различие масштабов
    ms = np.float64(0)

    @classmethod
    def WGS84_SK42_Lat(cls, Bd, Ld, H):
        return Bd - cls.dB(Bd, Ld, H) / 3600

    #
    # convert from SK-42 to WGS-84.
    # @param Bd longitude
    # @param Ld latitude
    # @param H altitude
    # @return longitude in WGS-84
    #
    @classmethod
    def SK42_WGS84_Lat(cls, Bd, Ld, H):
        return Bd + cls.dB(Bd, Ld, H) / 3600

    #
    # convert from WGS-84 to SK-42.
    # @param Bd longitude
    # @param Ld latitude
    # @param H altitude
    # @return latitude in SK-42
    #
    @classmethod
    def WGS84_SK42_Long(cls, Bd, Ld, H):
        return Ld - cls.dL(Bd, Ld, H) / 3600

    #
    # convert from SK-42 to WGS-84.
    # @param Bd longitude
    # @param Ld latitude
    # @param H altitude
    # @return latitude in WGS-84
    #
    @classmethod
    def SK42_WGS84_Long(cls, Bd, Ld, H):
        return Ld + cls.dL(Bd, Ld, H) / 3600
    
    #
    # @param Bd longitude
    # @param Ld latitude
    # @param H altitude
    # @return
    #
    @classmethod
    def dB(cls, Bd, Ld, H):
        # import pdb
        # pdb.set_trace()
        # should be 0.7050959999929773
        B = Bd * math.pi / 180
        L = Ld * math.pi / 180
        M = cls.a * (1 - cls.e2) / math.pow((1 - cls.e2 * math.pow(math.sin(B), 2)), 1.5)
        N = cls.a * math.pow((1 - cls.e2 * math.pow(math.sin(B), 2)), -0.5)
        result = cls.ro / (M + H) * (N / cls.a * cls.e2 * math.sin(B) * math.cos(B) * cls.da + (math.pow(N, 2) / math.pow(cls.a, 2) + 1) * N * math.sin(B) * math.cos(B) * cls.e2 / 2 - (cls.dx * math.cos(L) + cls.dy * math.sin(L)) * math.sin(B) + cls.dz * math.cos(B)) - cls.wx * math.sin(L) * (1 + cls.e2 * math.cos(2 * B)) + cls.wy * math.cos(L) * (1 + cls.e2 * math.cos(2 * B)) - cls.ro * cls.ms * cls.e2 * math.sin(B) * math.cos(B)
        return result

    #
    # @param Bd longitude
    # @param Ld latitude
    # @param H altitude
    # @return
    #
    @classmethod
    def dL(cls, Bd, Ld, H):
        """ generated source for method dL """
        B = Bd * math.pi / 180
        L = Ld * math.pi / 180
        N = cls.a * math.pow((1 - cls.e2 * math.pow(math.sin(B), 2)), -0.5)
        return cls.ro / ((N + H) * math.cos(B)) * (-cls.dx * math.sin(L) + cls.dy * math.cos(L)) + math.tan(B) * (1 - cls.e2) * (cls.wx * math.cos(L) + cls.wy * math.sin(L)) - cls.wz

    #
    # @param Bd longitude
    # @param Ld latitude
    # @param H altitude
    # @return
    #
    @classmethod
    def WGS84Alt(cls, Bd, Ld, H):
        """ generated source for method WGS84Alt """
        B = Bd * math.pi / 180
        L = Ld * math.pi / 180
        N = a * math.pow((1 - e2 * math.pow(math.sin(B), 2)), -0.5)
        dH = -a / N * cls.da + N * math.pow(math.sin(B), 2) * de2 / 2 + (dx * math.cos(L) + dy * math.sin(L)) * math.cos(B) + cls.dz * math.sin(B) - N * e2 * math.sin(B) * math.cos(B) * (wx / ro * math.sin(L) - wy / ro * math.cos(L)) + (math.pow(a, 2) / N + H) * cls.ms
        return H + dH

