import os
import shutil
import subprocess
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

import pulumi

python_version = "python3.12"

supported_cloud_providers = ['aws', 'gcp']
cloud_provider = pulumi.Config().get('cloud_provider', 'aws').lower()
if cloud_provider not in supported_cloud_providers:
    raise ValueError(f"Unsupported cloud provider: {cloud_provider}. Supported providers: {supported_cloud_providers}")


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

        deps_dir = os.path.join(dependencies_folder, 'python/lib', python_version, 'site-packages')
        # Install dependencies into the layer directory
        subprocess.run(["pip3", "install", "-r", requirements_path, "-t", deps_dir], check=True)

        # Zip the layer directory
        zip_directory(dependencies_folder, layer_output_filename)

        return layer_output_filename


exclude = ['.venv', 'aws', 'gcp']


def prepare_code(source_folder, output_filename, cloud_provider='gcp'):
    if cloud_provider not in supported_cloud_providers:
        raise NotImplementedError(f'Cloud provider {cloud_provider} not supported. Supported providers: {supported_cloud_providers}')

    with tempfile.TemporaryDirectory() as tmp_code_folder:
        # Walk through all the files and dirs in the source_folder except the cloud_provider in general traversal
        for dirpath, dirnames, filenames in os.walk(source_folder):
            if cloud_provider in dirnames:
                dirnames.remove(cloud_provider)  # Remove cloud_provider to handle it separately later

            # Remove other directories and files in the exclude list from dirnames and filenames
            dirnames[:] = [d for d in dirnames if d not in exclude]
            filenames[:] = [f for f in filenames if f not in exclude]

            # Copy files to the temporary dependencies folder, maintaining directory structure
            for filename in filenames:
                # Source file path
                src_path = os.path.join(dirpath, filename)

                # Relative path of file to maintain directory structure
                relative_path = os.path.relpath(src_path, start=source_folder)
                dest_path = os.path.join(tmp_code_folder, relative_path)

                # Ensure directory exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Copy file
                shutil.copy2(src_path, dest_path)

        # Handle cloud_provider directory specifically if it exists
        cloud_provider_path = os.path.join(source_folder, cloud_provider)
        if os.path.exists(cloud_provider_path):
            for filename in os.listdir(cloud_provider_path):
                src_path = os.path.join(cloud_provider_path, filename)
                if os.path.isfile(src_path):
                    # Copy directly to the root of tmp_code_folder
                    dest_path = os.path.join(tmp_code_folder, filename)
                    shutil.copy2(src_path, dest_path)

        return zip_directory(tmp_code_folder, output_filename)
