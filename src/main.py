import os, shutil, sys
from pathlib import Path
from markdown_blocks import markdown_to_html_node
from inline_markdown import extract_title

PATH_STATIC = "./static"
PATH_DOCS = "./docs"
PATH_TEMPLATE = "template.html"


def main():
    basepath = "/" if len(sys.argv) != 2 else sys.argv[1]
    copy_files(PATH_STATIC, PATH_DOCS)
    generate_pages_recursive("./content/", PATH_TEMPLATE, "./docs/", basepath)


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


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open_file(from_path)
    template = open_file(template_path)
    markdown_str = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page_html = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", markdown_str)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    with open(dest_path, "a") as html:
        html.write(page_html)
    html.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for file in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, file)
        dest_path = Path(os.path.join(dest_dir_path, file)).with_suffix(".html")
        if os.path.isfile(from_path):
            generate_page(from_path, template_path, dest_path, basepath)
            print("Done!")
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def open_file(path):
    try:
        with open(path) as file:
            return file.read()
    except FileNotFoundError as e:
        print(e)
    finally:
        file.close()


if __name__ == "__main__":
    main()
