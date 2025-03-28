{
  description = "Python Shell";
  inputs = {
    nixpkgs.url = "nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShell =
          with pkgs;
          mkShell rec {
            venvDir = ".venv";

            packages =
              with pkgs;
              [
                python313
                poetry
                portaudio
                stdenv.cc.cc.lib
                pre-commit
                nodejs
                jsbeautifier
              ]
              ++ (with pkgs.python313Packages; [
                pip
                venvShellHook
              ]);

            LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath packages;
          };
      }
    );
}
