# IGPS
Image Generation And Programming Scripts for Poleg BMC

## How to use
IGPS is written for Python 2.7

Please make sure you have it installed and added to your %PATH%.

If you are a windows user, the following tools are available as exe files inside the package.

For Linux users please download and compile the follwonig tools:

### 1.	Bingo
https://github.com/Nuvoton-Israel/bingo
This tool is meant to be used instead of FlashTool. 
The main difference between the Bingo and FlashTool, is that Bingo is a generic tool that can build any header. 
The Header format and contents are defined on an external xml file.
There is nothing Poleg specific on the tool itself. We will use it, as is, on Arbel too. 
For example if we decide to add a new field to the BootBlock header, we only need to update the xml. 
More details and a basic set of examples are available on the link above.

### 2.	SignIt
https://github.com/Nuvoton-Israel/sign-it
Wrapper app for OpenSSL. 


### 3.	UUT
https://github.com/Nuvoton-Israel/uart-update-tool
Used for programing the flash using the Poleg ROM UFPP mode.

Download and compile these three tools. The first tools should be placed inside ./ImageGeneration
The last tool should be placed inside ./ImageProgramming.

## Notes about input files
All the files in this package are used for EB. For other vendors, please contact tali.perry@nuvoton.com. 

## How to execute:

### Image generation:
```
python ./UpdateInputsBinaries_EB.py
python ./GenerateAll.py
```

### Image programming:
Connect a serial port (via COM port or USB to Serial) to Serial Interface 2
Set strap9 to active low and issue power-on reset
```
python ./ProgramAll_Basic.py
```
