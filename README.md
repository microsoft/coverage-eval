# CoverageEval
This is the data and usage code for the dataset introduced in the paper "Predicting Code Coverage without Execution".

The CoverageEval dataset is an extension of the [HumanEval](https://github.com/openai/human-eval) dataset. We augment the problems in HumanEval with code coverage information for each test within the problem. We propose this dataset as a useful metric for evaluating Large Language Models, as code coverage prediction from LLMs can be seen as a proxy for code understanding. 

## Data
Each problem in the dataset is in its own JSON file (named based on the problem ID). The JSON structure for each file is:
```
{'problem_id': 
'problem':
'method': 
'tests': [
    {'test_id':
    'test':
    'coverage_executed':
    'coverage':
    'coverage_sequence': []
    'branch_sequence': []
    },
    . . .
]
}
```

## Installation
TODO installation instructions based on usage code

## Usage
TODO usage instructions based on usage code

## Citation
Please cite using the following bibtex entry:


## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
