# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['QtTinySA.py'],
    pathex=[],
    binaries=[],
    datas=[('QtTSAprefs.db', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pandas','setuptools', 'tk', 'wheel', 'zipp', 'pyyaml', 'packaging', 'altgraph', 'mkl', 'fortran', 'matlab'],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='QtTinySA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity='Developer ID Application: Fujian Province Beacon Rescue Service Center (N7A447KD6D)',
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='QtTinySA.app',
    icon='tinySA.ico',
    bundle_identifier='top.n03.tinysa',
)