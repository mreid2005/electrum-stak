#!/bin/bash

NAME_ROOT=electrum-stak
PYTHON_VERSION=3.5.4

# These settings probably don't need any change
export WINEPREFIX=/opt/wine64
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=22

PYHOME=c:/python$PYTHON_VERSION
PYTHON="wine $PYHOME/python.exe -OO -B"


# Let's begin!
cd `dirname $0`
set -e

mkdir -p tmp
cd tmp

for repo in electrum-stak electrum-locale electrum-stak-icons; do
    if [ -d $repo ]; then
	cd $repo
	git pull
	git checkout master
	cd ..
    else
	URL=https://github.com/straks/$repo.git
	git clone -b master $URL $repo
    fi
done

pushd electrum-locale
for i in ./locale/*; do
    dir=$i/LC_MESSAGES
    mkdir -p $dir
    msgfmt --output-file=$dir/electrum.mo $i/electrum.po || true
done
popd

pushd electrum-stak
if [ ! -z "$1" ]; then
    git checkout $1
fi

#VERSION=`git describe --tags`
VERSION="3.0.5"
echo "Last commit: $VERSION"
find -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd

rm -rf $WINEPREFIX/drive_c/electrum-stak
cp -r electrum-stak $WINEPREFIX/drive_c/electrum-stak
cp electrum-stak/LICENCE .
cp -r electrum-locale/locale $WINEPREFIX/drive_c/electrum-stak/lib/
cp electrum-stak-icons/icons_rc.py $WINEPREFIX/drive_c/electrum-stak/gui/qt/

# Install frozen dependencies
$PYTHON -m pip install -r ../../deterministic-build/requirements.txt

$PYTHON -m pip install -r ../../deterministic-build/requirements-hw.txt

pushd $WINEPREFIX/drive_c/electrum-stak
$PYTHON setup.py install
popd

cd ..

rm -rf dist/

# build standalone and portable versions
wine "C:/python$PYTHON_VERSION/scripts/pyinstaller.exe" --noconfirm --ascii --name $NAME_ROOT-$VERSION -w deterministic.spec

# set timestamps in dist, in order to make the installer reproducible
pushd dist
find -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd

# build NSIS installer
# $VERSION could be passed to the electrum-stak.nsi script, but this would require some rewriting in the script iself.
wine "$WINEPREFIX/drive_c/Program Files (x86)/NSIS/makensis.exe" /DPRODUCT_VERSION=$VERSION electrum.nsi

cd dist
mv electrum-stak-setup.exe $NAME_ROOT-$VERSION-setup.exe
cd ..

echo "Done."
md5sum dist/electrum-stak*exe
