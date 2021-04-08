from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
	( 'design/*.kv', './design/' ),

	( 'game_logic/connect4AI/qtables/*', './game_logic/connect4AI/qtables/' ),
	( 'game_logic/dotsandboxesAI/qtables/*', './game_logic/dotsandboxesAI/qtables/' ),
	( 'game_logic/tictactoeAI/qtables/*', './game_logic/tictactoeAI/qtables/' ),

    ( 'images/tictactoe/*', './images/tictactoe' ),
    ( 'images/connect4/*', './images/connect4' ),
    ( 'images/dotsandboxes/*', './images/dotsandboxes' )


]

a = Analysis(['main.py'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
             
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [('W ignore', None, 'OPTION')], # supposedly stops the virus warning
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='reinforcement',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)
