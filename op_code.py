import re

from arg_type import ArgType
from my_exceptions import OpCodeException, OtherSyntaxLexicalException


class OpCode:
    def __init__(self, op_code: str, params: list[ArgType]):
        self.__name = op_code
        self.__params = params

    @property
    def name(self) -> str:
        return self.__name

    @property
    def params(self) -> list[ArgType]:
        return self.__params

    def __str__(self) -> str:
        return self.__name.upper()

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.__name.upper() == other.upper()
        if isinstance(other, OpCode):
            return self.__name.upper() == other.__name.upper()

    def __hash__(self):
        return hash(self.__name.upper())


# a-zA-Z0-9
op_code_regex = r'^[a-zA-Z0-9]+$'


class InstructionSet:

    def __init__(self):
        self.__instruction_set = []
        self.__label_set_ops = []
        self.__label_jump_ops = []
        self.__jump_ops = []
        self.__header = None

    def register_opcode(self, op_code: str, params: list[ArgType], *,
                        label_set_op=False, label_jump_op=False, jump_op=False) -> None:
        """
        Register new instruction to instruction set
        :param op_code: instruction op_code
        :param params: list of instruction arguments
        :param label_set_op: is this instruction label decl operation
        :param label_jump_op: is this instruction label jump operation
        :param jump_op: is this instruction jump operation
        :return:
        """
        new_op_code = OpCode(op_code, params)
        self.__instruction_set.append(new_op_code)
        setattr(self, op_code.upper(), new_op_code)
        if label_set_op:
            self.__label_set_ops.append(new_op_code)
        if label_jump_op:
            self.__label_jump_ops.append(new_op_code)
        if jump_op or label_jump_op:
            self.__jump_ops.append(new_op_code)

    def register_header(self, header: str) -> None:
        """
        Register header to instruction set
        :param header: header name
        :return:
        """
        self.__header = header

    @property
    def header(self) -> str:
        """
        :return: Returns header name
        """
        return self.__header

    @property
    def label_ops(self) -> list[OpCode]:
        """
        :return: Returns list of label operations
        """
        return self.__label_set_ops

    @property
    def jump_ops(self) -> list[OpCode]:
        """
        :return: Returns list of jump operations
        """
        return self.__jump_ops

    @property
    def label_jump_ops(self) -> list[OpCode]:
        """
        :return: Returns list of label jump operations
        """
        return self.__label_jump_ops

    def __getitem__(self, item: str) -> OpCode:
        if item.upper() not in self.__instruction_set:
            if not re.fullmatch(op_code_regex, item):
                raise OtherSyntaxLexicalException("Got non opcode format input")
            raise OpCodeException("Unknown OpCode")
        return getattr(self, item.upper())

    def __contains__(self, item):
        return item.upper() in self.__instruction_set

    def __iter__(self):
        return iter(self.__instruction_set)
