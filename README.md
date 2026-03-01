# Cyber-Security---Crack-The-Cipher
Cyber Security - Crack The Cipher


## Explanation of the code and Assumptions made 

## The program is interactive such that it is a recurring loop (until the user enters exit) that is command based. User will interact in the terminal . 

The logic and assumptions is as follows: 
1) we initialize a global common frequencies pairing sorted in desc. order of letters in english to their frequencies from oxford emory

2) we then take the cipher text (with provided assumptions in mind) and clean it just in case (to upper) 

3) we compute the frequencies of alphabetic characters for the cipher text (ignoring special chars like punctuation) 

4) we sort the frequencies in desc. order using pythons built in sorted( ) funciton with reverse flag

5) we map cipher frequencies to common frequencies and provide the user the option to graph this relationship 

6) the user can make an initial mapping that will do pairwise frequency substitution based soley on frequency alignment 
    i.e. most frequent cipher char maps to (->) e the most frequent common character according to our source 

7) users are then given the option to manually interact with cipher via the assoc x y option this will do a reciprocal association s.t. 
    ... x->ox , y->oy, ox->x, oy->y ... 
    will become 
    ... x->y, y->x, ox->oy, oy->ox ... and we handle edge of a letter that origianly mapped to itself 

8) the user will continue to manually associate characters using the map and commmon trigrams - computed using the built in Counter and most_common functions 
as well as their current status of decryption using the show command 

9) user can quit the program with quit or exit when done 

- 9a) user can reset to origianl mapping with reset 
- 9b) user can check that the mapping is reciprocal using check comand 
