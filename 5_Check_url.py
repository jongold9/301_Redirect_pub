import aiohttp
import asyncio
import aiofiles

async def get_final_redirect(url, session):
    try:
        async with session.get(url, allow_redirects=False, timeout=10) as response:
            if response.status in (301, 302):
                redirect_url = response.headers['Location']
                return await get_final_redirect(redirect_url, session)
            else:
                return url  # Return the final URL without redirection
    except Exception as e:
        print(f"Error with {url}: {e}")
        return url  # Return the original URL in case of an error

async def process_batch(urls, output_file, session):
    tasks = [get_final_redirect(url, session) for url in urls]
    final_urls = await asyncio.gather(*tasks)
    for final_url in final_urls:
        await output_file.write(final_url + "\n")  # Write the final URLs

async def process_urls():
    with open("1_From_urls.txt", "r") as urls_file:
        urls = urls_file.read().splitlines()

    batches = [urls[i:i + 30] for i in range(0, len(urls), 30)]

    async with aiofiles.open("6_Check_url.txt", "w") as output_file, aiohttp.ClientSession() as session:
        for batch in batches:
            await process_batch(batch, output_file, session)
    
    print("Check completed. 6_Check_url.txt updated.")

def read_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def compare_urls(to_url, check_url):
    if to_url == check_url:
        return "Matches"
    else:
        to_protocol, to_rest = to_url.split("://", 1)
        check_protocol, check_rest = check_url.split("://", 1)
        if to_rest == check_rest and (to_protocol == "http" or to_protocol == "https"):
            return f"Matches - http -  {to_url},  {check_url}"
        else:
            return f"Does not match {to_url},  {check_url}"

def compare_and_write_results():
    to_urls = read_file("2_To_urls.txt")
    check_urls = read_file("6_Check_url.txt")

    results = []
    for idx, (to_url, check_url) in enumerate(zip(to_urls, check_urls), start=1):
        result = compare_urls(to_url, check_url)
        results.append(f"{result} - Line {idx}")

    with open("7_Results.txt", "w") as file:
        file.write("\n".join(results))

    print("Comparison completed. 7_Results.txt updated.")

if __name__ == "__main__":
    asyncio.run(process_urls())  # Run the URL processing and wait for its completion
    compare_and_write_results()  # Perform the comparison after the asynchronous part
