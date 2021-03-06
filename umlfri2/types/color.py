import re


class Color:
    __RE_HTML_COLOR = re.compile('^#([0-9a-fA-F]{2})?[0-9a-fA-F]{6}')
    
    def __init__(self, argb):
        self.__value = argb
    
    @property
    def alpha(self):
        return self.__value >> 24
    
    @property
    def r(self):
        return (self.__value >> 16) & 0xff
    
    @property
    def g(self):
        return (self.__value >> 8) & 0xff
    
    @property
    def b(self):
        return self.__value & 0xff
    
    @property
    def rgb(self):
        return self.__value & 0xffffff
    
    @property
    def argb(self):
        return self.__value
    
    @property
    def rgba(self):
        return ((self.__value & 0xff000000) >> 24) + (self.__value & 0xffffff) << 8
    
    def invert(self):
        return Color((self.__value & 0xff000000) + (0xffffff - self.__value & 0xffffff))
    
    def add_alpha(self, alpha):
        return Color(self.__value & 0xffffff + (alpha << 24))
    
    def to_gray(self):
        return Color(self.__value & 0xff000000 + (self.r * 11 + self.g * 16 + self.b * 5) // 32)
    
    def __eq__(self, other):
        if isinstance(other, Color):
            return self.__value == other.__value
        return NotImplemented
    
    def to_rgb_str(self):
        return "#{0:06x}".format(self.__value & 0xffffff)
    
    def __str__(self):
        return "#{0:08x}".format(self.__value)
    
    def __repr__(self):
        return "<Color {0}>".format(self)
    
    @staticmethod
    def from_string(color):
        if Colors.exists(color):
            return Colors.get(color)
        if Color.__RE_HTML_COLOR.match(color): # html rgb/argb
            val = int(color[1:], 16)
            if len(color) == 7:
                val = val + 0xff000000
            return Color(val)
        raise ValueError("color")
    
    @staticmethod
    def from_rgb_values(r, g, b, a=255):
        return Color((a << 24) & (r << 16) & (g << 8) & b)
    
    @staticmethod
    def from_argb(argb):
        return Color(argb)
    
    @staticmethod
    def from_rgba(rgba):
        return Color(((rgba & 0xff) << 24) + rgba >> 8)


class Colors:
    aliceblue = Color(0xfff0f8ff)
    antiquewhite = Color(0xfffaebd7)
    antiquewhite1 = Color(0xffffefdb)
    antiquewhite2 = Color(0xffeedfcc)
    antiquewhite3 = Color(0xffcdc0b0)
    antiquewhite4 = Color(0xff8b8378)
    aquamarine = Color(0xff7fffd4)
    aquamarine1 = Color(0xff7fffd4)
    aquamarine2 = Color(0xff76eec6)
    aquamarine3 = Color(0xff66cdaa)
    aquamarine4 = Color(0xff458b74)
    azure = Color(0xfff0ffff)
    azure1 = Color(0xfff0ffff)
    azure2 = Color(0xffe0eeee)
    azure3 = Color(0xffc1cdcd)
    azure4 = Color(0xff838b8b)
    beige = Color(0xfff5f5dc)
    bisque = Color(0xffffe4c4)
    bisque1 = Color(0xffffe4c4)
    bisque2 = Color(0xffeed5b7)
    bisque3 = Color(0xffcdb79e)
    bisque4 = Color(0xff8b7d6b)
    black = Color(0xff000000)
    blanchedalmond = Color(0xffffebcd)
    blue = Color(0xff0000ff)
    blue1 = Color(0xff0000ff)
    blue2 = Color(0xff0000ee)
    blue3 = Color(0xff0000cd)
    blue4 = Color(0xff00008b)
    blueviolet = Color(0xff8a2be2)
    brown = Color(0xffa52a2a)
    brown1 = Color(0xffff4040)
    brown2 = Color(0xffee3b3b)
    brown3 = Color(0xffcd3333)
    brown4 = Color(0xff8b2323)
    burlywood = Color(0xffdeb887)
    burlywood1 = Color(0xffffd39b)
    burlywood2 = Color(0xffeec591)
    burlywood3 = Color(0xffcdaa7d)
    burlywood4 = Color(0xff8b7355)
    cadetblue = Color(0xff5f9ea0)
    cadetblue1 = Color(0xff98f5ff)
    cadetblue2 = Color(0xff8ee5ee)
    cadetblue3 = Color(0xff7ac5cd)
    cadetblue4 = Color(0xff53868b)
    chartreuse = Color(0xff7fff00)
    chartreuse1 = Color(0xff7fff00)
    chartreuse2 = Color(0xff76ee00)
    chartreuse3 = Color(0xff66cd00)
    chartreuse4 = Color(0xff458b00)
    chocolate = Color(0xffd2691e)
    chocolate1 = Color(0xffff7f24)
    chocolate2 = Color(0xffee7621)
    chocolate3 = Color(0xffcd661d)
    chocolate4 = Color(0xff8b4513)
    coral = Color(0xffff7f50)
    coral1 = Color(0xffff7256)
    coral2 = Color(0xffee6a50)
    coral3 = Color(0xffcd5b45)
    coral4 = Color(0xff8b3e2f)
    cornflowerblue = Color(0xff6495ed)
    cornsilk = Color(0xfffff8dc)
    cornsilk1 = Color(0xfffff8dc)
    cornsilk2 = Color(0xffeee8cd)
    cornsilk3 = Color(0xffcdc8b1)
    cornsilk4 = Color(0xff8b8878)
    cyan = Color(0xff00ffff)
    cyan1 = Color(0xff00ffff)
    cyan2 = Color(0xff00eeee)
    cyan3 = Color(0xff00cdcd)
    cyan4 = Color(0xff008b8b)
    darkblue = Color(0xff00008b)
    darkcyan = Color(0xff008b8b)
    darkgoldenrod = Color(0xffb8860b)
    darkgoldenrod1 = Color(0xffffb90f)
    darkgoldenrod2 = Color(0xffeead0e)
    darkgoldenrod3 = Color(0xffcd950c)
    darkgoldenrod4 = Color(0xff8b6508)
    darkgray = Color(0xffa9a9a9)
    darkgreen = Color(0xff006400)
    darkkhaki = Color(0xffbdb76b)
    darkmagenta = Color(0xff8b008b)
    darkolivegreen = Color(0xff556b2f)
    darkolivegreen1 = Color(0xffcaff70)
    darkolivegreen2 = Color(0xffbcee68)
    darkolivegreen3 = Color(0xffa2cd5a)
    darkolivegreen4 = Color(0xff6e8b3d)
    darkorange = Color(0xffff8c00)
    darkorange1 = Color(0xffff7f00)
    darkorange2 = Color(0xffee7600)
    darkorange3 = Color(0xffcd6600)
    darkorange4 = Color(0xff8b4500)
    darkorchid = Color(0xff9932cc)
    darkorchid1 = Color(0xffbf3eff)
    darkorchid2 = Color(0xffb23aee)
    darkorchid3 = Color(0xff9a32cd)
    darkorchid4 = Color(0xff68228b)
    darkred = Color(0xff8b0000)
    darksalmon = Color(0xffe9967a)
    darkseagreen = Color(0xff8fbc8f)
    darkseagreen1 = Color(0xffc1ffc1)
    darkseagreen2 = Color(0xffb4eeb4)
    darkseagreen3 = Color(0xff9bcd9b)
    darkseagreen4 = Color(0xff698b69)
    darkslateblue = Color(0xff483d8b)
    darkslategray = Color(0xff2f4f4f)
    darkslategray1 = Color(0xff97ffff)
    darkslategray2 = Color(0xff8deeee)
    darkslategray3 = Color(0xff79cdcd)
    darkslategray4 = Color(0xff528b8b)
    darkturquoise = Color(0xff00ced1)
    darkviolet = Color(0xff9400d3)
    deeppink = Color(0xffff1493)
    deeppink1 = Color(0xffff1493)
    deeppink2 = Color(0xffee1289)
    deeppink3 = Color(0xffcd1076)
    deeppink4 = Color(0xff8b0a50)
    deepskyblue = Color(0xff00bfff)
    deepskyblue1 = Color(0xff00bfff)
    deepskyblue2 = Color(0xff00b2ee)
    deepskyblue3 = Color(0xff009acd)
    deepskyblue4 = Color(0xff00688b)
    dimgray = Color(0xff696969)
    dodgerblue = Color(0xff1e90ff)
    dodgerblue1 = Color(0xff1e90ff)
    dodgerblue2 = Color(0xff1c86ee)
    dodgerblue3 = Color(0xff1874cd)
    dodgerblue4 = Color(0xff104e8b)
    firebrick = Color(0xffb22222)
    firebrick1 = Color(0xffff3030)
    firebrick2 = Color(0xffee2c2c)
    firebrick3 = Color(0xffcd2626)
    firebrick4 = Color(0xff8b1a1a)
    floralwhite = Color(0xfffffaf0)
    forestgreen = Color(0xff228b22)
    gainsboro = Color(0xffdcdcdc)
    ghostwhite = Color(0xfff8f8ff)
    gold = Color(0xffffd700)
    gold1 = Color(0xffffd700)
    gold2 = Color(0xffeec900)
    gold3 = Color(0xffcdad00)
    gold4 = Color(0xff8b7500)
    goldenrod = Color(0xffdaa520)
    goldenrod1 = Color(0xffffc125)
    goldenrod2 = Color(0xffeeb422)
    goldenrod3 = Color(0xffcd9b1d)
    goldenrod4 = Color(0xff8b6914)
    gray = Color(0xffbebebe)
    gray0 = Color(0xff000000)
    gray1 = Color(0xff030303)
    gray2 = Color(0xff050505)
    gray3 = Color(0xff080808)
    gray4 = Color(0xff0a0a0a)
    gray5 = Color(0xff0d0d0d)
    gray6 = Color(0xff0f0f0f)
    gray7 = Color(0xff121212)
    gray8 = Color(0xff141414)
    gray9 = Color(0xff171717)
    gray10 = Color(0xff1a1a1a)
    gray11 = Color(0xff1c1c1c)
    gray12 = Color(0xff1f1f1f)
    gray13 = Color(0xff212121)
    gray14 = Color(0xff242424)
    gray15 = Color(0xff262626)
    gray16 = Color(0xff292929)
    gray17 = Color(0xff2b2b2b)
    gray18 = Color(0xff2e2e2e)
    gray19 = Color(0xff303030)
    gray20 = Color(0xff333333)
    gray21 = Color(0xff363636)
    gray22 = Color(0xff383838)
    gray23 = Color(0xff3b3b3b)
    gray24 = Color(0xff3d3d3d)
    gray25 = Color(0xff404040)
    gray26 = Color(0xff424242)
    gray27 = Color(0xff454545)
    gray28 = Color(0xff474747)
    gray29 = Color(0xff4a4a4a)
    gray30 = Color(0xff4d4d4d)
    gray31 = Color(0xff4f4f4f)
    gray32 = Color(0xff525252)
    gray33 = Color(0xff545454)
    gray34 = Color(0xff575757)
    gray35 = Color(0xff595959)
    gray36 = Color(0xff5c5c5c)
    gray37 = Color(0xff5e5e5e)
    gray38 = Color(0xff616161)
    gray39 = Color(0xff636363)
    gray40 = Color(0xff666666)
    gray41 = Color(0xff696969)
    gray42 = Color(0xff6b6b6b)
    gray43 = Color(0xff6e6e6e)
    gray44 = Color(0xff707070)
    gray45 = Color(0xff737373)
    gray46 = Color(0xff757575)
    gray47 = Color(0xff787878)
    gray48 = Color(0xff7a7a7a)
    gray49 = Color(0xff7d7d7d)
    gray50 = Color(0xff7f7f7f)
    gray51 = Color(0xff828282)
    gray52 = Color(0xff858585)
    gray53 = Color(0xff878787)
    gray54 = Color(0xff8a8a8a)
    gray55 = Color(0xff8c8c8c)
    gray56 = Color(0xff8f8f8f)
    gray57 = Color(0xff919191)
    gray58 = Color(0xff949494)
    gray59 = Color(0xff969696)
    gray60 = Color(0xff999999)
    gray61 = Color(0xff9c9c9c)
    gray62 = Color(0xff9e9e9e)
    gray63 = Color(0xffa1a1a1)
    gray64 = Color(0xffa3a3a3)
    gray65 = Color(0xffa6a6a6)
    gray66 = Color(0xffa8a8a8)
    gray67 = Color(0xffababab)
    gray68 = Color(0xffadadad)
    gray69 = Color(0xffb0b0b0)
    gray70 = Color(0xffb3b3b3)
    gray71 = Color(0xffb5b5b5)
    gray72 = Color(0xffb8b8b8)
    gray73 = Color(0xffbababa)
    gray74 = Color(0xffbdbdbd)
    gray75 = Color(0xffbfbfbf)
    gray76 = Color(0xffc2c2c2)
    gray77 = Color(0xffc4c4c4)
    gray78 = Color(0xffc7c7c7)
    gray79 = Color(0xffc9c9c9)
    gray80 = Color(0xffcccccc)
    gray81 = Color(0xffcfcfcf)
    gray82 = Color(0xffd1d1d1)
    gray83 = Color(0xffd4d4d4)
    gray84 = Color(0xffd6d6d6)
    gray85 = Color(0xffd9d9d9)
    gray86 = Color(0xffdbdbdb)
    gray87 = Color(0xffdedede)
    gray88 = Color(0xffe0e0e0)
    gray89 = Color(0xffe3e3e3)
    gray90 = Color(0xffe5e5e5)
    gray91 = Color(0xffe8e8e8)
    gray92 = Color(0xffebebeb)
    gray93 = Color(0xffededed)
    gray94 = Color(0xfff0f0f0)
    gray95 = Color(0xfff2f2f2)
    gray96 = Color(0xfff5f5f5)
    gray97 = Color(0xfff7f7f7)
    gray98 = Color(0xfffafafa)
    gray99 = Color(0xfffcfcfc)
    gray100 = Color(0xffffffff)
    green = Color(0xff00ff00)
    green1 = Color(0xff00ff00)
    green2 = Color(0xff00ee00)
    green3 = Color(0xff00cd00)
    green4 = Color(0xff008b00)
    greenyellow = Color(0xffadff2f)
    honeydew = Color(0xfff0fff0)
    honeydew1 = Color(0xfff0fff0)
    honeydew2 = Color(0xffe0eee0)
    honeydew3 = Color(0xffc1cdc1)
    honeydew4 = Color(0xff838b83)
    hotpink = Color(0xffff69b4)
    hotpink1 = Color(0xffff6eb4)
    hotpink2 = Color(0xffee6aa7)
    hotpink3 = Color(0xffcd6090)
    hotpink4 = Color(0xff8b3a62)
    indianred = Color(0xffcd5c5c)
    indianred1 = Color(0xffff6a6a)
    indianred2 = Color(0xffee6363)
    indianred3 = Color(0xffcd5555)
    indianred4 = Color(0xff8b3a3a)
    ivory = Color(0xfffffff0)
    ivory1 = Color(0xfffffff0)
    ivory2 = Color(0xffeeeee0)
    ivory3 = Color(0xffcdcdc1)
    ivory4 = Color(0xff8b8b83)
    khaki = Color(0xfff0e68c)
    khaki1 = Color(0xfffff68f)
    khaki2 = Color(0xffeee685)
    khaki3 = Color(0xffcdc673)
    khaki4 = Color(0xff8b864e)
    lavender = Color(0xffe6e6fa)
    lavenderblush = Color(0xfffff0f5)
    lavenderblush1 = Color(0xfffff0f5)
    lavenderblush2 = Color(0xffeee0e5)
    lavenderblush3 = Color(0xffcdc1c5)
    lavenderblush4 = Color(0xff8b8386)
    lawngreen = Color(0xff7cfc00)
    lemonchiffon = Color(0xfffffacd)
    lemonchiffon1 = Color(0xfffffacd)
    lemonchiffon2 = Color(0xffeee9bf)
    lemonchiffon3 = Color(0xffcdc9a5)
    lemonchiffon4 = Color(0xff8b8970)
    lightblue = Color(0xffadd8e6)
    lightblue1 = Color(0xffbfefff)
    lightblue2 = Color(0xffb2dfee)
    lightblue3 = Color(0xff9ac0cd)
    lightblue4 = Color(0xff68838b)
    lightcoral = Color(0xfff08080)
    lightcyan = Color(0xffe0ffff)
    lightcyan1 = Color(0xffe0ffff)
    lightcyan2 = Color(0xffd1eeee)
    lightcyan3 = Color(0xffb4cdcd)
    lightcyan4 = Color(0xff7a8b8b)
    lightgoldenrod = Color(0xffeedd82)
    lightgoldenrod1 = Color(0xffffec8b)
    lightgoldenrod2 = Color(0xffeedc82)
    lightgoldenrod3 = Color(0xffcdbe70)
    lightgoldenrod4 = Color(0xff8b814c)
    lightgoldenrodyellow = Color(0xfffafad2)
    lightgray = Color(0xffd3d3d3)
    lightgreen = Color(0xff90ee90)
    lightpink = Color(0xffffb6c1)
    lightpink1 = Color(0xffffaeb9)
    lightpink2 = Color(0xffeea2ad)
    lightpink3 = Color(0xffcd8c95)
    lightpink4 = Color(0xff8b5f65)
    lightsalmon = Color(0xffffa07a)
    lightsalmon1 = Color(0xffffa07a)
    lightsalmon2 = Color(0xffee9572)
    lightsalmon3 = Color(0xffcd8162)
    lightsalmon4 = Color(0xff8b5742)
    lightseagreen = Color(0xff20b2aa)
    lightskyblue = Color(0xff87cefa)
    lightskyblue1 = Color(0xffb0e2ff)
    lightskyblue2 = Color(0xffa4d3ee)
    lightskyblue3 = Color(0xff8db6cd)
    lightskyblue4 = Color(0xff607b8b)
    lightslateblue = Color(0xff8470ff)
    lightslategray = Color(0xff778899)
    lightsteelblue = Color(0xffb0c4de)
    lightsteelblue1 = Color(0xffcae1ff)
    lightsteelblue2 = Color(0xffbcd2ee)
    lightsteelblue3 = Color(0xffa2b5cd)
    lightsteelblue4 = Color(0xff6e7b8b)
    lightyellow = Color(0xffffffe0)
    lightyellow1 = Color(0xffffffe0)
    lightyellow2 = Color(0xffeeeed1)
    lightyellow3 = Color(0xffcdcdb4)
    lightyellow4 = Color(0xff8b8b7a)
    limegreen = Color(0xff32cd32)
    linen = Color(0xfffaf0e6)
    magenta = Color(0xffff00ff)
    magenta1 = Color(0xffff00ff)
    magenta2 = Color(0xffee00ee)
    magenta3 = Color(0xffcd00cd)
    magenta4 = Color(0xff8b008b)
    maroon = Color(0xffb03060)
    maroon1 = Color(0xffff34b3)
    maroon2 = Color(0xffee30a7)
    maroon3 = Color(0xffcd2990)
    maroon4 = Color(0xff8b1c62)
    mediumaquamarine = Color(0xff66cdaa)
    mediumblue = Color(0xff0000cd)
    mediumorchid = Color(0xffba55d3)
    mediumorchid1 = Color(0xffe066ff)
    mediumorchid2 = Color(0xffd15fee)
    mediumorchid3 = Color(0xffb452cd)
    mediumorchid4 = Color(0xff7a378b)
    mediumpurple = Color(0xff9370db)
    mediumpurple1 = Color(0xffab82ff)
    mediumpurple2 = Color(0xff9f79ee)
    mediumpurple3 = Color(0xff8968cd)
    mediumpurple4 = Color(0xff5d478b)
    mediumseagreen = Color(0xff3cb371)
    mediumslateblue = Color(0xff7b68ee)
    mediumspringgreen = Color(0xff00fa9a)
    mediumturquoise = Color(0xff48d1cc)
    mediumvioletred = Color(0xffc71585)
    midnightblue = Color(0xff191970)
    mintcream = Color(0xfff5fffa)
    mistyrose = Color(0xffffe4e1)
    mistyrose1 = Color(0xffffe4e1)
    mistyrose2 = Color(0xffeed5d2)
    mistyrose3 = Color(0xffcdb7b5)
    mistyrose4 = Color(0xff8b7d7b)
    moccasin = Color(0xffffe4b5)
    navahowhite = Color(0xffffdead)
    navahowhite1 = Color(0xffffdead)
    navahowhite2 = Color(0xffeecfa1)
    navahowhite3 = Color(0xffcdb38b)
    navahowhite4 = Color(0xff8b795e)
    navajowhite = Color(0xffffdead)
    navajowhite1 = Color(0xffffdead)
    navajowhite2 = Color(0xffeecfa1)
    navajowhite3 = Color(0xffcdb38b)
    navajowhite4 = Color(0xff8b795e)
    navy = Color(0xff000080)
    navyblue = Color(0xff000080)
    oldlace = Color(0xfffdf5e6)
    olivedrab = Color(0xff6b8e23)
    olivedrab1 = Color(0xffc0ff3e)
    olivedrab2 = Color(0xffb3ee3a)
    olivedrab3 = Color(0xff9acd32)
    olivedrab4 = Color(0xff698b22)
    orange = Color(0xffffa500)
    orange1 = Color(0xffffa500)
    orange2 = Color(0xffee9a00)
    orange3 = Color(0xffcd8500)
    orange4 = Color(0xff8b5a00)
    orangered = Color(0xffff4500)
    orangered1 = Color(0xffff4500)
    orangered2 = Color(0xffee4000)
    orangered3 = Color(0xffcd3700)
    orangered4 = Color(0xff8b2500)
    orchid = Color(0xffda70d6)
    orchid1 = Color(0xffff83fa)
    orchid2 = Color(0xffee7ae9)
    orchid3 = Color(0xffcd69c9)
    orchid4 = Color(0xff8b4789)
    palegoldenrod = Color(0xffeee8aa)
    palegreen = Color(0xff98fb98)
    palegreen1 = Color(0xff9aff9a)
    palegreen2 = Color(0xff90ee90)
    palegreen3 = Color(0xff7ccd7c)
    palegreen4 = Color(0xff548b54)
    paleturquoise = Color(0xffafeeee)
    paleturquoise1 = Color(0xffbbffff)
    paleturquoise2 = Color(0xffaeeeee)
    paleturquoise3 = Color(0xff96cdcd)
    paleturquoise4 = Color(0xff668b8b)
    palevioletred = Color(0xffdb7093)
    palevioletred1 = Color(0xffff82ab)
    palevioletred2 = Color(0xffee799f)
    palevioletred3 = Color(0xffcd6889)
    palevioletred4 = Color(0xff8b475d)
    papayawhip = Color(0xffffefd5)
    peachpuff = Color(0xffffdab9)
    peachpuff1 = Color(0xffffdab9)
    peachpuff2 = Color(0xffeecbad)
    peachpuff3 = Color(0xffcdaf95)
    peachpuff4 = Color(0xff8b7765)
    peru = Color(0xffcd853f)
    pink = Color(0xffffc0cb)
    pink1 = Color(0xffffb5c5)
    pink2 = Color(0xffeea9b8)
    pink3 = Color(0xffcd919e)
    pink4 = Color(0xff8b636c)
    plum = Color(0xffdda0dd)
    plum1 = Color(0xffffbbff)
    plum2 = Color(0xffeeaeee)
    plum3 = Color(0xffcd96cd)
    plum4 = Color(0xff8b668b)
    powderblue = Color(0xffb0e0e6)
    purple = Color(0xffa020f0)
    purple1 = Color(0xff9b30ff)
    purple2 = Color(0xff912cee)
    purple3 = Color(0xff7d26cd)
    purple4 = Color(0xff551a8b)
    red = Color(0xffff0000)
    red1 = Color(0xffff0000)
    red2 = Color(0xffee0000)
    red3 = Color(0xffcd0000)
    red4 = Color(0xff8b0000)
    rosybrown = Color(0xffbc8f8f)
    rosybrown1 = Color(0xffffc1c1)
    rosybrown2 = Color(0xffeeb4b4)
    rosybrown3 = Color(0xffcd9b9b)
    rosybrown4 = Color(0xff8b6969)
    royalblue = Color(0xff4169e1)
    royalblue1 = Color(0xff4876ff)
    royalblue2 = Color(0xff436eee)
    royalblue3 = Color(0xff3a5fcd)
    royalblue4 = Color(0xff27408b)
    saddlebrown = Color(0xff8b4513)
    salmon = Color(0xfffa8072)
    salmon1 = Color(0xffff8c69)
    salmon2 = Color(0xffee8262)
    salmon3 = Color(0xffcd7054)
    salmon4 = Color(0xff8b4c39)
    sandybrown = Color(0xfff4a460)
    seagreen = Color(0xff2e8b57)
    seagreen1 = Color(0xff54ff9f)
    seagreen2 = Color(0xff4eee94)
    seagreen3 = Color(0xff43cd80)
    seagreen4 = Color(0xff2e8b57)
    seashell = Color(0xfffff5ee)
    seashell1 = Color(0xfffff5ee)
    seashell2 = Color(0xffeee5de)
    seashell3 = Color(0xffcdc5bf)
    seashell4 = Color(0xff8b8682)
    sienna = Color(0xffa0522d)
    sienna1 = Color(0xffff8247)
    sienna2 = Color(0xffee7942)
    sienna3 = Color(0xffcd6839)
    sienna4 = Color(0xff8b4726)
    skyblue = Color(0xff87ceeb)
    skyblue1 = Color(0xff87ceff)
    skyblue2 = Color(0xff7ec0ee)
    skyblue3 = Color(0xff6ca6cd)
    skyblue4 = Color(0xff4a708b)
    slateblue = Color(0xff6a5acd)
    slateblue1 = Color(0xff836fff)
    slateblue2 = Color(0xff7a67ee)
    slateblue3 = Color(0xff6959cd)
    slateblue4 = Color(0xff473c8b)
    slategray = Color(0xff708090)
    slategray1 = Color(0xffc6e2ff)
    slategray2 = Color(0xffb9d3ee)
    slategray3 = Color(0xff9fb6cd)
    slategray4 = Color(0xff6c7b8b)
    snow = Color(0xfffffafa)
    snow1 = Color(0xfffffafa)
    snow2 = Color(0xffeee9e9)
    snow3 = Color(0xffcdc9c9)
    snow4 = Color(0xff8b8989)
    springgreen = Color(0xff00ff7f)
    springgreen1 = Color(0xff00ff7f)
    springgreen2 = Color(0xff00ee76)
    springgreen3 = Color(0xff00cd66)
    springgreen4 = Color(0xff008b45)
    steelblue = Color(0xff4682b4)
    steelblue1 = Color(0xff63b8ff)
    steelblue2 = Color(0xff5cacee)
    steelblue3 = Color(0xff4f94cd)
    steelblue4 = Color(0xff36648b)
    tan = Color(0xffd2b48c)
    tan1 = Color(0xffffa54f)
    tan2 = Color(0xffee9a49)
    tan3 = Color(0xffcd853f)
    tan4 = Color(0xff8b5a2b)
    thistle = Color(0xffd8bfd8)
    thistle1 = Color(0xffffe1ff)
    thistle2 = Color(0xffeed2ee)
    thistle3 = Color(0xffcdb5cd)
    thistle4 = Color(0xff8b7b8b)
    tomato = Color(0xffff6347)
    tomato1 = Color(0xffff6347)
    tomato2 = Color(0xffee5c42)
    tomato3 = Color(0xffcd4f39)
    tomato4 = Color(0xff8b3626)
    turquoise = Color(0xff40e0d0)
    turquoise1 = Color(0xff00f5ff)
    turquoise2 = Color(0xff00e5ee)
    turquoise3 = Color(0xff00c5cd)
    turquoise4 = Color(0xff00868b)
    violet = Color(0xffee82ee)
    violetred = Color(0xffd02090)
    violetred1 = Color(0xffff3e96)
    violetred2 = Color(0xffee3a8c)
    violetred3 = Color(0xffcd3278)
    violetred4 = Color(0xff8b2252)
    wheat = Color(0xfff5deb3)
    wheat1 = Color(0xffffe7ba)
    wheat2 = Color(0xffeed8ae)
    wheat3 = Color(0xffcdba96)
    wheat4 = Color(0xff8b7e66)
    white = Color(0xffffffff)
    whitesmoke = Color(0xfff5f5f5)
    yellow = Color(0xffffff00)
    yellow1 = Color(0xffffff00)
    yellow2 = Color(0xffeeee00)
    yellow3 = Color(0xffcdcd00)
    yellow4 = Color(0xff8b8b00)
    yellowgreen = Color(0xff9acd32)
    
    @staticmethod
    def exists(name):
        return isinstance(getattr(Colors, name, None), Color)
    
    @staticmethod
    def get(name):
        return getattr(Colors, name)
