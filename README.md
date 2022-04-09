# cjbAssembler

<!--
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url] -->
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- DESCRIPTION -->
  <p align="left">
    This is a simple compiler for my custom RISC processor, that can be found at <a href="https://github.com/c-biancone/cjbRISC">cjbRSIC</a>. It takes in `.txt` files containing Assembly-like code of a custom syntax, verifies them for correct structure and syntax, and then assembles them into Machine Code Memory Initialization Files  that the CPU can understand. These `.mif` files are uploaded to the Program Memory of the CPU in Intel Quartus at compile time, so that they can be loaded onto an FPGA board and run in hardware.
    <br />
    <a href="#usage"><strong>Jump to Usage»</strong></a>
  <br/>
    <a href="#about"><strong>Jump to About»</strong></a>
    <br />
    <br />
    <!-- <a href="https://github.com/github_username/repo_name">View Demo</a> -->
    ·
    <a href="https://github.com/c-biancone/cjbRISC/issues">Report Bug / Request Feature</a>
    ·
  </p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps:

### Prerequisites
* <a href = "https://www.python.org/downloads/">python3</a>
* NLTK tokenization
  * From python terminal:
    ```python
    import nltk
    nltk.download('punkt')
    ```

### Cloning

* Clone the repo into the desired directory
   ```sh
   git clone https://github.com/c-biancone/cjbAssembler.git
   ```
   
## Usage 
1. Open a terminal in the project directory.
2. Run the `cjbASM.py` file with input Assembly file and desired output .mif file name arguments, as follows:
    ```sh
    ./cjbASM.py ./dir/inASMname.txt ./dir/outMCname.mif
    ```
    or
    ```
    python cjbASM.py ./dir/inASMname.txt ./dir/outMCname.mif
    ```
    Ex:
    ```
    python cjbASM.py ./asm/HelloWorld.txt ./out/HelloWorld.mif
    ```
    These names may only contain alphanumeric characters.
    
3. The output .mif file can then be transferred to the `cjbRISC_Quartus` directory of the CPU repository for compilation.


# About
I decided on this project so I could have full-stack development control over this Computer system, from CPU archiitecture itself all the way to the tools used to compile the software that runs on it.

This assembler heavily relies on <a href="https://en.wikipedia.org/wiki/Regular_expression">Regular Expressions</a> to perform structure and syntax checking. These search patterns are stored in `expressions.py` for readability of the main code, since some of them are quite long. They also pull information from JSON dictionaries that contain information on the CPU register names and the operation codes it understands, so it will see if the programmer typed something other than what they were supposed to.

It first verifies the structure of the input code file, looking for certain assembler flags in a certain order. If this passes, it moves on to checking the syntax of the assembler directives, code constants, and actual code line by line. It skips over whitespace and comment lines designated by a ";", and will throw a SyntaxError if something is incorrect. For some instructions like LOAD and STORE, it performs preprocessing of offsets needed by the CPU.

The assembling step has been split into 2 loops, turning this into a 3-pass assembler. This was necessary to perform lookahead in the code section, to allow the JUMP instruction to jump forward and backward through the program to labels designated with a "@". The offset needed here is based on the CPU architecture as well as the number of instructions, and is calculated during the second assembly pass. Simpler instructions don't need these extra steps and have a simpler dictionary lookup and replacement process.

If all is sucessful, the user is presented with their machine code in the directopry of their choosing.

## Future 
This stage of the project was done with a goal of keeping the code line count as close to 100 as possible, which I think as far as raw code goes, I got about as close as I could. <120 lines of raw code for a fully functional assembler is pretty good, though I needed a few tricks to hit that. In the future when integrating this into my cjbRISC repo I will more closely adhere to good coding practice for readability instead of minimizing line count. That way it will be more easily extensible in the future, like for when adding directive use cases, etc.


<!-- CONTACT -->
## Contact

Chris Biancone - [email](chris.biancone@gmail.com)

Project Link: [https://github.com/c-biancone/cjbAssembler](https://github.com/c-biancone/cjbAssembler)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/chris-biancone
