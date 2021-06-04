{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.poetry

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
