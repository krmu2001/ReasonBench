from importlib import import_module


TASK_MODULES = {
  "game24": "reasonbench.tasks.game24",
  "hle": "reasonbench.tasks.hle",
  "hotpotqa": "reasonbench.tasks.hotpotqa",
  "humaneval": "reasonbench.tasks.humaneval",
  "logiqa": "reasonbench.tasks.logiqa",
  "matharena": "reasonbench.tasks.matharena",
  "scibench": "reasonbench.tasks.scibench",
  "sonnetwriting": "reasonbench.tasks.sonnetwriting",
}


def load_task(benchmark: str):
  try:
    return import_module(TASK_MODULES[benchmark])
  except KeyError:
    raise ValueError(f"No task module found for benchmark={benchmark}")

def load_all_tasks():
  for benchmark in TASK_MODULES:
    load_task(benchmark)

__all__ = ["load_task", "load_all_tasks"]