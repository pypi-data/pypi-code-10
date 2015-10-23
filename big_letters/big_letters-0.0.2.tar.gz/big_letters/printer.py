from __future__ import print_function
import sys

letters = """
 ***
*   *
*****
*   *
*   *

****
*   *
****
*   *
****

 ****
*
*
*
 ****

****
*   *
*   *
*   *
****

*****
*
***
*
*****

*****
*
***
*
*

 ****
*
*  **
*   *
 ****

*   *
*   *
*****
*   *
*   *

***
 *
 *
 *
***

 ****
    *
    *
*   *
 ***

*  *
* *
**
* *
*  *

*
*
*
*
*****

*   *
** **
* * *
*   *
*   *

*   *
**  *
* * *
*  **
*   *

 ***
*   *
*   *
*   *
 ***

****
*   *
****
*
*

 ***
*   *
* * *
*  **
 *** *

****
*   *
****
*  *
*   *

 ****
*
 ****
     *
 ****

*****
  *
  *
  *
  *

*   *
*   *
*   *
*   *
 ***

*     *
*     *
 *   *
  * *
   *

*     *
*     *
*  *  *
*  *  *
 ** **

*   *
 * *
  *
 * *
*   *

*   *
 * *
  *
  *
  *

*****
   *
  *
 *
*****
"""

letters = letters.strip("\n")
lines = letters.split("\n")

letters= {}

space = ["     "] * 5

for i in range(26):
    letter_lines = lines[i * 6 : i * 6 + 5]
    char = chr(65 + i)
    letters[char] = letter_lines

for char, lines in letters.items():
    n = max(len(l) for l in lines)
    newl = []
    for l in lines:
        newl.append(l + (n - len(l)) * " ")
    letters[char] = newl


def print_big(words, fh=None):
    """prints given text `words` in big letters to given file handle `fh`.
    If `fh` is not given this function prints to the console.
    """
    if fh is None:
        fh = sys.stdout
    current_lines = [[] for _ in range(5)]
    for c in words.upper():
        for i, cii in enumerate(letters.get(c, space)):
            current_lines[i].append(cii)
        if max(sum(len(cii) for cii in cl) for cl in current_lines) > 70:
            for cl in current_lines:
                print("  ".join(cl), file=fh)
            print(file=fh)
            current_lines = [[] for _ in range(5)]
    for cl in current_lines:
        print("  ".join(cl), file=fh)
    print(file=fh)

if __name__ == "__main__":
    print_big("hello uwe schmitt")
