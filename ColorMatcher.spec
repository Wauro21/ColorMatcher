# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['ColorMatcher.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.datas += [('rsrcs\\icon.png', 'C:\\Users\\Mauricio_2\\Desktop\\ColorMatcher\\rsrcs\\icon.png', "DATA")]
a.datas += [('rsrcs\\icon.png', 'C:\\Users\\Mauricio_2\\Desktop\\ColorMatcher\\rsrcs\\color_picker_icon.png', "DATA")]
a.datas += Tree('DEPENDENCY_LICENSES', prefix='DEPENDENCY_LICENSES\\')
a.datas += [('LICENSE.txt', 'C:\\Users\\Mauricio_2\\Desktop\\SPLAMP_MOTOR\\LICENSE', "DATA")]
a.datas += [('COPYING_LESSER.txt', 'C:\\Users\\Mauricio_2\\Desktop\\SPLAMP_MOTOR\\COPYING.LESSER', "DATA")]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ColorMatcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['rsrcs\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ColorMatcher',
)
