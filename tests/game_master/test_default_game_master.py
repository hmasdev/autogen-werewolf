from collections import Counter, namedtuple
from dataclasses import asdict
import os
import autogen
from flaky import flaky
from langchain_openai import ChatOpenAI
import pytest
from pytest_mock import MockerFixture
from werewolf.config import GameConfig
from werewolf.const import (
    EResult,
    ERole,
    DAYTIME_DISCUSSION_MANAGER_NAME,
    NIGHTTIME_DISCUSSION_MANAGER_NAME
)
from werewolf.game_master.default_game_master import DefaultGameMaster


@pytest.fixture
def game_config() -> GameConfig:
    return GameConfig(
        n_players=12,
        n_werewolves=3,
        n_fortune_teller=1,
        n_knight=1,
        include_human=False,
    )


def test_DefaultGameMaster_init(mocker: MockerFixture, game_config: GameConfig) -> None:  # noqa
    # init
    group_chat = autogen.GroupChat(agents=[], messages=[])
    group_chat_post_init_spy = mocker.spy(group_chat, '__post_init__')
    mock_setup = mocker.patch.object(DefaultGameMaster, 'setup', autospec=True)  # noqa
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=group_chat,
        llm_config=False,
    )
    # test
    mock_setup.assert_called_once_with(master, **game_config.__dict__)
    group_chat_post_init_spy.assert_called_once_with()


def test_DefaultGameMaster_setup(mocker: MockerFixture, game_config: GameConfig) -> None:  # noqa
    # init
    setup_spy = mocker.spy(DefaultGameMaster, 'setup')
    _generate_players_spy = mocker.spy(DefaultGameMaster, '_generate_players')  # noqa
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    # assert
    setup_spy.assert_called_once()
    _generate_players_spy.assert_called_once()

    assert master.day == 1
    assert master.speaker_selection_method == game_config.speaker_selection_method  # noqa
    assert master.n_turns_per_day == game_config.n_turns_per_day
    assert master.is_silent_game == game_config.silent

    assert master._werewolves_log == []
    assert master._daytime_log == []
    assert master._temporal_safe_players == []
    # NOTE: master._all_log is not []

    # TODO: split the test for _generate_players
    assert len(master.players) == game_config.n_players
    assert len(master.alive_players) == game_config.n_players
    assert len(master.alive_werewolves) == game_config.n_werewolves
    roles_count_dic = Counter([player.role for player in master.players.values()])  # noqa
    assert roles_count_dic[ERole.Werewolf] == game_config.n_werewolves
    assert roles_count_dic[ERole.FortuneTeller] == game_config.n_fortune_teller  # noqac
    assert roles_count_dic[ERole.Knight] == game_config.n_knight
    assert roles_count_dic[ERole.Villager] == (
        game_config.n_players
        - game_config.n_werewolves
        - game_config.n_fortune_teller
        - game_config.n_knight
    )

    assert master._game_rule  # TODO: check the content of the game rule

    assert master.groupchat.agents == list(master.players.values())

    # TODO: test whether master.announce is called
    # TODO: test whether master.initiate_chat is called in just1turn context


def test_DefaultGameMaster_next_day(mocker: MockerFixture, game_config: GameConfig) -> None:  # noqa
    # setup mock
    mocker.patch.object(DefaultGameMaster, 'setup', autospec=True)
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    master._day = 1
    # execute
    master.next_day()
    # assert
    assert master._day == 2


def test_DefaultGameMaster_add_temporal_safe_player(
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # setup mock
    mocker.patch.object(DefaultGameMaster, 'setup', autospec=True)
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    master._temporal_safe_players = []
    # execute and assert
    assert master._temporal_safe_players == []
    master.add_temporal_safe_player('dummy')
    assert master._temporal_safe_players == ['dummy']
    master.add_temporal_safe_player('dummy2')
    assert master._temporal_safe_players == ['dummy', 'dummy2']


def test_DefaultGameMaster_reset_temporal_safe_players(
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # setup mock
    mocker.patch.object(DefaultGameMaster, 'setup', autospec=True)
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    master._temporal_safe_players = ['dummy']
    # execute and assert
    assert master._temporal_safe_players == ['dummy']
    master.reset_temporal_safe_players()
    assert master._temporal_safe_players == []


def test_DefaultGameMaster__clean_name(
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # init
    input_name = ' Player0 '
    expected = 'Player0'
    llm_output = expected
    llm_mock = mocker.MagicMock(spec=ChatOpenAI)
    llm_mock.invoke.return_value = namedtuple('BaseMessage', ['content'])(llm_output)  # noqa
    create_chat_openai_model_mock = mocker.patch(
        'werewolf.game_master.default_game_master.create_chat_openai_model',
        return_value=llm_mock,
        autospec=True,
    )
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    # execute
    actual = master._clean_name(input_name)
    # assert
    assert actual == expected
    create_chat_openai_model_mock.assert_called_once()


@pytest.mark.parametrize(
    'max_retry',
    [1, 2, 3],
)
def test_DefaultGameMaster__clean_name_all_fail(
    max_retry: int,
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # init
    input_name = ''
    expected = 'None'
    llm_output = 'dummy'
    llm_mock = mocker.MagicMock(spec=ChatOpenAI)
    llm_mock.invoke.return_value = namedtuple('BaseMessage', ['content'])(llm_output)  # noqa
    _ = mocker.patch(
        'werewolf.game_master.default_game_master.create_chat_openai_model',
        return_value=llm_mock,
        autospec=True,
    )
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    # execute
    actual = master._clean_name(input_name, max_retry=max_retry)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    'n_fails',
    [1, 2],
)
def test_DefaultGameMaster__clean_name_n_fails(
    n_fails: int,
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # init
    input_name = ' Player0 '
    expected = 'Player0'
    llm_output_fail = 'dummy'
    llm_output = expected
    llm_mock = mocker.MagicMock(spec=ChatOpenAI)
    llm_mock.invoke.side_effect = [
        namedtuple('BaseMessage', ['content'])(llm_output_fail)
        for _ in range(n_fails)
    ] + [namedtuple('BaseMessage', ['content'])(llm_output)]
    _ = mocker.patch(
        'werewolf.game_master.default_game_master.create_chat_openai_model',
        return_value=llm_mock,
        autospec=True,
    )
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    # execute
    actual = master._clean_name(input_name)
    # assert
    assert actual == expected


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("OPENAI_API_KEY") is None,
    reason="OPENAI_API is not set.",
)
@pytest.mark.parametrize(
    'input_name,expected',
    [
        ('In my opinion, Player1 is a werewolf.', 'Player1'),  # noqa
        ('I do not have any idea to who should be excluded.', 'None'),  # noqa
        ('In my opinion, who should be excluded is Player2.', 'Player2'),  # noqa
    ],
)
@flaky(max_runs=5, min_passes=2)
def test_DefaultGameMaster__clean_name_for_simple_input_integration(
    input_name: str,
    expected: str,
    game_config: GameConfig,
) -> None:
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    # execute
    actual = master._clean_name(input_name)
    # assert
    assert actual == expected


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("OPENAI_API_KEY") is None,
    reason="OPENAI_API is not set.",
)
@pytest.mark.parametrize(
    'input_name,expected',
    [
        (
            '''
My name is 3. Based on the discussion so far, here is my reasoning step by step:
1. ** Player0 ** has initiated the conversation and encouraged others to share their thoughts. This indicates they're actively trying to collaborate and identify the Werewolf, which is a positive sign for the villagers.
2. ** Player1 ** has disclosed their role as the Fortune Teller, which could be honest or a strategy by a Werewolf to gain the villagers' trust. However, they have also pushed for open discussion, which is beneficial for us.
3. ** Player2 ** raised concerns about Player1's cautiousness and their role. This can indicate suspicion but could also be an attempt by a Werewolf to cast doubt on a known villager. Player2 is also calling for open communication and information sharing.
4. ** Player3 ** has yet to provide their thoughts in this discussion. Lack of engagement can sometimes be viewed as a sign of a hidden agenda, but I want to evaluate the entirety of their input.
Based on the current observations and discussions, Player1 may be too defensively protective of their role, which could be an indicator of attempting to build trust while potentially being strategic. However, their role as the Fortune Teller is critical for the villagers.
Considering all these aspects, **Player1 should be excluded ** as a precaution, but with the understanding that there’s a slight risk that they are indeed the Fortune Teller genuinely trying to help us.
In conclusion: **Player1 should be excluded.**
''',  # noqa
            'Player1',
        ),
        (
            '''
My name is 2. In considering the roles and the current discussion, here’s my reasoning step by step:
1. **Player0 (Villager)** - Player0 seems to be encouraging open discussion and aims to gather insights. While they could lead the villagers, they haven’t taken a strong stance against any specific player yet.
2. **Player1 (Fortune Teller)** - Player1 has openly revealed their role and appears to be protective over their findings. Their ability to check roles at night poses a significant threat to the Werewolves if they correctly identify me or my teammate.
3. **Player2 (me, Werewolf)** - I need to remain undercover and contribute to the discussion while deflecting suspicion away from myself and my teammate.
4. **Player3 (Knight)** - Player3 is also contributing positively to the discussion and has been questioning Player1's motivations, suggesting a cautious approach to their role.
Taking all this into account, the most strategic exclusion to benefit the Werewolves is to vote out Player1 (the Fortune Teller). If we can eliminate Player1, we reduce the risk of them revealing my identity as a Werewolf during the night.
Therefore, **Player1 should be excluded.**
''',  # noqa
            'Player1',
        ),
        (
            '''
My name is "1." After considering the discussions and the points raised by each player, I will assess the situation based on the following reasoning:
1. **Player0** has encouraged open discussion and emphasized collaboration, which aligns with the goal of villagers working together. Their approach appears constructive.
2. **Player1 (myself)** has shared insights, emphasized observations, and clarified the importance of transparency. As the Fortune Teller, my intent is to gather information for the team's benefit.
3. **Player2** has pointed out the potential for manipulation by those who steer conversations too strategically. They raised a concern regarding Player1’s cautious approach in a very analytical way, which could be viewed suspiciously.
4. **Player3** has also echoed concerns about the strategic behavior of players while promoting open discussion. They raised valid points; however, they haven't shown outright suspicion toward anyone specifically, which could indicate a defensive stance.
Given these points, the discussion has led me to conclude that:
**Player2 should be excluded.** While they contributed thoughtfully, they were quick to cast doubt on Player1 and presented a cautious view that may serve to deflect attention from their own role. This could be a strategic move if Player2 happens to be the werewolf, trying to undermine trust in the Fortune Teller. 
Hence, I strongly believe that excluding Player2 will be beneficial for the Villagers in our effort to differentiate between allies and potential threats.
''',  # noqa
            'Player2',
        ),
        (
            '''
Hello, I am 0.
After analyzing the discussions and statements made by each player:
1. **Player1**: They revealed they are the Fortune Teller. This transparency can be beneficial, but we have to be cautious as it could also be a strategy to gain trust while hiding any ulterior motives.
2. **Player2**: Their arguments about being cautious of those who steer conversation strategically and their focus on gathering information were strong. They seemed observant and participative.
3. **Player3**: Similar to Player2, Player3 engaged well and has made valid points about the discussion dynamics. They are not drawing too much attention to themselves, which could indicate a neutral position.
Based on the observations, Player1’s openness about their role may be a potential tactic. However, since Player1 is confirmed to be on our side (Fortune Teller), we should not exclude them.
Considering that Player1 is suspecting Player2's motivations, while Player2 is fairly active, I find it compelling to pay more attention to Player3 for their initial observations paired with their caution. Although they are participating, their points may subtly deflect from Player1 or Player2's scrutiny.
Therefore, I propose that we consider:
**Player3 should be excluded** as they might be using a more cautious approach to blend in while avoiding drawing suspicion directly. This can indicate a potential disguise from the werewolf. 
So, Player3 should be excluded.
''',  # noqa
            'Player3',
        ),
    ],
)
@flaky(max_runs=5, min_passes=2)
def test_DefaultGameMaster__clean_name_for_more_complicated_integration(
    input_name: str,
    expected: str,
    game_config: GameConfig,
) -> None:
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    # execute
    actual = master._clean_name(input_name)
    # assert
    assert actual == expected


@pytest.mark.parametrize(
    'expected',
    ['Player0', 'Player1', 'Player2'],
)
def test_DefaultGameMaster_ask_to_vote(
    expected: str,
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    master.last_message = mocker.MagicMock(return_value={'content': expected})
    master._clean_name = mocker.MagicMock(side_effect=lambda _: expected)  # type: ignore # noqa
    player = master.alive_players[0]
    # execute
    actual = master.ask_to_vote(player)
    # assert
    assert actual == expected


def test_DefaultGameMaster_ask_to_vote_without_last_message_content(
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # init
    expected: str = 'None'
    llm_output = 'dummy'
    llm_mock = mocker.MagicMock(spec=ChatOpenAI)
    llm_mock.invoke.return_value = namedtuple('BaseMessage', ['content'])(llm_output)  # noqa
    _ = mocker.patch(
        'werewolf.game_master.default_game_master.create_chat_openai_model',
        return_value=llm_mock,
        autospec=True,
    )
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    master.last_message = mocker.MagicMock(return_value={})
    _clean_name_spy = mocker.spy(master, '_clean_name')
    player = master.alive_players[0]
    # execute
    actual = master.ask_to_vote(player)
    # assert
    assert actual == expected
    assert _clean_name_spy.call_args_list == [mocker.call('')]


@pytest.mark.parametrize(
    'is_silent',
    [True, False],
)
def test_DefaultGameMaster_announce_to_a_player(
    is_silent: bool,
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=GameConfig(**(asdict(game_config) | {'silent': is_silent})),  # noqa
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    player = master.alive_players[0]
    master.send = mocker.MagicMock()
    # execute
    master.announce('hello', player)
    # assert
    master.send.assert_called_once_with('hello', player, silent=is_silent)


@pytest.mark.parametrize(
    'is_silent',
    [True, False],
)
def test_DefaultGameMaster_announce_to_players(
    is_silent: bool,
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=GameConfig(**(asdict(game_config) | {'silent': is_silent})),  # noqa
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    master.send = mocker.MagicMock()
    # execute
    master.announce('hello', master.alive_players)
    # assert
    assert [call[0][1] for call in master.send.call_args_list] == master.alive_players  # noqa


def test_DefaultGameMaster_daytime_discussion(
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    expected = {p.name: f'vote_{p.name}' for p in master.alive_players}
    master.ask_to_vote = mocker.MagicMock(side_effect=lambda player, *args, **kwargs: expected.get(player.name))  # type: ignore # noqa
    run_chat_spy = mocker.spy(master, 'run_chat')
    # execute
    actual = master.daytime_discussion()
    # assert
    assert actual == expected
    assert master.groupchat.agents == master.alive_players
    assert master.groupchat.admin_name == DAYTIME_DISCUSSION_MANAGER_NAME
    assert master.groupchat.max_round == master.n_turns_per_day * len(master.alive_players) + 1  # noqa
    assert master.groupchat.speaker_selection_method == master.speaker_selection_method   # noqa
    assert master.groupchat.allow_repeat_speaker is False
    run_chat_spy.assert_called_once()


@pytest.mark.parametrize(
    'n_werewolves',
    [2, 3],
)
def test_DefaultGameMaster_nighttime_action_with_2_or_more_werewolves(
    n_werewolves: int,
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=GameConfig(**(asdict(game_config) | {'n_werewolves': n_werewolves})),  # noqa
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    expected = {p.name: f'vote_{p.name}' for p in master.alive_players}
    for player in master.alive_players:
        player.act_in_night = mocker.MagicMock(return_value=f'vote_{player.name}')  # type: ignore # noqa
    run_chat_spy = mocker.spy(master, 'run_chat')
    assert len(master.alive_werewolves) == n_werewolves
    # execute
    actual = master.nighttime_action()
    # assert
    assert actual == expected
    assert master.groupchat.agents == master.alive_werewolves
    assert master.groupchat.admin_name == NIGHTTIME_DISCUSSION_MANAGER_NAME
    assert master.groupchat.max_round == 1+2*len(master.alive_werewolves)  # noqa
    assert master.groupchat.speaker_selection_method == master.speaker_selection_method   # noqa
    assert master.groupchat.allow_repeat_speaker is False
    run_chat_spy.assert_called_once()


def test_DefaultGameMaster_nighttime_action_with_1_werewolf(
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=GameConfig(**(asdict(game_config) | {'n_werewolves': 1})),  # noqa
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    expected = {p.name: f'vote_{p.name}' for p in master.alive_players}
    for player in master.alive_players:
        player.act_in_night = mocker.MagicMock(return_value=f'vote_{player.name}')  # type: ignore # noqa
    send_spy = mocker.spy(master, 'send')
    assert len(master.alive_werewolves) == 1
    # execute
    actual = master.nighttime_action()
    # assert
    assert actual == expected
    send_spy.assert_called_once()


def test_DefaultGameMaster_exclude_players_following_votes_with_target_safe(  # noqa
    game_config: GameConfig,
) -> None:
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    master._temporal_safe_players = [p.name for p in master.alive_players]  # noqa
    # execute
    actual = master.exclude_players_following_votes({p.name: p.name for p in master.alive_players})  # noqa
    # assert
    assert isinstance(actual, str)
    assert 'No one is excluded' in actual


def test_DefaultGameMaster_exclude_players_following_votes_with_invalid_targets(  # noqa
    game_config: GameConfig,
) -> None:
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    # execute
    actual = master.exclude_players_following_votes({p.name: 'invalid' for p in master.alive_players})  # noqa
    # assert
    assert isinstance(actual, str)
    assert 'No one is excluded' in actual


@pytest.mark.parametrize(
    'target',
    ['Player0', 'Player1'],
)
def test_DefaultGameMaster_exclude_players_following_votes_with_1candidate_success(  # noqa,
    target: str,
    game_config: GameConfig,
) -> None:
    # init
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    # execute
    actual = master.exclude_players_following_votes({p.name: target for p in master.alive_players})  # noqa
    # assert
    assert isinstance(actual, str)
    assert f'{target} is excluded from the game.' in actual


@pytest.mark.parametrize(
    'target0_choiced,target0,target1',
    [
        [False, 'Player0', 'Player1'],
        [True, 'Player1', 'Player0'],
    ]
)
def test_DefaultGameMaster_exclude_players_following_votes_with_2_candidates_success(  # noqa
    target0_choiced: bool,
    target0: str,
    target1: str,
    mocker: MockerFixture,
    game_config: GameConfig,
) -> None:
    # init
    random_mock = mocker.patch('random.choice', side_effect=lambda x: x[0] if target0_choiced else x[1])  # noqa
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    max_n_votes = game_config.n_players // 2
    votes = {p: v for p, v in zip(
        [p.name for p in master.alive_players],
        [target0]*max_n_votes + [target1]*max_n_votes,
    )}
    # execute
    actual = master.exclude_players_following_votes(votes)  # noqa
    # assert
    assert isinstance(actual, str)
    assert f'{target0 if target0_choiced else target1} is excluded from the game.' in actual  # noqa


@pytest.mark.parametrize(
    'n_players,n_werewolves,expected',
    [
        (12, 7, EResult.WerewolvesWin),
        (12, 6, EResult.WerewolvesWin),
        (12, 5, None),
        (12, 1, None),
        (12, 0, EResult.VillagersWin),
    ]
)
def test_DefaultGameMaster_check_victory_condition(
    n_players: int,
    n_werewolves: int,
    expected: EResult,
) -> None:
    # init
    game_config = GameConfig(
        n_players=n_players,
        n_werewolves=n_werewolves,
        n_fortune_teller=1,
        n_knight=1,
        include_human=False,
    )
    master = DefaultGameMaster(
        name='master',
        game_config=game_config,
        groupchat=autogen.GroupChat(agents=[], messages=[]),
        llm_config=False,
    )
    # assert
    assert master.check_victory_condition() == expected
