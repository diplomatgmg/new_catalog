from apps.comparison.models import CPUComparison, GPUComparison


class CPUBase:
    @staticmethod
    def get_category_slug():
        return "cpu"

    @staticmethod
    def get_comparison_model():
        return CPUComparison


class GPUBase:
    @staticmethod
    def get_category_slug():
        return "gpu"

    @staticmethod
    def get_comparison_model():
        return GPUComparison
