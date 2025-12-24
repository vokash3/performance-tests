from grpc import Channel, insecure_channel, intercept_channel
from locust.env import Environment

from clients.grpc.interceptors.locust_interceptor import LocustInterceptor


def build_gateway_grpc_client() -> Channel:
    """
    Фабричная функция (билдер) для создания gRPC-канала к сервису grpc-gateway.

    :return: gRPC-канал (Channel), настроенный на адрес localhost:9003.
    """
    # Создаём небезопасное (без TLS) соединение с gRPC-сервером по адресу localhost:9003
    return insecure_channel("155.212.171.137:9003")


def build_gateway_locust_grpc_client(environment: Environment) -> Channel:
    """
    Фабричная функция для создания gRPC-канала, адаптированного для Locust.
    В канал автоматически встраивается интерцептор LocustInterceptor,
    который регистрирует вызовы в системе метрик Locust.

    Принимает на вход Environment из Locust, чтобы отправлять метрики.
    Создаёт тот же insecure_channel, но далее оборачивает его с помощью intercept_channel(...), встраивая LocustInterceptor.
    В результате все вызовы, проходящие через этот канал, будут автоматически логироваться в метрики Locust,
    включая время ответа, ошибки и объём данных.

    :param environment: Среда выполнения Locust (необходима для отправки событий).
    :return: gRPC-канал с интерцептором, пригодный для нагрузочного тестирования.
    """
    # Создаём экземпляр интерцептора, передаём в него окружение Locust
    locust_interceptor = LocustInterceptor(environment=environment)

    # Создаём обычный канал
    channel = insecure_channel("155.212.171.137:9003")

    # Оборачиваем канал интерцептором, чтобы все запросы проходили через него
    return intercept_channel(channel, locust_interceptor)
