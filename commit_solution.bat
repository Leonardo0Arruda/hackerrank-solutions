@echo off
:: ─────────────────────────────────────────
:: commit_solution.bat
:: Uso: arraste um .py pra cima deste .bat
::      OU rode: commit_solution.bat "nome do problema"
:: ─────────────────────────────────────────

set PROBLEM=%~1

if "%PROBLEM%"=="" (
    echo.
    set /p PROBLEM="Nome do problema resolvido: "
)

echo.
echo [1/3] Atualizando README...
python update_readme.py

echo.
echo [2/3] Commitando...
git add .
git commit -m "feat: add solution - %PROBLEM%"

echo.
echo [3/3] Enviando pro GitHub...
git push

echo.
echo Pronto! Solucao publicada no GitHub.
pause
