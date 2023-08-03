import os
import sys

src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.append(src_dir)

from django_compat_patcher import default_settings
from compat_patcher_core.readme_generator import generate_readme
from django_compat_patcher.registry import django_patching_registry

def generate_dcp_readme():

    # Insert default settings into final README

    with open("README.in") as f:
        data = f.read()

    default_settings_dict = vars(default_settings)
    data = data.format(**default_settings_dict)

    with open("README.in2", "w") as f:
        f.write(data)

    generate_readme(
        input_filename="README.in2",
        output_filename="README.rst",
        patching_registry=django_patching_registry,
    )
    os.remove("README.in2")



if __name__ == "__main__":
    generate_dcp_readme()
