from grpc import Channel

from clients.grpc.client import GRPCClient
from clients.grpc.gateway.client import build_gateway_grpc_client

from contracts.services.gateway.cards.rpc_issue_virtual_card_pb2 import (
    IssueVirtualCardRequest,
    IssueVirtualCardResponse,
)
from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import (
    IssuePhysicalCardRequest,
    IssuePhysicalCardResponse,
)
from contracts.services.gateway.cards.cards_gateway_service_pb2_grpc import (
    CardsGatewayServiceStub,
)


class CardsGatewayGRPCClient(GRPCClient):
    """
    gRPC-клиент для взаимодействия с CardsGatewayService.
    Предоставляет высокоуровневые методы для выпуска виртуальных и физических карт.
    """

    def __init__(self, channel: Channel) -> None:
        """
        Инициализация клиента с указанным gRPC-каналом.

        :param channel: gRPC-канал для подключения к CardsGatewayService.
        """
        super().__init__(channel)
        self.stub = CardsGatewayServiceStub(channel)

    def issue_virtual_card_api(
            self,
            request: IssueVirtualCardRequest,
    ) -> IssueVirtualCardResponse:
        """
        Низкоуровневый вызов метода IssueVirtualCard через gRPC.

        :param request: gRPC-запрос для выпуска виртуальной карты.
        :return: Ответ сервиса с данными выпущенной виртуальной карты.
        """
        return self.stub.IssueVirtualCard(request)

    def issue_physical_card_api(
            self,
            request: IssuePhysicalCardRequest,
    ) -> IssuePhysicalCardResponse:
        """
        Низкоуровневый вызов метода IssuePhysicalCard через gRPC.

        :param request: gRPC-запрос для выпуска физической карты.
        :return: Ответ сервиса с данными выпущенной физической карты.
        """
        return self.stub.IssuePhysicalCard(request)

    def issue_virtual_card(
            self,
            user_id: str,
            account_id: str,
    ) -> IssueVirtualCardResponse:
        """
        Выпуск виртуальной карты для указанного пользователя и счёта.

        :param user_id: Идентификатор пользователя.
        :param account_id: Идентификатор счёта.
        :return: Ответ сервиса с информацией о выпущенной виртуальной карте.
        """
        request = IssueVirtualCardRequest(
            user_id=user_id,
            account_id=account_id,
        )
        return self.issue_virtual_card_api(request)

    def issue_physical_card(
            self,
            user_id: str,
            account_id: str,
    ) -> IssuePhysicalCardResponse:
        """
        Выпуск физической карты для указанного пользователя и счёта.

        :param user_id: Идентификатор пользователя.
        :param account_id: Идентификатор счёта.
        :return: Ответ сервиса с информацией о выпущенной физической карте.
        """
        request = IssuePhysicalCardRequest(
            user_id=user_id,
            account_id=account_id,
        )
        return self.issue_physical_card_api(request)


def build_cards_gateway_grpc_client() -> CardsGatewayGRPCClient:
    """
    Фабрика для создания экземпляра CardsGatewayGRPCClient.

    :return: Инициализированный клиент для CardsGatewayService.
    """
    return CardsGatewayGRPCClient(channel=build_gateway_grpc_client())


if __name__ == '__main__':
    """
    Для теста
    """
    client = build_cards_gateway_grpc_client()

    # В реальном сценарии сюда лучше подставлять реальные ID из Users/Accounts,
    # но для smoke‑теста можно использовать что-то фиксированное или из fake.
    user_id = "553e146c-ee7d-43e0-8e54-19fab082b174"
    account_id = "ff89b4e8-d41e-4ccc-b488-6050879d0d92"

    print(f"Using user_id={user_id}, account_id={account_id}")

    # Выпуск виртуальной карты
    virtual_card_response = client.issue_virtual_card(
        user_id=user_id,
        account_id=account_id,
    )
    print("Issue virtual card response:", virtual_card_response)

    # Выпуск физической карты
    physical_card_response = client.issue_physical_card(
        user_id=user_id,
        account_id=account_id,
    )
    print("Issue physical card response:", physical_card_response)
