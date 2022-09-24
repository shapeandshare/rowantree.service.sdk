""" User Population Get Command Definition """
from typing import Optional

from starlette import status

from ...contracts.dto.request_status_codes import RequestStatusCodes
from ...contracts.dto.wrapped_request import WrappedRequest
from ...contracts.request_verb import RequestVerb
from ...contracts.responses.population_get import PopulationGetResponse
from ..abstract_command import AbstractCommand


class UserPopulationGetCommand(AbstractCommand):
    """
    User Population Get Command
    Gets the user population.

    Methods
    -------
    execute(self, user_guid: str) -> int
        Executes the command.
    """

    def execute(self, user_guid: Optional[str] = None) -> int:
        """
        Executes the command.

        Parameters
        ----------
        user_guid: str
            The target user guid.

        Returns
        -------
        user_population: int
            User population size.
        """

        target_guid: str = self.demand_user_guid(user_guid=user_guid)

        request: WrappedRequest = WrappedRequest(
            verb=RequestVerb.GET,
            url=f"https://api.{self.options.tld}/game/v1/user/{target_guid}/population",
            statuses=RequestStatusCodes(allow=[status.HTTP_200_OK], reauth=[status.HTTP_401_UNAUTHORIZED], retry=[]),
        )
        response: dict = self.wrapped_request(request=request)
        population_get_response: PopulationGetResponse = PopulationGetResponse.parse_obj(response)
        return population_get_response.population
