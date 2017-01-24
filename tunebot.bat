@echo off
setlocal enabledelayedexpansion

for /l %%i in (1, 1, 3) do (
	for /l %%x in (0, 2, 98) do (
		set /a num = %%x/2
		echo generation %%i game !num!
		set /a a= %%x+1
		start runengine.bat
		start runtunebot.bat 3000 %%x
		python Player.py 3001 !a!
		python bottuner.py %%x
	)
	python evolution.py
	del winners.txt
)


