# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['QtTinySA.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pandas','setuptools', 'tk', 'wheel', 'zipp', 'pyyaml', 'packaging', 'altgraph', 'mkl', 'fortran', 'matlab'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    coll,
    name='QtTinySA.app',
    icon='tinySA.ico',
    bundle_identifier='top.n03.tinysa',
)