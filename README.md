### [CactusCode](https://repl.it/@RealMrCameron/CactusCode) Info

Hopefully the final repository created to house my programming language made for the purposes of the cybersecurity project

CactusCode spawned from the StewCode language which was another project of mine of which's orginal idea was to be able to get people who wouldn't otherwise understand code to be able to understand what exactly the code is doing and by extension be able to code in that language. However, into the development of the project i had realised that i wasn't learning much new and therefore there wasn't as big an improvement in the quality of the programming in comparison to earlier projects as there could have been. Enter EngineerMan (Youtube). Whilst scrolling through one of his streams i came accross a stream in which you were taught the fundamentals of creating an interpreter in python as well as a very efficient way of doing so. Now enter CactusCode. The most original version of CactusCode is indeed a product of that stream however through research, idea thinking and error handling, CactusCode has become so much more! The idea of the name 'CactusCode' was because one of classmates has somewhat of an infatuation with Cacti and so i thought it fitting to have a singular random thought shape the future of my cybersecurity project
***
Urgent list to-do lurkers:

* Still need to add loops using regex with `repeat`
* Still need to add the `cleanValue()` for directly setting variables as opposed to referencing them
* Still need to add calculations procedurally when it comes to variables. All non-int/non-float values being likened to strings to avoid compilation problems
* Still need to add `if`, `then` and `default to` using regex

As well as non-urgent list to-do lurkers:

* Add `@extend{@Jess}`, `@extend{@Sherlock}` and `@extend{@Janitor}`
* Jess compiler extension shows errors/things when/where they shouldn't be
* Sherlock compiler extension adding cybersecurit/puzzle features such as regex, bruteforce cipher cracks etc
* Janitor compiler extension to as opposed to tell you where errors are, remove them for you (cleaning your code)
***
### 26.04.2020

Release Notes

* The creation of and storing of code in subroutines is now implemented with the help of regex. Something that it would have taken me marginally longer to figure out if it weren't for the aforementioned regex.
* Setting variables, placeholders etc are now implemented using a cleanValue subroutine which simply replaces the values as they are procedurally. I thought this much easier than just doing a traceback whenever i needed to find the value of something from a variable set to another variable.
* The compiler is now a work in progress as opposed to something that wouldn't happen. Although currently i'm using it as just a text editor. At some point, because of my implementation of the syntax highlighting, i find myself wanting to remove the idea of other language being in there and focusing on it just being an IDE for CactusCode.
