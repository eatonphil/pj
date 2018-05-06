# pj

This is a small, hand-written library for encoding and decoding JSON
strings and objects in Python. I wrote it because I wanted a small
example to demonstrate the simplest hand-written parser techniques
and couldn't find any obvious results on Google.

### Use

```python
import pj

print(pj.to_string(pj.from_string('{"foo":{"bar":[1,2,3]}}')))
```

### Tests

```bash
python3 -m unittest
```