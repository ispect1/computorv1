# ComputorV1

Installation
---
```shell script
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

Usage
---
```
python comptor.py [-h] [-c] [-d] [-i] [equation]
```

Examples
---
```
> python computor.py
> python computor.py "X^2+X-2=0"
> python computor.py "X^2+1/9-2/3*X=0" -c
```

If everything is bad, use magic (Docker required)
---
```shell script
sh runcmd.sh
```