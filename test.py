import re

import requests
from bs4 import BeautifulSoup
from django.db import IntegrityError

from apps.product.models import Brand, Category, CPUModel

url = "https://www.chaynikam.info/cpu_table.html?td3=yearofprod&sortd=td3&scrl=258"

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

table = soup.find("table", class_="cpus")

rows = table.find_all("td", {"class": "cpus2"})

root_url = "https://www.chaynikam.info/"
hrefs = []
for row in rows[1:1500]:
    href = row.find("a")["href"]
    hrefs.append(root_url + href)


def split_processor_name(full_name):
    # Регулярное выражение для разбиения полного имени процессора
    pattern = r"^(AMD|Intel)\s+(.*?)\s+([A-Z0-9]+)$"

    # Извлекаем данные из полного имени процессора
    match = re.match(pattern, full_name)

    try:
        brand, family, model = match.group(1), match.group(2), match.group(3)
        brand = Brand.objects.get(name=brand)
        return brand, family, model
    except:
        return None


def parse_year(year):
    try:
        return int(year)
    except:
        print(href)
        print("Invalid year")


def parse_segment(segment):
    if "для настольных компьютеров" == segment.lower():
        return "DES"
    elif "для мобильных компьютеров" == segment.lower():
        return "MOB"
    elif "для серверов" == segment.lower():
        return "SER"

    elif "встраиваемый" == segment.lower():
        return False
    else:
        print(href)
        print("Invalid segment")
        raise ValueError


def parse_socket(socket):
    return socket.lower().replace("socket", "").strip().upper()


def parse_cores(cores):
    return int(cores.split()[0])


def parse_threads(threads):
    return int(threads.split()[0])


def parse_base_clock(base_clock):
    return int(base_clock.lower().replace("mhz", "").strip())


def parse_boost_clock(boost_clock):
    try:
        return int(boost_clock.lower().replace("mhz", "").strip())
    except ValueError:
        return None


def parse_unlocked_multiplier(unlocked_multiplier):
    if "нет" == unlocked_multiplier.lower().strip():
        return False
    if "да" == unlocked_multiplier.lower().strip():
        return True
    else:
        print(href)
        print("Invalid unlocked multiplier")
        raise ValueError


def parse_architecture(architecture):
    return architecture.lower().split("-")[0].title()


def parse_technology(process):
    return int(process.split()[0])


def parse_tdp(tdp):
    return int(float(tdp.split("-")[0].split()[0]))


def parse_max_temperature(max_temperature):
    match = re.match(r"\d+", max_temperature)
    if match:
        return int(match.group(0))
    else:
        print(href)
        print("Invalid max temperature")
        raise ValueError


def parse_cache(cache):
    try:
        return int(cache)
    except:
        try:
            cache = cache.lower().replace("x", "*")
            return int(eval(cache))
        except:
            print("ERROR:", full_name)


def parse_integrated_graphics(integrated_graphics):
    if integrated_graphics.lower() == "нет":
        return False
    elif (
        "mhz" in integrated_graphics.lower()
        or "mgz" in integrated_graphics.lower()
    ):
        return True
    else:
        print(href)
        print("Invalid integrated graphics")
        raise ValueError


def parse_memory_controller(memory_controller):
    memory_controller = memory_controller.upper().replace("-", " ")
    match = sorted(re.findall(r"(DDR\d|LPDDR\d)", memory_controller.upper()))
    if len(match) == 1:
        return match[0]
    elif len(match) in (2, 3, 4):
        return ", ".join(match)
    else:
        print(href)
        print("Invalid memory controller")
        raise ValueError


def parse_pcie(pcie):
    match = re.findall(r"\d\.\d", pcie)
    if len(match) == 1:
        return float(match[0])
    elif pcie.lower() == "нет":
        return None
    else:
        print(href)
        print("Invalid PCIe")
        raise ValueError


words = {
    "Год выхода": "year",
    "Сегмент": "segment",
    "Socket": "socket",
    "Количество ядер": "cores",
    "Количество потоков": "threads",
    "Базовая частота": "base_clock",
    "Turbo Boost": "boost_clock",
    "Turbo Core": "boost_clock",
    "Разблокированный множитель": "unlocked_multiplier",
    "Архитектура (ядро)": "architecture",
    "Техпроцесс": "technology",
    "TDP": "tdp",
    "Макс. температура": "max_temperature",
    "Кэш L1, КБ": "l1_cache",
    "Кэш L2, КБ": "l2_cache",
    "Кэш L3, КБ": "l3_cache",
    "Графический процессор": "integrated_graphics",
    "Контроллер оперативной памяти": "memory_controller",
    "Контроллер PCIe": "pcie",
}

category = Category.objects.get(slug="cpu")

for href in hrefs[:1500]:
    page = requests.get(href)
    soup = BeautifulSoup(page.content, "html.parser")

    full_name = soup.find("div", class_="verh").text.strip().replace("-", " ")

    try:
        brand, family, model = split_processor_name(full_name)
    except:
        print("ERROR:", full_name)

    table = soup.find("table")

    try:
        rows = table.find_all("tr")
    except AttributeError:
        continue

    # Создаем словарь для хранения информации о процессоре
    info = {
        "brand": brand,
        "category": category,
        "family": family,
        "model": model,
        "year": None,
        "segment": None,
        "socket": None,
        "num_cores": None,
        "threads": None,
        "base_clock": None,
        "boost_clock": None,
        "unlocked_multiplier": None,
        "architecture": None,
        "technology": None,
        "tdp": None,
        "max_temperature": None,
        "l1_cache": None,
        "l2_cache": None,
        "l3_cache": None,
        "integrated_graphics": None,
        "memory_controller": None,
        "pcie": None,
    }

    # Проходим по каждой строке таблицы
    for row in rows:
        if not row.find("td", colspan="2"):
            td1 = row.find("td", class_="tdc1")
            td2 = row.find("td", class_="tdc2")

            if td1 and td2:
                td1 = td1.text.strip()
                td2 = td2.text.strip()

                if td1 == "Год выхода":
                    year = parse_year(td2)
                    info["year"] = year
                elif td1 == "Сегмент":
                    segment = parse_segment(td2)
                    if not segment:
                        continue
                    info["segment"] = segment
                elif td1 == "Socket":
                    socket = parse_socket(td2)
                    info["socket"] = socket
                elif td1 == "Количество потоков":
                    threads = parse_threads(td2)
                    info["threads"] = threads
                elif td1 == "Количество ядер":
                    num_cores = parse_cores(td2)
                    info["num_cores"] = num_cores
                elif td1 == "Базовая частота":
                    base_clock = parse_base_clock(td2)
                    info["base_clock"] = base_clock
                elif td1 == "Turbo Boost" or td1 == "Turbo Core":
                    boost_clock = parse_boost_clock(td2)
                    info["boost_clock"] = boost_clock
                elif td1 == "Разблокированный множитель":
                    unlocked_multiplier = parse_unlocked_multiplier(td2)
                    info["unlocked_multiplier"] = unlocked_multiplier
                elif td1 == "Архитектура (ядро)":
                    architecture = parse_architecture(td2)
                    info["architecture"] = architecture
                elif td1 == "Техпроцесс":
                    technology = parse_technology(td2)
                    info["technology"] = technology
                elif td1 == "TDP":
                    tdp = parse_tdp(td2)
                    info["tdp"] = tdp
                elif td1 == "Макс. температура":
                    max_temperature = parse_max_temperature(td2)
                    info["max_temperature"] = max_temperature
                elif td1 == "Кэш L1, КБ":
                    l1_cache = parse_cache(td2)
                    info["l1_cache"] = l1_cache
                elif td1 == "Кэш L2, КБ":
                    l2_cache = parse_cache(td2)
                    info["l2_cache"] = l2_cache
                elif td1 == "Кэш L3, КБ":
                    l3_cache = parse_cache(td2)
                    info["l3_cache"] = l3_cache
                elif td1 == "Графический процессор":
                    integrated_graphics = parse_integrated_graphics(td2)
                    info["integrated_graphics"] = integrated_graphics
                elif td1 == "Контроллер оперативной памяти":
                    memory_controller = parse_memory_controller(td2)
                    info["memory_controller"] = memory_controller
                elif td1 == "Контроллер PCIe":
                    pcie = parse_pcie(td2)
                    info["pcie"] = pcie

    try:
        CPUModel.objects.create(**info)
        print("CREATED:", full_name)

    except IntegrityError:
        print("DOUBLE CREATE:", full_name)

    except:
        print("ERROR:", full_name)
