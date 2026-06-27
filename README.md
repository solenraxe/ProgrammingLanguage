SUPPORTED OS : Windows
| File | OS | Architecture |
|------|----|--------------|
| editor.exe | Windows | x86_64 |

TECH STACK :
- Language : Python (100%)
- Libraries : Pygame (for the text editor window), tKinter, OS
- IDE : Visual Studio Code

A.I. USE:
- Tried using Claude for debugging once, didn't work (my code is too bad for it to understand 😔), ended up not using any A.I generated code.

MOTIVATION :
I thought it'd be fun.
And I think it's cool.
That's really it. 
I always felt like making a programming language from another programming language wouldn't be that hard, 11+ hours later, I stand corrected.
I'll probably update this project in the future, when I feel something missing from another programming language.

Screenshot :

<img width="300" height="234" alt="image" src="https://github.com/user-attachments/assets/ee17f949-896a-4d2c-95be-65bffd9912e5" />

HOW IT WORKS :
When opening the app, you get a text editor display (made with pygame), making it was a lot of fun and not nearly as easy as I tohught, you can type code in it and execute the code by either clicking the button or pressing F9, a complete documentation will be written below with screenshots.
You can also load a script, save your current one, toggle fullscreen or clear all the code.
When you're done and click the Run button, a python script will read the text you typed, line by line, and convert it into python code to execute it.

DOCUMENTATION :
- Object Type : Each object has a type attached to it, for example, nbr 50 is the number 50, txt 50 is the text "50" and so
    on. There's 6 object types as of now, Numbers (nbr/int), Decimals (dec/float), True or False (truth/bool), Text
    (txt/str), Variables (var) and Lists (list).
  
    <img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/5a3f8bd8-ba53-4a81-8677-0236653652e3" />
    <img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/f320a4c8-cb3a-4a15-b8dd-5bdb53cd3d84" />
    <img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/0c9c09fe-5c4a-400c-b3e4-f9864b571d9f" />


- Prints : You can print a variable or text by doing "print VARIABLENAME" or "print TEXT", those will then show up in the
    console.
    
    <img width="400" height="250" alt="print" src="https://github.com/user-attachments/assets/d7ca77ef-446d-440a-a53a-5630a3ae51b5" />

- Variable Assignation : You can give certain objects names to re-use them later in the code
    var a = nbr 50 -> a is now equal to 50, print a puts 50 in the console.
    var a + nbr 100 -> a is now equal to 150 (50 + 100), print a puts 150 in the console.
    Existing operations are: = (equals); + (plus); - (minus); * (multiplication); / (division); ** (exponent); % (remainer)
    
    <img width="400" height="250" alt="variable" src="https://github.com/user-attachments/assets/9ced298f-cbb2-4804-99f8-dd429a0338a3" />

- For Loop : Do something x number of times
    for i 10 runs the following lines 10 times, each time the i variable increases by 1. You can also do for i 5,10 which starts at 10 and goes to 10 (not included)
    Or you could do for i 3,7,2 which goes from 3 to 7 but adds +2 each time instead of 1.
  
    <img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/01869922-f7a5-4ccd-925b-897d9765da58" />
    <img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/9f566b97-380b-4bf5-9d9f-e2b40332ecd7" />
    <img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/1a98e7a5-d0ce-4a19-9cd3-90d2aa856b18" />

- While Loop : Repeat something until a condition is met (!MIGHT CRASH IF CONDITION CAN NEVER BE FULLFILLED)
    while var a < int 10 will repeat the following lines until a is superior to 10.
  
    <img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/228bf7d0-dad2-48a5-a71b-940ea5310eb5" />

- Functions : When called, execute a small piece of code, you first have to tell the function what code to execute, then you can run it a lot of times without rewriting it.
    
    <img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/9593c7ef-0a11-4c8a-a055-d8fe6ed8cd49" />

- Imports : Run another script when called, so you can re-use function you wrote in another script in your current one.
  
    <img width="400" height="250" alt="image" src="https://github.com/user-attachments/assets/ae68ecc1-349b-48a8-af21-6016b4af95ec" />

DEMO VIDEO :
https://youtu.be/KExpSzZWDLg
