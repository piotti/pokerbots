@echo off
setlocal enabledelayedexpansion


for /l %%x in (0, 1, 40) do (
	set /a num1 = %%x %% 2
	set /a num2 = !num1! + 1
	echo gen %%x
	start runengine.bat
	start runtunebot.bat 3000 %%num1
	python Player.py 3001 %%num2
	python bottuner.py %%x
	python evolution.py
	
)
del winners.txt

