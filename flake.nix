# mastodon-markov — Nix dev shell
#
# Provides Python 3 for any post-processing scripts that might need
# to run outside of the Rust binary (e.g. corpus pre-processing).
# The Rust toolchain itself is expected to come from rustup, not nixpkgs.

{
  description = "mastodon-markov — Markov chain bot for Mastodon";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in {
      devShells = forAllSystems (system:
        let pkgs = nixpkgs.legacyPackages.${system}; in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              python3
              python3Packages.pip
              python3Packages.virtualenv
            ];

            shellHook = ''
              echo "mastodon-markov dev shell ready (Python 3)"
            '';
          };
        }
      );

      # Keep formatting consistent across all Nix files in the project
      formatter = forAllSystems (pkgs: pkgs.nixfmt-rfc-style);
    };
}
