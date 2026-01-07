@echo off
chcp 65001 >nul
title Verificador de Sistema ENIAC
echo ========================================
echo    VERIFICADOR DE SISTEMA
echo    ENIAC SYSTEM TUNER v4.0
echo ========================================
echo.
echo Verificando requisitos do sistema...
echo.

:: Verificar Windows
ver | find "Windows 10" >nul
if %errorlevel% equ 0 (
    echo ✅ Windows 10 detectado
) else (
    ver | find "Windows 11" >nul
    if %errorlevel% equ 0 (
        echo ✅ Windows 11 detectado
    ) else (
        echo ⚠️  Versão do Windows não suportada
    )
)

:: Verificar arquitetura
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo ✅ Sistema 64-bit
) else (
    echo ❌ Sistema 32-bit não suportado
)

:: Verificar Python
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ Python instalado
) else (
    echo ⚠️  Python não encontrado
)

:: Verificar permissões
net session >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Executando como administrador
) else (
    echo ❌ Execute como administrador!
)

echo.
echo ========================================
echo Verificação concluída!
echo.
pause
