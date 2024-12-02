import shutil


def prepare_deployment(output_file):
    print(f"Preparing deployment for output file: {output_file}")
    # Example: Copy the generated output to a deployment directory
    deployment_dir = "deployment"
    shutil.copy(output_file, deployment_dir)
    print("Deployment preparation completed.")
