from functools import partial
from tqdm.auto import tqdm as _tqdm

tqdm = partial(
    _tqdm,
    dynamic_ncols=True,
    mininterval=0.2,
    leave=False,
    bar_format=(
        "{l_bar}{bar}| "
        "{n_fmt:>15}/{total_fmt:>15} "
        "[Time elapsed: {elapsed} < ETA: {remaining}, {rate_fmt}]"
    )
)

for i in tqdm(range(100000000)):
    continue

for i in tqdm(
    range(10000000),
    desc="Downloading",
    unit="file",
    dynamic_ncols=True,
    mininterval=0.2,
    leave=True,
    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [elapsed: {elapsed} < {remaining}, {rate_fmt}]"
):
    continue
