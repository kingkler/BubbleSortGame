
# BubbleSortGame
An interactive game coded in python which helps understand how the algorithm functions.

**Decomposition**

  The bubble sort program is broken into smaller steps:
  Generate a list of random numbers.
  Compare two adjacent values (at index i and i+1).
  Decide whether to swap based on the user’s choice.
  Advance the algorithm by updating the index or starting a new pass.
  Check if the list is sorted and mark completion.
  Visualize the list as a bar graph after each step.
  Update the interface (feedback, steps, history, visualization).

  
**Pattern Recognition**

  Bubble sort repeatedly performs the same pattern:
    Compare two neighboring numbers.
    If the left value is bigger than the right, a swap is needed.
    Step through the list until the largest value “bubbles up” to the end.
    Repeat the full pass until no swaps are needed.

    
**Abstraction**

  Shown to the user:
    A bar graph of the array.
    The two values being compared (highlighted).
    Feedback messages explaining correctness.
    Step count and history log.
    
  Hidden from the user:
    Internal variables (pass, i, loops).
    Matplotlib buffer and image generation.
    Behind-the-scenes state updates.
    Timing delays and Python logic.
  Only the essential learning actions—viewing, comparing, and deciding to swap—are shown.

  
**Algorithm Design**

  Input
  
  The user interacts by:
    Generate New List,
    Swap,
    Don't Swap,
    Auto Sort.
    
  Processing
  
  Which leads to functions getting called:
    Reads the array and current index.
    Compares the two numbers.
    Applies the user’s decision or the auto-sort rule.
    Updates the state (array, index, pass, steps, history).
    Creates a new visualization.
    
  Output
  
  The UI updates by:
    New list,
    Refreshed bar graph,
    Step number,
    Feedback,
    Sorting History.
    
![Rough Design](https://github.com/user-attachments/assets/10ba9c18-6053-4121-b3b7-e8f7182a1ea6)
