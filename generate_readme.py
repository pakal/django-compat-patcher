import os
import sys

src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.append(src_dir)

from compat_patcher_core.readme_generator import generate_readme
from django_compat_patcher.registry import django_patching_registry

def generate_dcp_readme():
    generate_readme(
        input_filename="README.in",
        output_filename="README.rst",
        patching_registry=django_patching_registry,
    )


if __name__ == "__main__":
    generate_dcp_readme()
