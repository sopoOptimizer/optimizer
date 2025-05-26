@echo off
echo Running bcdedit optimizations...
bcdedit /set bootux disabled
bcdedit /set tscsyncpolicy enhanced
bcdedit /set uselegacyapicmode No
echo All bcdedit commands executed successfully.
pause
