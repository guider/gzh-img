#!/usr/bin/env python3
"""Render a 900x383 WeChat cover from one of several embedded templates.

    python3 make_cover.py --text 四字关键词 --out cover.png \
        [--variant tech|idea|steps|life|retail-shelf|retail-tag|retail-bag] \
        [--layout row|grid|wide] [--font-scale 1.0] \
        [--primary '#1a7f5a'] [--dark '#1c2b26']

retail-shelf / retail-tag / retail-bag are retail/goods-themed illustrations
(shelf display, price tag, shopping bag) meant to be used with
--layout wide, which lets the hero text run ~1.5x larger than the row/grid
layouts without colliding with the artwork (those templates reserve their
own space for it — a bottom band, a background block, or a corner cutout —
instead of a competing side column).
"""
import argparse
import io
import math
import re
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sys.stderr.write("playwright is missing. Try:\n"
                     "  pip install playwright --break-system-packages\n")
    raise SystemExit(1)

from PIL import Image

W, H = 900, 383
FONT_STACK = ("'Noto Sans CJK SC','Noto Sans SC','PingFang SC',"
              "'Microsoft YaHei',sans-serif")

TPL_TECH = """\
<!doctype html>
<html><head><meta charset="utf-8">
<style>
html,body{margin:0;padding:0;}
*{-webkit-font-smoothing:antialiased;}
</style><style>
    body { margin: 0; }
    a { color: #b45309; } a:hover { color: #92400e; }
  </style>
</head>
<body><div style="width: 900px; height: 383px; position: relative; overflow: hidden; background: {{dark}}; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;">
  <svg width="900" height="383" viewBox="0 0 900 383" style="position: absolute; left: 0; top: 0;">
    <defs>
      <clipPath id="t-box"><rect x="0" y="0" width="900" height="383"></rect></clipPath>
      <clipPath id="t-lensR"><rect x="700" y="0" width="200" height="383"></rect></clipPath>
    </defs>
    <g clip-path="url(#t-box)">
      <rect x="0" y="0" width="900" height="383" fill="{{dark}}"></rect>
      <rect x="596" y="0" width="304" height="383" fill="{{deeper}}"></rect>
      <path d="M 700 26 A 165 165 0 0 1 700 356 Z" fill="{{primary}}"></path>
      <path d="M 700 66 A 125 125 0 0 0 700 316" fill="none" stroke="{{tint2}}" stroke-width="24"></path>
      <path d="M 700 106 A 85 85 0 0 0 700 276" fill="none" stroke="{{tint3}}" stroke-width="16"></path>
      <circle cx="700" cy="191" r="26" fill="{{tint1}}"></circle>
      <path d="M 74 88 L 170 88 L 170 158 L 238 158" fill="none" stroke="{{deep}}" stroke-width="10" stroke-linecap="square"></path>
      <path d="M 74 262 L 122 262 L 122 320 L 214 320" fill="none" stroke="{{primary}}" stroke-width="10" stroke-linecap="square"></path>
      <circle cx="74" cy="88" r="9" fill="{{tint2}}"></circle>
      <circle cx="170" cy="88" r="9" fill="{{deep}}"></circle>
      <circle cx="170" cy="158" r="9" fill="{{deep}}"></circle>
      <circle cx="74" cy="262" r="9" fill="{{deep}}"></circle>
      <circle cx="122" cy="262" r="9" fill="{{primary}}"></circle>
      <circle cx="122" cy="320" r="9" fill="{{deep}}"></circle>
      <circle cx="214" cy="320" r="9" fill="{{tint2}}"></circle>
      <rect x="824" y="52" width="22" height="22" fill="{{tint3}}"></rect>
      <rect x="854" y="52" width="22" height="22" fill="{{tint1}}"></rect>
      <rect x="824" y="82" width="22" height="22" fill="{{tint1}}"></rect>
      <rect x="854" y="82" width="22" height="22" fill="{{primary}}"></rect>
    </g>
  </svg>
  <!--HERO--><div style="position: absolute; left: 262px; top: 70px; z-index: 3;">
    <div style="display: grid; grid-template-columns: repeat(2, 112px); grid-template-rows: repeat(2, 112px); gap: 14px;"><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">公</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">众</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">排</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">版</span></div>
  </div><!--/HERO-->
  <div style="position: absolute; left: 482px; top: 22px; width: 84px; height: 84px; background: {{tint3}}; z-index: 1;"></div>
  <div style="position: absolute; left: 244px; top: 324px; width: 226px; height: 10px; background: {{tint2}}; z-index: 1;"></div>
</div></body></html>
"""

TPL_IDEA = """\
<!doctype html>
<html><head><meta charset="utf-8">
<style>
html,body{margin:0;padding:0;}
*{-webkit-font-smoothing:antialiased;}
</style><style>
    body { margin: 0; }
    a { color: #b45309; } a:hover { color: #92400e; }
  </style>
</head>
<body><div style="width: 900px; height: 383px; position: relative; overflow: hidden; background: {{dark}}; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;">
  <svg width="900" height="383" viewBox="0 0 900 383" style="position: absolute; left: 0; top: 0;">
    <defs>
      <clipPath id="i-box"><rect x="0" y="0" width="900" height="383"></rect></clipPath>
    </defs>
    <g clip-path="url(#i-box)">
      <rect x="0" y="0" width="900" height="383" fill="{{dark}}"></rect>
      <rect x="596" y="0" width="304" height="383" fill="{{deeper}}"></rect>
      <circle cx="686" cy="146" r="132" fill="{{primary}}"></circle>
      <path d="M 630 262 L 700 262 L 640 340 Z" fill="{{primary}}"></path>
      <circle cx="808" cy="248" r="86" fill="{{tint2}}"></circle>
      <circle cx="716" cy="122" r="44" fill="{{tint3}}"></circle>
      <path d="M 560 348 L 848 348" fill="none" stroke="{{tint1}}" stroke-width="20"></path>
      <path d="M 846 328 L 890 348 L 846 368 Z" fill="{{tint1}}"></path>
      <path d="M 76 130 A 54 54 0 0 1 130 76" fill="none" stroke="{{deep}}" stroke-width="14"></path>
      <path d="M 130 40 A 90 90 0 0 1 220 130" fill="none" stroke="{{deep}}" stroke-width="14"></path>
      <path d="M 76 194 A 118 118 0 0 0 194 312" fill="none" stroke="{{primary}}" stroke-width="14"></path>
    </g>
  </svg>
  <!--HERO--><div style="position: absolute; left: 262px; top: 70px; z-index: 3;">
    <div style="display: grid; grid-template-columns: repeat(2, 112px); grid-template-rows: repeat(2, 112px); gap: 14px;"><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">公</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">众</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">排</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">版</span></div>
  </div><!--/HERO-->
  <div style="position: absolute; left: 490px; top: 232px; width: 0; height: 0; border-left: 74px solid {{tint3}}; border-bottom: 62px solid transparent; border-top: 62px solid transparent; z-index: 1;"></div>
  <div style="position: absolute; left: 244px; top: 26px; width: 178px; height: 12px; background: {{tint2}}; z-index: 1;"></div>
</div></body></html>
"""

TPL_STEPS = """\
<!doctype html>
<html><head><meta charset="utf-8">
<style>
html,body{margin:0;padding:0;}
*{-webkit-font-smoothing:antialiased;}
</style><style>
    body { margin: 0; }
    a { color: #b45309; } a:hover { color: #92400e; }
  </style>
</head>
<body><div style="width: 900px; height: 383px; position: relative; overflow: hidden; background: {{dark}}; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;">
  <svg width="900" height="383" viewBox="0 0 900 383" style="position: absolute; left: 0; top: 0;">
    <defs>
      <clipPath id="s-box"><rect x="0" y="0" width="900" height="383"></rect></clipPath>
    </defs>
    <g clip-path="url(#s-box)">
      <rect x="0" y="0" width="900" height="383" fill="{{dark}}"></rect>
      <rect x="596" y="0" width="304" height="383" fill="{{deeper}}"></rect>
      <rect x="600" y="272" width="52" height="111" fill="{{deep}}"></rect>
      <rect x="662" y="216" width="52" height="167" fill="{{primary}}"></rect>
      <rect x="724" y="160" width="52" height="223" fill="{{primary}}"></rect>
      <rect x="786" y="104" width="52" height="279" fill="{{tint1}}"></rect>
      <rect x="848" y="48" width="52" height="335" fill="{{tint2}}"></rect>
      <circle cx="874" cy="26" r="26" fill="{{tint3}}"></circle>
      <path d="M 64 214 L 116 266 L 214 152" fill="none" stroke="{{primary}}" stroke-width="24" stroke-linecap="square"></path>
      <rect x="64" y="60" width="150" height="16" fill="{{deep}}"></rect>
      <rect x="64" y="88" width="110" height="16" fill="{{deep}}"></rect>
      <rect x="64" y="116" width="70" height="16" fill="{{tint2}}"></rect>
      <rect x="64" y="324" width="16" height="16" fill="{{tint2}}"></rect>
      <rect x="92" y="324" width="122" height="16" fill="{{deep}}"></rect>
    </g>
  </svg>
  <!--HERO--><div style="position: absolute; left: 262px; top: 70px; z-index: 3;">
    <div style="display: grid; grid-template-columns: repeat(2, 112px); grid-template-rows: repeat(2, 112px); gap: 14px;"><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">公</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">众</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">排</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">版</span></div>
  </div><!--/HERO-->
  <div style="position: absolute; left: 486px; top: 208px; width: 84px; height: 84px; background: {{tint3}}; z-index: 1;"></div>
  <div style="position: absolute; left: 244px; top: 322px; width: 214px; height: 10px; background: {{tint2}}; z-index: 1;"></div>
</div></body></html>
"""

TPL_LIFE = """\
<!doctype html>
<html><head><meta charset="utf-8">
<style>
html,body{margin:0;padding:0;}
*{-webkit-font-smoothing:antialiased;}
</style><style>
    body { margin: 0; }
    a { color: #b45309; } a:hover { color: #92400e; }
  </style>
</head>
<body><div style="width: 900px; height: 383px; position: relative; overflow: hidden; background: {{dark}}; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;">
  <svg width="900" height="383" viewBox="0 0 900 383" style="position: absolute; left: 0; top: 0;">
    <defs>
      <clipPath id="l-box"><rect x="0" y="0" width="900" height="383"></rect></clipPath>
    </defs>
    <g clip-path="url(#l-box)">
      <rect x="0" y="0" width="900" height="383" fill="{{dark}}"></rect>
      <rect x="596" y="0" width="304" height="383" fill="{{deeper}}"></rect>
      <circle cx="722" cy="120" r="72" fill="{{primary}}"></circle>
      <rect x="714" y="8" width="16" height="34" fill="{{tint2}}"></rect>
      <rect x="808" y="112" width="34" height="16" fill="{{tint2}}"></rect>
      <rect x="790" y="46" width="34" height="16" fill="{{tint2}}" transform="rotate(-45 807 54)"></rect>
      <rect x="620" y="46" width="34" height="16" fill="{{tint2}}" transform="rotate(45 637 54)"></rect>
      <rect x="500" y="266" width="400" height="8" fill="{{tint3}}"></rect>
      <path d="M 512 274 A 118 118 0 0 1 748 274 Z" fill="{{tint1}}"></path>
      <path d="M 690 274 A 150 150 0 0 1 900 274 Z" fill="{{primary}}"></path>
      <circle cx="128" cy="82" r="44" fill="{{tint3}}"></circle>
      <circle cx="152" cy="70" r="44" fill="{{dark}}"></circle>
      <rect x="64" y="318" width="150" height="12" fill="{{deep}}"></rect>
      <rect x="64" y="342" width="72" height="12" fill="{{primary}}"></rect>
    </g>
  </svg>
  <!--HERO--><div style="position: absolute; left: 262px; top: 70px; z-index: 3;">
    <div style="display: grid; grid-template-columns: repeat(2, 112px); grid-template-rows: repeat(2, 112px); gap: 14px;"><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">公</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">众</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">排</span><span style="display: flex; align-items: center; justify-content: center; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif; font-weight: 900; font-size: 104px; line-height: 1; color: #ffffff;">版</span></div>
  </div><!--/HERO-->
  <div style="position: absolute; left: 486px; top: 262px; width: 84px; height: 84px; border-radius: 50%; background: {{tint3}}; z-index: 1;"></div>
  <div style="position: absolute; left: 244px; top: 30px; width: 190px; height: 10px; background: {{tint2}}; z-index: 1;"></div>
</div></body></html>
"""

TPL_RETAIL_SHELF = """\
<!doctype html>
<html><head><meta charset="utf-8">
<style>
html,body{margin:0;padding:0;}
*{-webkit-font-smoothing:antialiased;}
</style></head>
<body><div style="width: 900px; height: 383px; position: relative; overflow: hidden; background: {{dark}}; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;">
  <svg width="900" height="383" viewBox="0 0 900 383" style="position:absolute;left:0;top:0;">
    <circle cx="-70" cy="-70" r="115" fill="none" stroke="{{primary}}" stroke-width="16" opacity=".30"></circle>
    <line x1="0" y1="349" x2="900" y2="349" stroke="{{tint2}}" stroke-width="6" opacity=".55"></line>
    <rect x="28" y="279" width="46" height="70" rx="8" fill="{{primary}}" opacity=".95"></rect>
    <rect x="100" y="295" width="58" height="54" rx="8" fill="{{tint2}}" opacity=".8"></rect>
    <circle cx="197" cy="330" r="19" fill="{{primary}}" opacity=".6"></circle>
    <rect x="242" y="285" width="38" height="64" rx="8" fill="{{tint3}}" opacity=".9"></rect>
    <rect x="306" y="279" width="52" height="70" rx="8" fill="{{primary}}" opacity=".95"></rect>
    <circle cx="404" cy="317" r="21" fill="{{tint2}}" opacity=".8"></circle>
    <rect x="452" y="253" width="46" height="96" rx="8" fill="{{deep}}" opacity=".9"></rect>
    <rect x="524" y="289" width="58" height="60" rx="8" fill="{{tint3}}" opacity=".85"></rect>
    <circle cx="621" cy="330" r="19" fill="{{primary}}" opacity=".9"></circle>
    <rect x="664" y="295" width="44" height="54" rx="8" fill="{{tint2}}" opacity=".7"></rect>
    <rect x="732" y="279" width="52" height="70" rx="8" fill="{{deep}}" opacity=".85"></rect>
    <circle cx="833" cy="317" r="21" fill="{{primary}}" opacity=".6"></circle>
    <rect x="862" y="289" width="34" height="60" rx="8" fill="{{tint3}}" opacity=".9"></rect>
  </svg>
  <!--HERO--><!--/HERO-->
  <div style="position: absolute; left: 58px; bottom: 34px; width: 150px; height: 8px; background: {{primary}}; border-radius: 4px; z-index: 1;"></div>
</div></body></html>
"""

TPL_RETAIL_TAG = """\
<!doctype html>
<html><head><meta charset="utf-8">
<style>
html,body{margin:0;padding:0;}
*{-webkit-font-smoothing:antialiased;}
</style></head>
<body><div style="width: 900px; height: 383px; position: relative; overflow: hidden; background: {{dark}}; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;">
  <svg width="900" height="383" viewBox="0 0 900 383" style="position:absolute;left:0;top:0;">
    <defs><clipPath id="rt-box"><rect x="0" y="0" width="900" height="383"></rect></clipPath></defs>
    <g clip-path="url(#rt-box)">
      <path d="M 560 -60 L 960 -60 L 960 443 L 250 443 Z" fill="{{primary}}"></path>
      <circle cx="800" cy="42" r="19" fill="{{dark}}"></circle>
      <path d="M 675 305 l 30 30 M 705 305 l -30 30" stroke="#ffffff" stroke-width="9" stroke-linecap="round" opacity=".9"></path>
      <rect x="630" y="344" width="100" height="9" rx="4" fill="{{tint2}}" opacity=".75"></rect>
      <rect x="630" y="362" width="64" height="9" rx="4" fill="{{tint2}}" opacity=".5"></rect>
    </g>
  </svg>
  <!--HERO--><!--/HERO-->
  <div style="position: absolute; left: 0; bottom: 0; width: 900px; height: 12px; background: {{primary}}; z-index: 1;"></div>
</div></body></html>
"""

TPL_RETAIL_BAG = """\
<!doctype html>
<html><head><meta charset="utf-8">
<style>
html,body{margin:0;padding:0;}
*{-webkit-font-smoothing:antialiased;}
</style></head>
<body><div style="width: 900px; height: 383px; position: relative; overflow: hidden; background: {{dark}}; font-family: 'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;">
  <svg width="900" height="383" viewBox="0 0 900 383" style="position:absolute;left:0;top:0;">
    <circle cx="850" cy="437" r="165" fill="{{primary}}" opacity=".22"></circle>
    <g transform="translate(650,120) scale(1.15)">
      <path d="M 28 78 L 202 78 L 186 246 L 44 246 Z" fill="{{primary}}"></path>
      <path d="M 78 78 V 52 a 37 37 0 0 1 74 0 V 78" stroke="{{tint2}}" stroke-width="11" fill="none" stroke-linecap="round"></path>
      <circle cx="92" cy="146" r="15" fill="{{tint2}}" opacity=".9"></circle>
      <circle cx="140" cy="176" r="21" fill="{{tint2}}" opacity=".65"></circle>
      <rect x="112" y="122" width="30" height="30" rx="6" fill="{{tint2}}" opacity=".5"></rect>
    </g>
  </svg>
  <!--HERO--><!--/HERO-->
  <div style="position: absolute; left: 58px; bottom: 34px; width: 150px; height: 8px; background: {{primary}}; border-radius: 4px; z-index: 1;"></div>
</div></body></html>
"""

TEMPLATES = {"tech": TPL_TECH, "idea": TPL_IDEA,
              "steps": TPL_STEPS, "life": TPL_LIFE,
              "retail-shelf": TPL_RETAIL_SHELF,
              "retail-tag": TPL_RETAIL_TAG,
              "retail-bag": TPL_RETAIL_BAG}

# 'wide' layout puts the hero text left-aligned across nearly the full width
# (54px margins) with no competing right-side illustration column, so it can
# run much larger than the row/grid layouts without colliding with artwork.
# Each retail-* template reserves its own space for the illustration (a
# bottom band, a background block, or a bottom-right corner cutout) instead
# of relying on hero_html to dodge it, so the vertical anchor differs per
# template — WIDE_TOP supplies the default for each.
WIDE_TOP = {"retail-shelf": 138, "retail-tag": 191, "retail-bag": 148}


# --------------------------------------------------------------- color math
# Mirrors renderVals() in the .dc.html artboards so the PNG matches the canvas.
def _hx(c):
    s = str(c).lstrip('#')
    if len(s) == 3:
        s = ''.join(ch * 2 for ch in s)
    return [int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)]


def _th(a):
    return '#' + ''.join('%02x' % max(0, min(255, int(round(v)))) for v in a)


def mix(a, b, t):
    A, B = _hx(a), _hx(b)
    return _th([A[i] + (B[i] - A[i]) * t for i in range(3)])


def rot(c, deg):
    r, g, b = [v / 255.0 for v in _hx(c)]
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    h = 0.0
    if d != 0:
        if mx == r:
            h = ((g - b) / d) % 6
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
    h = (h * 60 + deg + 360) % 360
    lightness = (mx + mn) / 2
    s = 0 if d == 0 else d / (1 - abs(2 * lightness - 1))
    cc = (1 - abs(2 * lightness - 1)) * s
    x = cc * (1 - abs((h / 60) % 2 - 1))
    m = lightness - cc / 2
    if h < 60:
        p = [cc, x, 0]
    elif h < 120:
        p = [x, cc, 0]
    elif h < 180:
        p = [0, cc, x]
    elif h < 240:
        p = [0, x, cc]
    elif h < 300:
        p = [x, 0, cc]
    else:
        p = [cc, 0, x]
    return _th([(v + m) * 255 for v in p])


def vals(primary, dark):
    return {
        'primary': primary,
        'dark': dark,
        'tint1': mix(primary, '#ffffff', 0.30),
        'tint2': mix(primary, '#ffffff', 0.55),
        'tint3': mix(primary, '#ffffff', 0.80),
        'deep': mix(primary, dark, 0.55),
        'deeper': mix(primary, dark, 0.80),
        'ink': mix(dark, '#000000', 0.25),
        'paper': '#f6f1e7',
        'paper2': '#efe6d6',
        'terra': '#c0714b',
        'warm': '#e0a15c',
        'ana1': rot(primary, 42),
        'ana2': rot(primary, -46),
        'glowA': mix(rot(primary, 42), '#ffffff', 0.30),
        'glowB': mix(rot(primary, -46), '#ffffff', 0.20),
        'card': '#fbf7ef',
    }


HOLE = re.compile(r'\{\{(\w+)\}\}')
HERO = re.compile(r'<!--HERO-->.*?<!--/HERO-->', re.S)


def fill_holes(html, v):
    return HOLE.sub(lambda m: v.get(m.group(1), m.group(0)), html)


# ------------------------------------------------------------------ hero text
FONT_PRESETS = {
    'sans': FONT_STACK,
    'mashan': ("'Ma Shan Zheng','Noto Sans CJK SC','PingFang SC',sans-serif"),
    'zhimang': ("'Zhi Mang Xing','Noto Sans CJK SC','PingFang SC',sans-serif"),
    'longcang': ("'Long Cang','Noto Sans CJK SC','PingFang SC',sans-serif"),
}

FONT_WEIGHTS = {'sans': 900, 'mashan': 400, 'zhimang': 400, 'longcang': 400}


def hero_html(text, layout='grid', font='sans', font_scale=1.0, wide_top=150):
    """Return the absolutely-positioned hero grid for 1..N characters.

    The 4-character case is the designed one (2x2, 112px cells at 262/70);
    other counts fall back to a single row, or extra rows, that still reads
    as a deliberate lockup inside the central 383px crop square.

    layout='row' forces a single left-aligned row inside the free band
    between the left ornaments (x<=232) and the right illustration (x>=548).
    That band is only 296px wide, which caps how large the text can go
    before it collides with the illustration column — see the font-scale
    docs (1.85 is the practical ceiling for mashan in this layout).

    layout='wide' is for the retail-* templates: text runs left-aligned
    across nearly the full 900px canvas (54px margins, no reserved right
    column) because those templates put their illustration in a band,
    background block, or corner instead of a competing side column. This
    allows a much larger font-scale (roughly 1.5x the row-layout look)
    without any collision. wide_top sets the vertical center and should
    match the template's reserved illustration space (see WIDE_TOP).
    """
    n = max(1, len(text))
    if layout == 'wide' and n >= 1:
        gap = 14
        left = 54
        avail = 900 - left * 2
        cell = int((avail - gap * (n - 1)) / n)
        cols, size = n, int(cell * 0.94)
        top = int(wide_top - cell / 2)
    elif layout == 'row' and n >= 2:
        gap = 8
        cell = int((296 - gap * (n - 1)) / n)
        cols, size, left = n, int(cell * 0.94), 244
        top = int(189 - cell / 2)
    elif n == 1:
        cols, cell, gap, size, left, top = 1, 238, 14, 208, 262, 70
    elif n == 2:
        cols, cell, gap, size, left, top = 2, 152, 14, 140, 262, 116
    elif n == 3:
        cols, cell, gap, size, left, top = 3, 104, 12, 96, 262, 140
    elif n == 4:
        cols, cell, gap, size, left, top = 2, 112, 14, 104, 262, 70
    else:
        cols = 2
        rows = math.ceil(n / 2)
        cell = int((238 - 14 * (rows - 1)) / rows)
        gap = 14
        size = int(cell * 0.93)
        left = 262
        block = rows * cell + gap * (rows - 1)
        top = int(189 - block / 2)
    rows = math.ceil(n / cols)
    size = max(12, int(size * font_scale))
    face = FONT_PRESETS.get(font, FONT_STACK)
    weight = FONT_WEIGHTS.get(font, 900)
    spans = ''.join(
        '<span style="display: flex; align-items: center; justify-content: '
        "center; font-family: {ff}; font-weight: {fw}; font-size: {sz}px; "
        'line-height: 1; color: #ffffff; overflow: visible; '
        'white-space: nowrap;">{ch}</span>'.format(
            ff=face, fw=weight, sz=size, ch=ch)
        for ch in text)
    return (
        '<!--HERO--><div style="position: absolute; left: {l}px; top: {t}px; '
        'z-index: 3;">'
        '<div style="display: grid; grid-template-columns: repeat({c}, {q}px); '
        'grid-template-rows: repeat({r}, {q}px); gap: {g}px;">{s}</div>'
        '</div><!--/HERO-->'.format(l=left, t=top, c=cols, r=rows, q=cell,
                                    g=gap, s=spans))


def build(variant, text, primary, dark, layout='grid', font='sans',
          font_scale=1.0, wide_top=None):
    html = TEMPLATES[variant]
    if wide_top is None:
        wide_top = WIDE_TOP.get(variant, 150)
    html = HERO.sub(
        lambda _m: hero_html(text, layout, font, font_scale, wide_top),
        html, count=1)
    return fill_holes(html, vals(primary, dark))


def render(html, out):
    with sync_playwright() as p:
        browser = p.chromium.launch(args=['--font-render-hinting=none'])
        page = browser.new_page(viewport={'width': W, 'height': H},
                                device_scale_factor=2)
        page.set_content(html, wait_until='load')
        page.evaluate('() => document.fonts.ready')
        shot = page.screenshot(clip={'x': 0, 'y': 0, 'width': W, 'height': H})
        browser.close()
    img = Image.open(io.BytesIO(shot)).convert('RGB')
    if img.size != (W, H):
        img = img.resize((W, H), Image.LANCZOS)
    img.save(out, 'PNG')


def main(argv=None):
    ap = argparse.ArgumentParser(description='Render a WeChat 900x383 cover.')
    ap.add_argument('--text', required=True, help='hero characters (4 is ideal)')
    ap.add_argument('--out', required=True, help='output PNG path')
    ap.add_argument('--variant', default='tech',
                    choices=sorted(TEMPLATES), help='illustration motif')
    ap.add_argument('--layout', default='row', choices=('row', 'grid', 'wide'),
                    help='single row (default), 2x2 grid lockup, or wide '
                         '(full-width text for retail-* variants, supports '
                         'much larger font-scale — see --font-scale help)')
    ap.add_argument('--wide-top', type=int, default=None, dest='wide_top',
                    help='vertical center (px) for layout=wide; defaults '
                         'to the value tuned for each retail-* variant '
                         '(see WIDE_TOP), override only if you changed the '
                         'illustration')
    ap.add_argument('--font', default='sans', choices=sorted(FONT_PRESETS),
                    help='hero typeface: sans (default) or a calligraphy '
                         'face (mashan / zhimang / longcang)')
    ap.add_argument('--font-scale', type=float, default=1.0,
                    dest='font_scale',
                    help='multiplier on the hero font-size (default 1.0). '
                         'Cap depends on --layout: row/grid top out around '
                         '1.85 (mashan) before colliding with the '
                         'illustration column; wide has no such column and '
                         'comfortably takes ~1.3-1.6 for a 4-character '
                         'hero — push further only after checking a render.')
    ap.add_argument('--primary', default='#1a7f5a')
    ap.add_argument('--dark', default='#1c2b26')
    a = ap.parse_args(argv)

    text = a.text.strip()
    if not text:
        sys.stderr.write('error: --text is empty\n')
        return 2
    if len(text) != 4:
        sys.stderr.write(
            'warning: --text has %d characters; the layout is designed for 4. '
            'Rendering anyway with an adjusted grid.\n' % len(text))
    for name, value in (('primary', a.primary), ('dark', a.dark)):
        if not re.fullmatch(r'#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})', value):
            sys.stderr.write('error: --%s must be a hex color\n' % name)
            return 2

    if not 0.3 <= a.font_scale <= 3.0:
        sys.stderr.write('error: --font-scale must be between 0.3 and 3.0\n')
        return 2

    render(build(a.variant, text, a.primary, a.dark, a.layout, a.font,
                 a.font_scale, a.wide_top), a.out)
    print('wrote %s (%dx%d, variant %s)' % (a.out, W, H, a.variant))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
