from aiogram.fsm.state import State, StatesGroup


class AdminBaseStates(StatesGroup):
    send_to_all = State()
    confirm = State()


class MainBaseState(StatesGroup):
    main_state = State()
