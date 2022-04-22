# Assignment

Implement the `probability_path` method which takes a string, a mapping from letter to index and a transition matrix.  
The function should return the probability of the given path.

# Example

```python
>>> probability_path('BABAA', {'B': 1, 'A': 0}, [[0.24439433296892832, 0.7556056670310717], [0.24241542404217956, 0.7575845759578205]])
0.005425963151164815

>>> probability_path('AABABABAAA', {'B': 1, 'A': 0}, [[0.3981195623715506, 0.6018804376284493], [0.3924198144356077, 0.6075801855643923]])
0.00041571340299273414
```
