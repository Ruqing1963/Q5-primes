@echo off
title Titanic Prime Mine - Ultra Sieve V4
color 0E

echo [Phase 1/3] Starting C++ 1-Billion-Depth Sieve...
fast_sieve.exe

echo [Phase 2/3] Packing Diamond-Grade Targets...
python build_targets.py

echo [Phase 3/3] Commencing PFGW Refinement...
if exist pfgw64.exe (
    :: 注意：这里去掉了 -q，直接让 pfgw 处理文件
    pfgw64.exe pfgw_targets.txt -l"pfgw_results.log"
) else (
    echo [ERROR] pfgw64.exe is missing in this folder!
)

echo.
echo =======================================================
echo EXTRACTION FINISHED. Check pfgw_results.log.
echo =======================================================
pause
