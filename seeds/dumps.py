import os

from seeds.schema.result import SeedsResult
from tools.logger import get_logger

# Инициализируем логгер с именем SEEDS_SCENARIO
logger = get_logger("SEEDS_DUMPS")


def save_seeds_result(result: SeedsResult, scenario: str):
    """
    Сохраняет результат сидинга (SeedsResult) в JSON-файл.

    :param result: Результат сидинга, сгенерированный билдером.
    :param scenario: Название сценария нагрузки, для которого создаются данные.
                     Используется для генерации имени файла (например, "credit_card_test").
    """
    # Убедимся, что папка dumps существует
    if not os.path.exists("dumps"):
        os.mkdir("dumps")

    path_str = f"./dumps/{scenario}_seeds.json"
    # Сохраняем результат сидинга в файл с именем {scenario}_seeds.json
    with open(path_str, 'w+', encoding="utf-8") as file:
        file.write(result.model_dump_json())

    logger.debug(f"Seeding result saved to file: {path_str}")


def load_seeds_result(scenario: str) -> SeedsResult:
    """
    Загружает результат сидинга из JSON-файла.

    :param scenario: Название сценария нагрузки, данные которого нужно загрузить.
    :return: Объект SeedsResult, восстановленный из файла.
    """
    path_str = f"./dumps/{scenario}_seeds.json"
    # Открываем файл и валидируем его как объект SeedsResult
    with open(path_str, 'r', encoding="utf-8") as file:
        logger.debug(f"Seeding result loaded from file: {path_str}")
        return SeedsResult.model_validate_json(file.read())
