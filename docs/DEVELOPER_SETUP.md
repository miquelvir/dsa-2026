# Developer setup

## Linux

1. Install GCC
```zsh
sudo apt update
sudo apt install build-essential
sudo apt install gdb
sudo apt install valgrind
sudo apt install clang-format
gcc --version
```

2. [Clone the repository using VSCode](https://code.visualstudio.com/docs/sourcecontrol/intro-to-git#_clone-a-repository-locally)
   
3. Run `make r` and make sure you see this message: `Welcome to DSA!`

## MacOS

1. [Install homebrew](https://brew.sh/)

2. [Install GCC](https://formulae.brew.sh/formula/gcc#default)

3. [Install GDB](https://formulae.brew.sh/formula/gdb#default)

4. [Install make](https://formulae.brew.sh/formula/make#default)

5. [Install clang-format](https://formulae.brew.sh/formula/clang-format#default)

6. [Clone the repository using VSCode](https://code.visualstudio.com/docs/sourcecontrol/intro-to-git#_clone-a-repository-locally)
   
7. Run `make r` and make sure you see this message: `Welcome to DSA!`

## Windows

1. [Install WSL with Ubuntu](https://documentation.ubuntu.com/wsl/en/latest/guides/install-ubuntu-wsl2/) (Linux subsystem inside Windows)

2. Follow the instructions for [Linux](#linux) in a WSL terminal
