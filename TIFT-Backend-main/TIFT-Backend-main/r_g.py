import time
from core.utils import MyGovClient

mg = MyGovClient()

def run_all_get_methods(method_args, repeat=5):
    methods = [
        (name, func) for name, func in vars(type(mg)).items()
        if callable(func) and name.startswith('get_') and not name.startswith('_')
    ]
    counters = {name: 0 for name, func in methods}
    for _ in range(repeat):
        for name, func in methods:
            try:
                args = method_args.get(name, [])
                kwargs = method_args.get(name + "_kwargs", {})
                print(f"{name}:")
                print(getattr(mg, name)(*args, **kwargs))
                counters[name] += 1
            except Exception as e:
                print(f"Error in {name}: {e}")
        print(f"Request counters so far: {counters}")
        time.sleep(3)
    print("Final request count:", counters)
    print("Total requests made:", sum(counters.values()))
