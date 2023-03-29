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

result = {}

for field in range_filter_fields:
    field_min = f"{field}__gte"
    field_max = f"{field}__lte"

    result[field_min] = 13
    result[field_max] = 25


print(result)
