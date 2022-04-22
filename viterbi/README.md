# assignment

Implement the `viterbi` method which takes a string, a mapping from letter to index, a mapping from hidden path letter
to index, a transition matrix and an emission matrix.  
The function should return the most likely hidden path.

# example

```python
>>> viterbi('yxzxx', {'z': 2, 'x': 0, 'y': 1}, {'B': 1, 'A': 0},
             [[0.24439433296892832, 0.7556056670310717], [0.24241542404217956, 0.7575845759578205]],
             [[0.7180611502606178, 0.19057500286653098, 0.09136384687285123],
              [0.291514305851776, 0.4407137316635376, 0.26777196248468643]])
'BBBBB'

>>> viterbi('yyyyzyxxxy', {'z': 2, 'x': 0, 'y': 1}, {'B': 1, 'A': 0},
             [[0.2915439583949658, 0.7084560416050342], [0.5443249998401023, 0.4556750001598978]],
             [[0.6496850841876853, 0.13086798248939702, 0.2194469333229175],
              [0.17166446158695747, 0.681506463779169, 0.14682907463387349]])
'BBBBABABAB'
```