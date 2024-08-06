from aiogram.fsm.state import StatesGroup, State


class UserRegistration(StatesGroup):
    accepting_terms_of_use = State()
    choosing_role = State()


class SolverAuthentication(StatesGroup):
    sending_info = State()
    waiting_for_check = State()
    choosing_nickname = State()


class ClientAuthentication(StatesGroup):
    sending_OP = State()
    sending_course = State()
    choosing_nickname = State()


class ClientBaseStates(StatesGroup):
    main_menu = State()
    creating_order = State()
    changing_info = State()
    entering_chat = State()
    finishing_order = State()


class SolverBaseStates(StatesGroup):
    main_menu = State()
    accepting_order = State()


class ClientChangeInfo(StatesGroup):
    choosing_changes = State()
    changing_nickname = State()
    changing_course = State()
    changing_OP = State()


class SolverChangeInfo(StatesGroup):
    choosing_changes = State()
    changing_nickname = State()


class ClientCreateOrder(StatesGroup):
    choosing_subject = State()
    choosing_date = State()
    choosing_time = State()
    choosing_job_type = State()
    choosing_grade = State()
    choosing_duration = State()
    writing_comment = State()
    accepting_price = State()
    paying = State()
    payed = State()
    waiting_solver = State()


class UserChatStates(StatesGroup):
    choosing_order = State()
    in_chat = State()
    in_chat_admin = State()

class ClientOrders(StatesGroup):
    choosing_order = State()

class ClientFinishOrder(StatesGroup):
    choosing_order = State()
    confirmation = State()
    set_grade = State()
    set_recall_text = State()


class SolverAcceptOrder(StatesGroup):
    accepting_order = State()


class ClientDisputeStates(StatesGroup):
    choosing_order = State()
    writing_problem = State()

class SolverDisputeStates(StatesGroup):
    choosing_order = State()
    writing_problem = State()

class AdminBaseStates(StatesGroup):
    main_menu = State()
