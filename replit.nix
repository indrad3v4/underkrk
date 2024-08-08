{ pkgs }: {
  deps = [
    pkgs.zlib
    pkgs.tk
    pkgs.tcl
    pkgs.openjpeg
    pkgs.libxcrypt
    pkgs.libwebp
    pkgs.libtiff
    pkgs.libjpeg
    pkgs.libimagequant
    pkgs.lcms2
    pkgs.freetype
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.stdenv
    pkgs.python38Packages.python
    pkgs.python38Packages.pip
  ];
}
