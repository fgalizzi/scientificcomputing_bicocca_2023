from setuptools import setup, find_packages

setup(name="wf_analyzer",
      description="Analyze waveforms of the DUNE PDS",
      author="Federico Galizzi",
      version="1.0",
      packages=find_packages(),
      install_requires=["numpy", "scipy", "struct", "multiprocessing", "tqdm"])
