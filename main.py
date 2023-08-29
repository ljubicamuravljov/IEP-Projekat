import subprocess


def build_dockerfile(dockerfile_path, image_name, build_args=None):
    command = ["docker", "build", "-t", image_name]

    if build_args:
        for key, value in build_args.items():
            command.extend(["--build-arg", f"{key}={value}"])

    command.append(dockerfile_path)

    try:
        subprocess.run(command, check=True)
        print(f"Successfully built Docker image: {image_name}")
    except subprocess.CalledProcessError:
        print("Error: Failed to build Docker image")


def deploy_kubernetes_manifest(manifest_path):
    try:
        subprocess.run(["kubectl", "apply", "-f", manifest_path], check=True)
        print(f"Successfully deployed Kubernetes manifest: {manifest_path}")
    except subprocess.CalledProcessError:
        print("Error: Failed to deploy Kubernetes manifest")









def main():
    # Replace these values with your actual paths and image names

    # Replace this with the actual path to your deployment.yaml file
    deployment_manifest_path = "C:/Users/Acer/OneDrive - student.etf.bg.ac.rs/FAKULTET/6. semestar/IEP/Projekat/deployment.yaml"

    deploy_kubernetes_manifest(deployment_manifest_path)


    dockerfile_path_1 = "C:/Users/Acer/OneDrive - student.etf.bg.ac.rs/FAKULTET/6. semestar/IEP/Projekat/authentication.dockerfile"
    image_name_1 = "authentication"
    # build_args_1 = {"ARG_NAME": "ARG_VALUE"}  # Optional build arguments

    dockerfile_path_2 = "C:/Users/Acer/OneDrive - student.etf.bg.ac.rs/FAKULTET/6. semestar/IEP/Projekat/authenticationDBMigration.dockerfile"
    image_name_2 = "authmigration"
    dockerfile_path_3 = "C:/Users/Acer/OneDrive - student.etf.bg.ac.rs/FAKULTET/6. semestar/IEP/Projekat/ownerApp.dockerfile"
    image_name_3 = "owner"
    dockerfile_path_4 = "C:/Users/Acer/OneDrive - student.etf.bg.ac.rs/FAKULTET/6. semestar/IEP/Projekat/courier.dockerfile"
    image_name_4 = "courier"
    dockerfile_path_5 = "C:/Users/Acer/OneDrive - student.etf.bg.ac.rs/FAKULTET/6. semestar/IEP/Projekat/customer.dockerfile"
    image_name_5 = "customer"
    dockerfile_path_6 = "C:/Users/Acer/OneDrive - student.etf.bg.ac.rs/FAKULTET/6. semestar/IEP/Projekat/shopMigration.dockerfile"
    image_name_6= "shopmigration"
    dockerfile_path_7 = "C:/Users/Acer/OneDrive - student.etf.bg.ac.rs/FAKULTET/6. semestar/IEP/Projekat/statistics.dockerfile"
    image_name_7= "statistics"

    build_dockerfile(dockerfile_path_1, image_name_1)
    print("authImage")
    build_dockerfile(dockerfile_path_2, image_name_2)
    print(dockerfile_path_2)
    build_dockerfile(dockerfile_path_3, image_name_3)
    print(dockerfile_path_3)
    build_dockerfile(dockerfile_path_4, image_name_4)
    print(dockerfile_path_4)
    build_dockerfile(dockerfile_path_5, image_name_5)
    print(dockerfile_path_5)
    build_dockerfile(dockerfile_path_6, image_name_6)
    print(dockerfile_path_6)
    build_dockerfile(dockerfile_path_7, image_name_7)
    print(dockerfile_path_7)

    deploy_kubernetes_manifest(deployment_manifest_path)


if __name__ == "__main__":
    main()