# CoverageEval
This is the data and usage code for the dataset introduced in the paper "[Predicting Code Coverage without Execution](https://arxiv.org/abs/2307.13383)".

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
Check out this repository and install the necessary requirements

`git clone https://github.com/microsoft/coverage-eval.git`

`pip install -r requirements.txt`

## Usage
Access the coverage-augmented problems via the `read_problems()` function:

```
from utils import read_problems

problems = read_problems()
```

## Experimental Results

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

#### Multi Shot Experimentation
| Model                         | Match | Stmt | Branch | 
|-------------------------------|-------|-------|-------|
| OpenAI GPT-4 (gpt-4           | 30.04 | 90.5  | 22.5  |
| OpenAI GPT-3.5 (gpt-3.5-turbo)| 11.03 | 82.29 | 17.9  |
| Google BARD (text-bison-001)  | 21.56 | 85.66 | 20.52 |
| Anthropic Claude (claude-1.3  | 6.88  | 55.7  | 12.23 |
## Citation
Please cite using the following bibtex entry:

```
@misc{tufano2023predicting,
      title={Predicting Code Coverage without Execution}, 
      author={Michele Tufano and Shubham Chandel and Anisha Agarwal and Neel Sundaresan and Colin Clement},
      year={2023},
      eprint={2307.13383},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
```

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
