let
  overlay = self: super: {
    jita = self.poetry2nix.mkPoetryApplication {
      projectDir = ./.;
      python = self.python3;
    };
  };
  hostPkgs = import <nixpkgs> { overlays = [ overlay ]; };
  linuxPkgs = import <nixpkgs> { overlays = [ overlay ]; system = "x86_64-linux"; };
in
{
  inherit (hostPkgs) jita;

  docker = hostPkgs.dockerTools.streamLayeredImage {
    name = "jita";
    contents = [linuxPkgs.jita];
    config.Cmd = ["app"];
  };
}
