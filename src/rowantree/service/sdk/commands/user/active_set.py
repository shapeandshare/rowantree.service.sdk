""" UserActiveSet Command Definition """

from starlette import status

from ...contracts.dto.request_status_codes import RequestStatusCodes
from ...contracts.dto.wrapped_request import WrappedRequest
from ...contracts.request_verb import RequestVerb
from ...contracts.user_active_status import UserActiveGetStatus
from ..abstract_command import AbstractCommand


class UserActiveSetCommand(AbstractCommand):
    """
    User Active Set Command
    Sets the user active state.

    Methods
    -------
    execute(self, user_guid: str, request: UserActiveGetStatus) -> UserActiveGetStatus
        Executes the command.
    """

    def execute(self, user_guid: str, request: UserActiveGetStatus) -> UserActiveGetStatus:
        """
        Executes the command.

        Parameters
        ----------
        user_guid
        request: UserActiveGetStatus
            The active state to set the user to.

        Returns
        -------
        user_active: UserActive
            The state of the user.
        """

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.POST,
            url=f"https://api.{self.options.tld}/game/v1/user/{user_guid}/active",
            data={"active": request.active},
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[status.HTTP_401_UNAUTHORIZED], retry=[]),
        )
        response: dict = self.wrapped_request(request=request)
        return UserActiveGetStatus.parse_obj(response)
