from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
	( 'design/connect4.kv', './design/' ),
	( 'design/dotsandboxes.kv', './design/' ),
	( 'design/tiktactoe.kv', './design/' ),
    ( 'design/gui.kv', './design/' ),

	( 'game_logic/connect4AI/qtables/easy.txt', './game_logic/connect4AI/qtables/' ),
	( 'game_logic/connect4AI/qtables/medium.txt', './game_logic/connect4AI/qtables/' ),
	( 'game_logic/connect4AI/qtables/hard.txt', './game_logic/connect4AI/qtables/' ),
	( 'game_logic/connect4AI/qtables/league.txt', './game_logic/connect4AI/qtables/' ),

	( 'game_logic/dotsandboxesAI/qtables/easy.txt', './game_logic/dotsandboxesAI/qtables/' ),
	( 'game_logic/dotsandboxesAI/qtables/medium.txt', './game_logic/dotsandboxesAI/qtables/' ),
	( 'game_logic/dotsandboxesAI/qtables/hard.txt', './game_logic/dotsandboxesAI/qtables/' ),
	( 'game_logic/dotsandboxesAI/qtables/league.txt', './game_logic/dotsandboxesAI/qtables/' ),

    ( 'images/connect4/*', './images/connect4' ),
    ( 'images/dotsandboxes/*', './images/dotsandboxes' ),

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
          console=False )
