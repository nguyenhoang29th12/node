import aiohttp
import asyncio
from aiohttp import ClientTimeout

# Danh sách các nguồn proxy bổ sung
PROXY_SOURCES = [
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://spys.me/proxy.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://www.proxy-listen.de/Proxy/Proxyliste.html",
    "https://www.my-proxy.com/free-proxy-list.html",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://spys.me/proxy.txt"
]

# Đường dẫn file lưu proxy
OUTPUT_FILE = "proxy.txt"

# URL kiểm tra proxy hoạt động
TEST_URLS = [
    "http://httpbin.org/ip",
    "http://ifconfig.me/ip"
]

# Yêu cầu người dùng nhập giá trị timeout
TIMEOUT = int(input("Nhập thời gian timeout (giây): "))  # Nhập giá trị timeout từ người dùng

async def fetch_proxies(source_url):
    """Lấy proxy từ nguồn"""
    try:
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=20)) as session:  # Tăng timeout lên 20 giây
            async with session.get(source_url) as response:
                if response.status == 200:
                    return await response.text()
    except Exception as e:
        print(f"Không thể lấy proxy từ {source_url}: {e}")
    return ""


async def check_proxy(proxy):
    """Kiểm tra proxy còn sống"""
    for test_url in TEST_URLS:
        proxies = f"http://{proxy}"
        try:
            async with aiohttp.ClientSession(timeout=ClientTimeout(total=TIMEOUT)) as session:
                async with session.get(test_url, proxy=proxies) as response:
                    if response.status == 200:
                        print(f"Proxy sống: {proxy}")
                        return proxy
        except Exception as e:
            print(f"Proxy không hoạt động {proxy}: {e}")
            continue  # Tiếp tục kiểm tra với URL tiếp theo nếu có lỗi
    return None


async def main():
    # Lấy proxy từ các nguồn
    print("Đang lấy proxy từ các nguồn...")
    all_proxies = []
    tasks = [fetch_proxies(source) for source in PROXY_SOURCES]
    results = await asyncio.gather(*tasks)
    for result in results:
        all_proxies.extend(result.splitlines())

    print(f"Lấy được tổng cộng {len(all_proxies)} proxy từ các nguồn.")

    # Kiểm tra proxy còn sống
    print("Đang kiểm tra proxy...")
    tasks = [check_proxy(proxy) for proxy in all_proxies]
    alive_proxies = await asyncio.gather(*tasks)
    alive_proxies = [proxy for proxy in alive_proxies if proxy]

    print(f"Có {len(alive_proxies)} proxy hoạt động.")

    # Lưu proxy hoạt động vào file
    with open(OUTPUT_FILE, "w") as file:
        for proxy in alive_proxies:
            file.write(proxy + "\n")
    print(f"Proxy đã được lưu vào file {OUTPUT_FILE}.")


if __name__ == "__main__":
    asyncio.run(main())
