Question selection algorithm

Things to consider
 - a new user with no state, what questions are provided to him/her
 - a user with no current session, whould their progress be based on their progress record or current session

Information required
 - flag a word as being studied in the current session
 - number of times successfully studied in the current session
 - word weight

Basic algorithm
 - user submits answer
 - system analyses the result and adjusts the weight
 - new words may be selected if number of words is below a threshold

Result analysis
 - if answer is wrong
     - push down the weight of the one they got wrong and of the word they selected
 - if answer is right
     - push up the weight of the one they got right and increment times studied
     - if number of times successfully studied is over a threshold
          - Remove it from the studied item list

New word selection
 - select word with lowest attempt value
