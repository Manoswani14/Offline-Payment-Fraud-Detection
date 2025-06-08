# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_all

# Collect all packages and their data files
hidden_imports = [
    'imblearn',
    'imblearn.over_sampling',
    'imblearn._version',
    'sklearn',
    'sklearn.utils._cython_blas',
    'sklearn.utils._isfinite',
    'sklearn.utils._openmp_helpers',
    'sklearn.neighbors._quad_tree',
    'sklearn.tree._utils',
    'sklearn.utils._typedefs',
    'sklearn.utils._heap',
    'sklearn.utils._sorting',
    'sklearn.utils._vector_sentinel',
    'sklearn.utils._weight_vector',
    'sklearn.utils._typedefs',
    'sklearn.utils._cython_blas',
    'sklearn.utils._isfinite',
    'sklearn.utils._openmp_helpers'
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
