@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=_build
set LINKCHECKDIR=\%BUILDDIR%\linkcheck

if "%1" == "" goto help
if "%1" == "clean" goto clean
if "%1" == "pdf" goto pdf
@REM if "%1" == "simple-pdf" goto simple-pdf
if "%1" == "linkcheck" goto linkcheck

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:clean
rmdir /s /q %BUILDDIR% > /NUL 2>&1
for /d /r %SOURCEDIR% %%d in (_autosummary) do @if exist "%%d" rmdir /s /q "%%d"
goto end

@REM :pdf
@REM %SPHINXBUILD% -M latex %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
@REM cd "%BUILDDIR%\latex"
@REM for %%f in (*.tex) do (
@REM pdflatex "%%f" --interaction=nonstopmode)
@REM if NOT EXIST ansys-mechanical-core.pdf (
@REM 	Echo "no pdf generated!"
@REM 	exit /b 1)
@REM Echo "pdf generated!"

:pdf
%SPHINXBUILD% -M simplepdf %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
cd "%BUILDDIR%\simplepdf"
if NOT EXIST ansys-mechanical-core.pdf (
	Echo "no pdf generated!"
	exit /b 1)
Echo "pdf generated!"

:linkcheck
%SPHINXBUILD% -b %1 %SPHINXOPTS% %SOURCEDIR% %LINKCHECKDIR%
echo "Check finished. Report is in %LINKCHECKDIR%."
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd

