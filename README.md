# Zero Width Steganography - WIP
`Steganography: the practice of concealing a file, message, image, or video within another file, message, image, or video.` ~ [Wikipedia](https://en.wikipedia.org/wiki/Steganography)

## Introduction
Since its inception (happened in 1499 by German abbot *Johannes Trithemius*), steganography has always been regarded as a powerful method of hiding text in plain sight. The clear advantage over encryption it's that, if used correctly, will raise absolutely no suspicion.

 ​​﻿​​﻿​​​​​﻿﻿​﻿​​﻿​​﻿﻿​​﻿​​​​﻿﻿​​﻿​​​​﻿﻿​​﻿​﻿​​﻿﻿​﻿﻿﻿​​​​﻿​​​​​​​﻿﻿﻿​﻿​​​​﻿﻿​​﻿​﻿​​﻿﻿﻿﻿​​​​​﻿﻿﻿​﻿​​​​​﻿​​​​﻿
Steganography is normally used in photos. Novadays, it takes very little so upload a photo into your favourite social network to sneeringly share some deep secret. But I wanted to take it a bit further.
Why not text? What if i told you that somewhere in this paragraph, there's a secret message hiding?﻿ ​​﻿​​﻿​​​​​﻿﻿​﻿​​﻿​​﻿﻿​​﻿​​​​﻿﻿​​﻿​​​​﻿﻿​​﻿​﻿​​﻿﻿​﻿﻿﻿​​​You couldn't tell, right?


So this is how I got the ispiration. Neat, isn't it?

## Looking for the right way
At this point I had to start tinkering on how I could concretize this project.
Snooping through Wikipedia, I started looking for characters that could be hidden inside text files without being too noticeable. Instantly, I was very surprising by discovering that Greek question marks (;) are very similar (if not completely unrecognizable!) to regular semicolons (;). I thought that maybe I could find a way to swap them in some clever way to hide text. But honestly, unless you are working with C/C++ code, how often do you use semicolons? (This similarity can be used to prank a programmer. Just replace every semicolon and watch him *-and his compiler-* go crazy)

So at this point, I was lost. There are *1,112,064 different characters* encoded by UTF-8. I mean, it's bound to create some very similar symbols, right? Sadly, after scrolling a while (a very long while) through the list of every character it dawned to me that this couldn't be the right path.

## The discovery
Almost ready to give up, my eyes noticed a very strange table named *General Punctuation*. There are some funky charactes in there, including parenthesis and asterisks. But the real interesting feature in that table is *Whitespaces*.

So, basically, *whitespaces* are special character that, as the name suggests, leave some space (usually, white) between characters. I started exploring them, toying with the idea of converting some text in space.
This could actually work, with the small limitation of actually adding some visible spacing inside the "container" text.

Some Googling later, I discovered that there are 2 different space characters that add no visible space to the file: *U+200B* **(ZERO WIDTH SPACE)** and *U+FEFF* **(ZERO WIDTH NO-BREAK SPACE)**. These characters are actually invisible to the user and don't show up while writing.
I still don't really understand how they could be legitimately used inside a document, but I chose to ride with this.

## How I did it
Now that I had everything, I could start working on the idea.

The first thing that I had to do was encode the input string into UTF-8, convert it in binary and "translate" it into a "custom" binary system, using those two magic charactes as 0 and 1. At this point, it's pretty easy to add the encoded string into a "container" file. This file is visually identical to the "source" file.
To decode an encrypted string, I just need to convert those strange spaces back into binary and decode them from Unicode. Pretty awesome, right?

# The code
I made two Python3 scripts:
1. `zerowidthspy.py` - the main module. Its name stands for *Zero Width Steganography [in] Python*
2. `zero-width-steganography.py` - a wrapper, built around the aforementioned module, to quickly encode/decode/clean files

Those next sections will explain how to use the second script.
## Encoding
You can either provide a file text or a string as a source file. The hidden text will be hidden in here.
Then you must provide some text that will be encrypted and hidden in the source. As for the source file, you can either supply it inline or load from a file.

You must then provide a destination file that will contain the hidden text.

The next step is to state where you want to put the hidden string inside the source text. The options are:
* *Top* - the hidden string will be put at the very beginning of the text file.
* *Bottom* - the hidden string will be put at the end the text file.
* *Nth* - the hidden text will be placed at the end of every nth line.
* *Lines* - the hidden text will be placed at the end of every specified line.
* *Random* - the hidden text will be placed in random positions all through the document.

If you either chose *Random* or *Nth* you must provide respectively the number of occurrences or how many lines you want to skip at every iteration

## Decoding
Like in *Encoding*, you must provide a file text as source and you can provide a file destination. If you chose to not do so, the decoded text (if found) will be shown in console.

If you use the *verbose* command, more infos about the found text will be given.

## Cleaning
The script also has the ability to clean a file containing hidden text. Just provide a source file and a destination. If you omit the destination, the source file will be overwritten.

## Logging and verbose mode
This script logs everything inside a log file named "zero-width-steganography.log". Furthermore, if you want to have more information on what the script is doing, use the *--verbose* parameter.


# Documentation
This code doesn't need any particular module. It will work with the pre installed packages.

**TODO**
