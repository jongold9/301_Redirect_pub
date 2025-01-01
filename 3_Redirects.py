import re

def extract_path_from_url(url):
    match = re.search(r'https?://[^/]+(/.*)', url)
    if match:
        path = match.group(1)
        if not path.endswith('/'):
            path += '/'
        return path
    else:
        return '/'

def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

def format_redirect_301(from_path, to_url):
    return f"Redirect 301 {from_path} {to_url}\n"

def format_rewrite_rule(from_path, to_url):
    from_path = from_path.strip("/")
    return f"RewriteRule ^{from_path}/?$ {to_url} [R=301,L]\n"

def format_rewrite_rule_with_subpaths(from_path, to_url):
    return f"RewriteRule ^{from_path.strip('/')}(/.*)?$ {to_url} [R=301,L]\n"

def format_directory_redirect_with_subpaths(from_directory, to_directory):
    return f"RewriteRule ^{from_directory.strip('/')}(/.*)?$ /{to_directory.strip('/')}\\$1 [R=301,L]\n"

def format_https_rewrite_rule(from_path, to_url):
    from_path = from_path.strip("/")
    match = re.match(r'https?://[^/]+(/.*)?', to_url)
    if not match:
        raise ValueError(f"Некорректный URL: {to_url}")
    
    path = match.group(1) or "/"  # Извлекаем путь из to_url
    return f"RewriteRule ^{from_path}/?$ https://%{{HTTP_HOST}}{path} [R=301,L]\n"


if __name__ == "__main__":
    from_file_path = '1_From_urls.txt'
    to_file_path = '2_To_urls.txt'
    output_file_path = '4_Redirects.txt'

    from_urls = read_urls(from_file_path)
    to_urls = read_urls(to_file_path)

    if len(from_urls) != len(to_urls):
        print("Списки URL-адресов имеют разную длину")
    else:
        print("Выберите тип редиректа:")
        print("1 - Redirect 301")
        print("2 - RewriteRule")
        print("3 - RewriteRule с подпутями")
        print("4 - Перенаправление директории с сохранением пути подпапок")
        print("5 - HTTPS RewriteRule")
        redirect_type = input("Введите номер: ")

        with open(output_file_path, 'w') as output_file:
            for from_url, to_url in zip(from_urls, to_urls):
                from_path = extract_path_from_url(from_url)
                if redirect_type == '1':
                    redirect = format_redirect_301(from_path, to_url)
                elif redirect_type == '2':
                    redirect = format_rewrite_rule(from_path, to_url)
                elif redirect_type == '3':
                    redirect = format_rewrite_rule_with_subpaths(from_path, to_url)
                elif redirect_type == '4':
                    redirect = format_directory_redirect_with_subpaths(from_path, to_url)
                elif redirect_type == '5':
                    redirect = format_https_rewrite_rule(from_path, to_url)
                output_file.write(redirect)

        print(f"Результаты редиректов сохранены в файл: {output_file_path}")
