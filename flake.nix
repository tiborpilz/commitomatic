{
  description = "ChatGPT Commit Message Generator";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    {
      # Nixpkgs overlay providing the application
      overlay = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
      ];
    } // (flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlay ];
        };
      in
      rec {
        packages.flakeRepl = pkgs.writeShellScriptBin "repl" ''
          confnix=$(mktemp)
          echo "builtins.getFlake (toString $(git rev-parse --show-toplevel))" >$confnix
          trap "rm $confnix" EXIT
          nix repl $confnix
        '';

        packages.chatgpt-commit-messages = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          preferWheels = true;
        };

        apps = {
          repl = flake-utils.lib.mkApp { drv = packages.flakeRepl; };
          ccm = flake-utils.lib.mkApp { drv = packages.chatgpt-commit-message; };
        };

        defaultApp = apps.ccm;

        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            (python310.withPackages (ps: with ps; [ poetry setuptools ]))
          ];
        };
      }));
}
