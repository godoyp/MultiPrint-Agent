# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['multiprint_agent\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('multiprint_agent/config', 'multiprint_agent/config'), ('multiprint_agent/static', 'multiprint_agent/static'), ('multiprint_agent/certs', 'multiprint_agent/certs')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MultiPrintAgent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MultiPrintAgent',
)
