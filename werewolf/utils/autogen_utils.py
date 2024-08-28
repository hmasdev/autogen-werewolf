from contextlib import contextmanager
import autogen


@contextmanager
def just1turn(agent: autogen.ConversableAgent):
    """Context manager to make the agent reply only once.

    Args:
        agent (autogen.ConversableAgent): ConversableAgent instance
    """

    def terminate(self, messages, sender, config) -> tuple[bool, None]:
        return True, None
    agent.register_reply([autogen.Agent, None], terminate, position=0)
    yield
    agent._reply_func_list = [d for d in agent._reply_func_list if d['reply_func'] is not terminate]  # noqa
