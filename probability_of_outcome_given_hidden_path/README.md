# assignment

Implement the `probability_outcome_hidden_path` method which takes a string, a mapping from letter to index,
a hidden path, a mapping from hidden path letter to index and an emission matrix.  
The function should return the probability of the emitted path.

# example

```python
>>> probability_outcome_hidden_path('xxyzyxzzxzxyxyyzxxzzxxyyxxyxyzzxxyzyzxzxxyxyyzxxzx', {'x':0,'y':1,'z':2}, 'BBBAAABABABBBBBBAAAAAABAAAABABABBBBBABAABABABABBBB', {'A':0, 'B':1}, [[0.612, 0.314, 0.074],[0.346, 0.317, 0.336]])
1.93157070893e-28
>>> probability_outcome_hidden_path('zyyyxzxzyyzxyxxyyzyzzxyxyxxxxzxzxzxxzyzzzzyyxzxxxy', {'x':0,'y':1,'z':2}, 'BAABBAABAABAAABAABBABBAAABBBABBAAAABAAAABBAAABABAA', {'A':0, 'B':1}, [[0.093, 0.581, 0.325],[0.77, 0.21, 0.02]])
3.42316482177e-35
>>> probability_outcome_hidden_path('yxyxxyyxxxyyzzyyyxzxzyyxzyzzzzxzzzzxzxxxyxxzzyzyyz', {'x':0,'y':1,'z':2}, 'ABBBAAAAABAABAABABBABAAABBBABBAAABAAABABAAAAAAAAAB', {'A':0, 'B':1}, [[0.442, 0.119, 0.439],[0.721, 0.022, 0.257]])
1.2100173973246485e-30
```