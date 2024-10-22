## Jack Compiler
Compiler for the Jack Programming Language written in Python. Projects 10 and 11 of the [nand2tetris](https://github.com/paudsu01/nand2tetris) course.

## Prerequisites
* Need `python` installed.
* Clone the repo: `git clone git@github.com:paudsu01/nand2tetrisCompiler.git path/to/clone/to`
* If you do not have your ssh keys set up, you can download the compiler from [releases](https://github.com/paudsu01/nand2tetrisCompiler/releases). Download `v.Project11`.

## How to run the compiler
* Open terminal and `cd path/to/clone/to`
*  Run the compiler with either
    * `python main.py path/to/JackFile.jack` for a single `.jack` file
    * `python main.py path/to/directory/` for multiple `.jack` files in the specified directory.
   
#### Compiling a sample .jack file (`sampleFiles/Average/Main.jack`)
*  Compile the `sampleFiles/Average/Main.jack` inside the `sampleFiles/Average` directory with `python main.py sampleFiles/Average/Main.jack`.
*  This will produce `Main.vm` file inside the `sampleFiles/Average` directory.

#### Compiling a directory with multiple .jack files (`sampleFiles/Pong/`)
*  Compile all `.jack` files in the `sampleFiles/Pong` directory with `python main.py sampleFiles/Pong`.
*  This will produce multiple `.vm` files with the same names as their respective `.jack` files inside the `sampleFiles/Pong` directory.
  
## nand2tetris
You can find all my projects for the course [here](https://github.com/paudsu01/nand2tetris).

