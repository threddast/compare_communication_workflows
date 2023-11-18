{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }: {
    overlay = nixpkgs.lib.composeManyExtensions [
      (final: prev: {
        myApp = prev.poetry2nix.mkPoetryApplication {
          projectDir = self;
        };
      })
    ];
  } // (flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [ self.overlay ];
      };
    in
    {
      apps = {
        inherit (pkgs) myApp;
      };

      defaultApp = pkgs.myApp;

      devShell =
        pkgs.mkShell {
          buildInputs = with pkgs.python3Packages; [ python venvShellHook ];
          packages = with pkgs; [ 
            poetry 
            jupyter 
            sqlitebrowser
            libreoffice
          ];
          venvDir = "./.venv";

          postVenvCreation = ''
            unset SOURCE_DATE_EPOCH
            poetry env use .venv/bin/python
            poetry install
          '';
          postShellHook = ''
            unset SOURCE_DATE_EPOCH
            poetry env info
          '';
          LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
        };
    }));
}
