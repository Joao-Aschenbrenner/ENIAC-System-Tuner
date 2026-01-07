@echo off
chcp 65001 >nul
title Desinstalador ENIAC System Tuner v4.0
echo ========================================
echo    DESINSTALADOR ENIAC SYSTEM TUNER
echo ========================================
echo.
echo AVISO: Isso removerá completamente o ENIAC System Tuner.
echo.
set /p confirm="Digite 'S' para confirmar desinstalação: "
if /i "%confirm%" neq "S" (
    echo.
    echo Desinstalação cancelada.
    pause
    exit /b
)

echo.
echo Parando processos do ENIAC...
taskkill /f /im python.exe /t 2>nul
timeout /t 2 /nobreak >nul

echo Removendo arquivos...
rmdir /s /q "C:\Program Files\ESTU" 2>nul

echo Removendo atalhos...
del "%USERPROFILE%\Desktop\ENIAC System Tuner.lnk" 2>nul
del "%USERPROFILE%\Desktop\ENIAC System Tuner.url" 2>nul

echo Removendo do registro...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\ENIACSystemTuner" /f 2>nul

echo.
echo ========================================
echo    DESINSTALAÇÃO CONCLUÍDA!
echo ========================================
echo.
echo O ENIAC System Tuner foi removido do sistema.
echo.
pause
