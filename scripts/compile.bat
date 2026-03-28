@echo off
g++ -O3 fast_sieve.cpp -o fast_sieve.exe
if %errorlevel% neq 0 (
    echo Compilation Failed!
) else (
    echo Compilation Success! fast_sieve.exe is ready.
)
pause
