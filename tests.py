import responses
import chronostat


@responses.activate
def test_context_manager():
    responses.add(responses.POST, chronostat.StatHat.STATHAT_URL + '/ez',
                  status=200)

