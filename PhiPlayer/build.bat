python -m nuitka player.py --include-module=View,integrated --enable-plugin=qt-plugins --mingw --standalone
copy ./assets player.dist/
