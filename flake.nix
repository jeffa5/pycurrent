{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    python = pkgs.python3;
    pypkgs = pkgs.python3Packages;
    fs = pkgs.lib.fileset;
    current = pkgs.python3Packages.buildPythonPackage {
      name = "current";
      src = fs.toSource {
        root = ./.;
        fileset = fs.unions[ ./pyproject.toml ./README.md ./src];
      };
      format = "pyproject";
      propagatedBuildInputs = [pypkgs.hatchling];
    };
    pycurrent = pkgs.python3.withPackages (ps: [current]);
  in {
    packages.${system} = {
      inherit current pycurrent;
    };

    devShells.${system}.default = pkgs.mkShell {
      packages = [python];
    };
  };
}
