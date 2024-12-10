import os, shutil


PATH_STATIC = "./static"
PATH_PUBLIC = "./public"


def main():
    copy_files(PATH_STATIC, PATH_PUBLIC)


def copy_files(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    copy_recursive(source, destination)


def copy_recursive(source, destination):
    # Make destination if doesn't exist
    if not os.path.exists(destination):
        os.mkdir(destination)

    for file in os.listdir(source):
        from_path = os.path.join(source, file)
        dest_path = os.path.join(destination, file)
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_recursive(from_path, dest_path)


if __name__ == "__main__":
    main()
