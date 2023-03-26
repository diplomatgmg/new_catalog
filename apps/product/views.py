from apps.product.base_views import BaseProductListView
from apps.product.models import CPUModel, GPUModel


class CPUListView(BaseProductListView):
    model = CPUModel
    # Поля для фильтрации диапазона
    range_filter_fields = (
        "cores",
        "threads",
        "base_clock",
        "boost_clock",
        "tdp",
        "max_temperature",
        "l1_cache",
        "l2_cache",
        "l3_cache",
    )

    choice_filter_fields = (
        "brand",
        "family",
        "model",
        "year",
        "segment",
        "socket",
        "unlocked_multiplier",
        "architecture",
        "technology",
        "integrated_graphics",
        "memory_controller",
        "pcie",
    )

    list_display_fields = (
        ("brand", "Бренд", ""),
        ("family", "Семейство", ""),
        ("model", "Модель", ""),
        ("cores", "Количество ядер", "ядер"),
        ("threads", "Количество Потоков", "потока"),
        ("base_clock", "Базовая частота", "МГц"),
        ("year", "Год выхода", ""),
        ('segment', "Сегмент", ""),
        ("socket", "Сокет", ""),
        ("architecture", "Архитектура процессора", ""),
        ("technology", "Технология процессора", "нм"),
        ("tdp", "Тепловыделение", "Вт"),
        ("max_temperature", "Максимальная температура", "C°"),
        ("l1_cache", "Кэш L1, в КБ", "КБ"),
        ("l2_cache", "Кэш L2, в КБ", "КБ"),
        ("l3_cache", "Кэш L3, в КБ", "КБ"),
        ("integrated_graphics", "Встроенная графика", ""),
        ("memory_controller", "Поддерживаемая память", ""),
        ("pcie", "PCIe", ""),
    )

    brief_list = (
        ("cores", "Ядер"),
        ("year", "Год"),
    )


class GPUListView(BaseProductListView):
    model = GPUModel
    range_filter_fields = (
        "base_clock",
        "boost_clock",
    )

    choice_filter_fields = (
        "brand",
        "family",
        "model",
    )

    list_display_fields = (
        ("brand", "Бренд", ""),
        ("family", "Семейство", ""),
        ("model", "Семейство", ""),
        ("base_clock", "Базовая частота", "МГц"),
        ("boost_clock", "Базовая частота", "МГц"),
    )

    brief_list = (
        ("base_clock", "Базовая частота"),
        ("boost_clock", "Частота турбобуста"),
    )
