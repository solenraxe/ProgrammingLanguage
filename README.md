TECH STACK :
- Language : Python (100%)
- Libraries : Pygame (for the text editor window)
- IDE : Visual Studio Code

A.I. USE:
- Tried using claude for debugging once, didn't work (my code is too bad for it to understand 😔).

MOTIVATION :
I thought it'd be fun.
And I think it's cool
That's really it. 
I always felt like making a programming language from another programming language wouldn't be that hard, 11 hours later, I stand corrected.
I'll probably update this project in the future, when I feel something missing from another programming language.

Screenshots :

<img width="300" height="234" alt="image" src="https://github.com/user-attachments/assets/ee17f949-896a-4d2c-95be-65bffd9912e5" />
<img width="300" height="121" alt="image" src="https://github.com/user-attachments/assets/404429d6-20fb-437c-b2f7-1a899b55bd78" />

HOW IT WORKS :
When opening the app, you get a text editor display (made with pygame), you can type code in and execute it by either clicking the button or pressing F9, a complete documentation of the syntax and valid commands will be written below.
You can also load a script, save your current one, toggle fullscreen or clear all the code.
When you're done and click the Run button, a python script will read the text you typed, line by line, and convert it into python code to execute it.

SYNTAX :
- Object Type : Each object has a type attached to it, for example, nbr 50 is the number 50, txt 50 is the text "50" and so
    on. There's 6 object types as of now, Numbers (nbr/int), Decimals (dec/float), True or False (truth/bool), Text
    (txt/str), Variables (var) and Lists (list).
- Prints : You can print a variable or text by doing "print VARIABLENAME" or "print TEXT", those will then show up in the
    console.
- Variable Assignation : You can give certain objects names to re-use them later in the code
    var a = nbr 50 -> a is now equal to 50, print a puts 50 in the console.
    var a + nbr 100 -> a is now equal to 150 (50 + 100), print a puts 150 in the console.
    Existing operations are: = (equals); + (plus); - (minus); * (multiplication); / (division); ** (exponent); % (remainer)
- 
