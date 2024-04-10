import os
import subprocess
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED
import pulumi_aws as aws

PY_VER = aws.lambda_.Runtime.PYTHON3D12

def zip_directory(source_folder, output_filename):
    # create directory for the output file if it doesn't exist
    output_dir = os.path.dirname(output_filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # create a zip file with the contents of the source folder
    with ZipFile(output_filename, 'w', ZIP_DEFLATED) as zipf:
        for folder, _, files in os.walk(source_folder):
            for file in files:
                zipf.write(os.path.join(folder, file),
                           os.path.relpath(os.path.join(folder, file), source_folder))


def install_dependencies_and_prepare_layer(requirements_path, layer_output_filename):
    with tempfile.TemporaryDirectory() as dependencies_folder:

        deps_dir = os.path.join(dependencies_folder, 'python/lib', PY_VER, 'site-packages')
        # Install dependencies into the layer directory
        subprocess.run(["pip3", "install", "-r", requirements_path, "-t", deps_dir], check=True)

        # Zip the layer directory
        zip_directory(dependencies_folder, layer_output_filename)

        return layer_output_filename

