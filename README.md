# Ant-Colony-Optimization
Ant Colony Optimization (ACO) for Job Shop Scheduling Problem.


## Execution:
### Initial requirements:
* Pytho 3.8.2
* Venv (sudo apt install python3.8-venv)
* pip (sudo apt install python3-pip)

### Initial setup:
1. Create enviroment:    `python3 -m venv ./code/venv`
2. Activate enviroment:  `cd code && source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

### Execute:
1. Activate enviroment:  `cd code && source venv/bin/activate`
2. Execute: `python3 main.py`
3. Exit: `deactivate`


### Input:
The optimized parameters are at the beginning of the main file, change at will.

### Output:
When executing the algorithm, the time of the best schedule will be printed. A *ACO_cycles_results.json* file will also be generated, where all time results per cycles will be recorded with the following order: the fastest, the average and the longest time.


## Data:
The test instances used for exeperiments on documentation are in <b>/test_instances</b>. <br><br>
These instances are from a contribution to the [OR-Library by Dirk C. Mattfeld and Rob J.M. Vaessens](http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/jobshop1.txt)


## References:
* [FLÓREZ, Edson; GÓMEZ, Wilfredo; BAUTIST, Lola. An ant colony optimization algorithm for job shop scheduling problem. Universidad Industrial de Santander, Bucaramanga, Colombia. arXiv:1309.5110, 2013](https://arxiv.org/ftp/arxiv/papers/1309/1309.5110.pdf)

* [COLORNI, A.; DORIGO, M.; MANIEZZO, V.; TRUBIAN, M. Ant system for Job-shop scheduling. JORBEL - Belgian Journal of Operations Research, Statistics, and Computer Science, v. 34, n. 1, p. 39-53, 1 jan. 1995.](https://www.orbel.be/jorbel/index.php/jorbel/article/view/169/125)
