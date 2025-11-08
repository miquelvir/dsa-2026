# Building Google Maps

`Universitat Pompeu Fabra - Data Structures and Algorithms (DSA) - 2025/26`

# Get started

- Follow the [developer setup](./docs/DEVELOPER_SETUP.md) to configure your laptop.
- Use `make r` to run the project.
- Read the [problem statement](./docs/PROBLEM.md) and start implementing.

# Repository Contents

- [Problem statement](./docs/PROBLEM.md): explanation of what you need to build and deliver
- [Developer setup](./docs/DEVELOPER_SETUP.md): how to configure your laptop for development for the DSA course
- [Report](./docs/REPORT.md): document where you need to write your report
- [.github/workflows/unit-tests.yml](./.github/workflows/unit-tests.yml): script to run tests when pushing to GitHub (CI)
- [maps](./maps/): datasets of different maps you can use for testing your project
- [maps_builder](./maps_builder/README.md): useful scripts to build your own maps
- [Makefile](./Makefile): file defining what `make` commands are used to run the code from the CLI

# Commands

## How to run

```zsh
make r
```

## How to run unit tests

```zsh
make t
```

## How to format the code

```zsh
make f
```

## How to use Valgrind to check for memory leaks

```zsh
make v
```

## How to debug

```zsh
make d
```

You can also use `make dt` to debug the unit tests.

Then, you can:
- Start the program
```zsh
run
```

- View the call stack
```zsh
backtrace
```

- Move through the call stack
```zsh
up
down
```

- Print a variable
```zsh
print x
```

- Print a structure
```zsh
display *x
```

- Add breakpoint
```zsh
break myfile.c:42
```

## How to remove temporary files
```zsh
make c
```

## How to run unit tests in GitHub

When you push to GitHub, your [unit tests will automatically run](.github/workflows/unit-tests.yml). Check out the results and logs in the Actions tab of your repository (in GitHub).
