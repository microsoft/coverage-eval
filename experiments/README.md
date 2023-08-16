# CoverageEval Experiments

## Experiment Logs

#### Zero Shot Experimentation
| Model                         | Match | Stmt | Branch | 
|-------------------------------|-------|-------|-------|
| OpenAI GPT-4 (gpt-4           | 25.75 | 84.47 | 20.16 |
| OpenAI GPT-3.5 (gpt-3.5-turbo)| 0     | 39.87 | 8.33  |
| Google BARD (text-bison-001)  |  0    | 81.27 | 17.21 |
| Anthropic Claude (claude-1.3  | 3.9   | 84.47 | 20.07 |

#### One Shot Experimentation
| Model                         | Match | Stmt | Branch | 
|-------------------------------|-------|-------|-------|
| OpenAI GPT-4 (gpt-4           | 22.85 | 90.71 | 22.65 |
| OpenAI GPT-3.5 (gpt-3.5-turbo)|  8.17 | 76.53 | 17.17 |
| Google BARD (text-bison-001)  |  1.87 | 86.93 | 19.63 |
| Anthropic Claude (claude-1.3  |  4.83 | 83.21 | 19.16 |

#### Multi (6) Shot Experimentation
| Model                         | Match | Stmt | Branch | 
|-------------------------------|-------|-------|-------|
| OpenAI GPT-4 (gpt-4           | 30.04 | 90.5  | 22.5  |
| OpenAI GPT-3.5 (gpt-3.5-turbo)| 11.03 | 82.29 | 17.9  |
| Google BARD (text-bison-001)  | 21.56 | 85.66 | 20.52 |
| Anthropic Claude (claude-1.3  | 6.88  | 55.7  | 12.23 |

## Prompting the Model
We provide input to all the models with the same prompt structure. We begin each request to the model with the following instructions:

```
You are a terminal.
Instruction:
When use runs:
`coverage run -m  pytest code.py`
then you'll cat the file `code.py`, with each line starting with either of the two symbols below:

> if the line is executed
! is the line is not executed

Example output:

> line1
! line2
> line3
...
> linen

You job is to figure out which line will be executed given different test cases.


```
We append the specific input for a given problem to the end of this system prompt to get its coverage prediction from the model. 


## Model Input
### Zero Shot Input
The following is an example of the input for the zero shot experiment. It is appended to the end of the prompt above. 

```
(anaconda3-2020.11) ➜ cat code.py
def check_dict_case(dict):
    """
    Given a dictionary, return True if all keys are strings in lower 
    case or all keys are strings in upper case, else return False.
    The function should return False is the given dictionary is empty.
    Examples:
    check_dict_case({"a":"apple", "b":"banana"}) should return True.
    check_dict_case({"a":"apple", "A":"banana", "B":"banana"}) should return False.
    check_dict_case({"a":"apple", 8:"banana", "a":"apple"}) should return False.
    check_dict_case({"Name":"John", "Age":"36", "City":"Houston"}) should return False.
    check_dict_case({"STATE":"NC", "ZIP":"12345" }) should return True.
    """
    if len(dict.keys()) == 0:
        return False
    else:
        state = "start"
        for key in dict.keys():
            if isinstance(key, str) == False:
                state = "mixed"
                break
            if state == "start":
                if key.isupper():
                    state = "upper"
                elif key.islower():
                    state = "lower"
                else:
                    break
            elif (state == "upper" and not key.isupper()) or (state == "lower" and not key.islower()):
                    state = "mixed"
                    break
            else:
                break
        return state == "upper" or state == "lower"

(anaconda3-2020.11) ➜ cat test.py
def test():
        assert check_dict_case({}) == False, "1st edge test error: " + str(check_dict_case({}))

(anaconda3-2020.11) ➜ coverage run -m  pytest test.py
```

In the zero shot case, we provide the model with a function and one test case, and ask it to annotate the function based on which lines are executed (`>`), not executed (`!`) and unreachable (`-`) for the given test.

### One/Multi Shot Input
For the one and multi shot experiments, we provide the model with example annotations from other HumanEval problems before asking it to annotate the given problem. Here is an example of such a prompt, for the one shot learning experiment:
```
(anaconda3-2020.11) ➜ cat code.py
def numerical_letter_grade(grades):
    """It is the last week of the semester and the teacher has to give the grades
    to students. The teacher has been making her own algorithm for grading.
    The only problem is, she has lost the code she used for grading.
    She has given you a list of GPAs for some students and you have to write 
    a function that can output a list of letter grades using the following table:
             GPA       |    Letter grade
              4.0                A+
            > 3.7                A 
            > 3.3                A- 
            > 3.0                B+
            > 2.7                B 
            > 2.3                B-
            > 2.0                C+
            > 1.7                C
            > 1.3                C-
            > 1.0                D+ 
            > 0.7                D 
            > 0.0                D-
              0.0                E
    Example:
    grade_equation([4.0, 3, 1.7, 2, 3.5]) ==> ['A+', 'B', 'C-', 'C', 'A-']
    """
    letter_grade = []
    for gpa in grades:
        if gpa == 4.0:
            letter_grade.append("A+")
        elif gpa > 3.7:
            letter_grade.append("A")
        elif gpa > 3.3:
            letter_grade.append("A-")
        elif gpa > 3.0:
            letter_grade.append("B+")
        elif gpa > 2.7:
            letter_grade.append("B")
        elif gpa > 2.3:
            letter_grade.append("B-")
        elif gpa > 2.0:
            letter_grade.append("C+")
        elif gpa > 1.7:
            letter_grade.append("C")
        elif gpa > 1.3:
            letter_grade.append("C-")
        elif gpa > 1.0:
            letter_grade.append("D+")
        elif gpa > 0.7:
            letter_grade.append("D")
        elif gpa > 0.0:
            letter_grade.append("D-")
        else:
            letter_grade.append("E")
    return letter_grade

(anaconda3-2020.11) ➜ cat test.py
def test():
        assert numerical_letter_grade([1, 0.3, 1.5, 2.8, 3.3]) == ['D', 'D-', 'C-', 'B', 'B+']

(anaconda3-2020.11) ➜ coverage run -m  pytest test.py
> def numerical_letter_grade(grades):
>     """It is the last week of the semester and the teacher has to give the grades
>     to students. The teacher has been making her own algorithm for grading.
>     The only problem is, she has lost the code she used for grading.
>     She has given you a list of GPAs for some students and you have to write 
>     a function that can output a list of letter grades using the following table:
>              GPA       |    Letter grade
>               4.0                A+
>             > 3.7                A 
>             > 3.3                A- 
>             > 3.0                B+
>             > 2.7                B 
>             > 2.3                B-
>             > 2.0                C+
>             > 1.7                C
>             > 1.3                C-
>             > 1.0                D+ 
>             > 0.7                D 
>             > 0.0                D-
>               0.0                E
>     Example:
>     grade_equation([4.0, 3, 1.7, 2, 3.5]) ==> ['A+', 'B', 'C-', 'C', 'A-']
>     """
>     letter_grade = []
>     for gpa in grades:
>         if gpa == 4.0:
!             letter_grade.append("A+")
>         elif gpa > 3.7:
!             letter_grade.append("A")
>         elif gpa > 3.3:
!             letter_grade.append("A-")
>         elif gpa > 3.0:
>             letter_grade.append("B+")
>         elif gpa > 2.7:
>             letter_grade.append("B")
>         elif gpa > 2.3:
!             letter_grade.append("B-")
>         elif gpa > 2.0:
!             letter_grade.append("C+")
>         elif gpa > 1.7:
!             letter_grade.append("C")
>         elif gpa > 1.3:
>             letter_grade.append("C-")
>         elif gpa > 1.0:
!             letter_grade.append("D+")
>         elif gpa > 0.7:
>             letter_grade.append("D")
>         elif gpa > 0.0:
>             letter_grade.append("D-")
!         else:
!             letter_grade.append("E")
>     return letter_grade



(anaconda3-2020.11) ➜ cat code.py
def check_dict_case(dict):
    """
    Given a dictionary, return True if all keys are strings in lower 
    case or all keys are strings in upper case, else return False.
    The function should return False is the given dictionary is empty.
    Examples:
    check_dict_case({"a":"apple", "b":"banana"}) should return True.
    check_dict_case({"a":"apple", "A":"banana", "B":"banana"}) should return False.
    check_dict_case({"a":"apple", 8:"banana", "a":"apple"}) should return False.
    check_dict_case({"Name":"John", "Age":"36", "City":"Houston"}) should return False.
    check_dict_case({"STATE":"NC", "ZIP":"12345" }) should return True.
    """
    if len(dict.keys()) == 0:
        return False
    else:
        state = "start"
        for key in dict.keys():
            if isinstance(key, str) == False:
                state = "mixed"
                break
            if state == "start":
                if key.isupper():
                    state = "upper"
                elif key.islower():
                    state = "lower"
                else:
                    break
            elif (state == "upper" and not key.isupper()) or (state == "lower" and not key.islower()):
                    state = "mixed"
                    break
            else:
                break
        return state == "upper" or state == "lower"

(anaconda3-2020.11) ➜ cat test.py
def test():
        assert check_dict_case({}) == False, "1st edge test error: " + str(check_dict_case({}))

(anaconda3-2020.11) ➜ coverage run -m  pytest test.py

```

In the one shot example, we provide the model with an example annotation of the `numerical_letter_grade` HumanEval problem before asking it to annotate the `check_dict_case` problem.

## Model Output
The same problem (`check_dict_case`), has the following ground-truth output for the aforementioned (function, test) pair:
```
> def check_dict_case(dict):
>     """
>     Given a dictionary, return True if all keys are strings in lower 
>     case or all keys are strings in upper case, else return False.
>     The function should return False is the given dictionary is empty.
>     Examples:
>     check_dict_case({"a":"apple", "b":"banana"}) should return True.
>     check_dict_case({"a":"apple", "A":"banana", "B":"banana"}) should return False.
>     check_dict_case({"a":"apple", 8:"banana", "a":"apple"}) should return False.
>     check_dict_case({"Name":"John", "Age":"36", "City":"Houston"}) should return False.
>     check_dict_case({"STATE":"NC", "ZIP":"12345" }) should return True.
>     """
>     if len(dict.keys()) == 0:
>         return False
!     else:
!         state = "start"
!         for key in dict.keys():
!             if isinstance(key, str) == False:
!                 state = "mixed"
!                 break
!             if state == "start":
!                 if key.isupper():
!                     state = "upper"
!                 elif key.islower():
!                     state = "lower"
!                 else:
!                     break
!             elif (state == "upper" and not key.isupper()) or (state == "lower" and not key.islower()):
!                     state = "mixed"
!                     break
!             else:
!                 break
!         return state == "upper" or state == "lower"
```

A `>` symbol at the beginning of a line indicates the model predicts that the test will run this line of code. An `!` symbol indicates that the model predicts the test will not cause the line to be run. 
