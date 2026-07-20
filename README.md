# dary-cuckoo-hashing

## 1. Installing Dependencies

Setup your environment.

```sh
pip install -r requirements.txt
```


## 2. Running Simulations

Run the main program. This will generate a directort containing the
runs organized by `OUTPUT_DIR/TABLE_SIZE/D_VALUE/LOAD_FACTOR.png`.

```sh
python main.py
```


## 3. Updating configuration

This project can be configured in `config.py`

```py
random.seed(1)

D_VALUES = [2, 3, 4, 5, 6, 7, 8, 9]
TABLE_SIZES = [1_000, 10_000, 100_000]
LOAD_FACTORS = [.4, .5, .6, .7, .8, .9, .99, .999, .9999]
N = 1_000
OUTPUT_DIR = "output/"
```

