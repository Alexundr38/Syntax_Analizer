from typing import List, Optional

from Syntax_Analizer.src.tokenizer import Token, TokenEnum

def raiser(text1: Optional[str] = None, text2: Optional[str] = None):
    if text2 is None:
        raise Exception(text1)
    else:
        raise Exception(f'Ожидалось: {text1}, полученно: {text2}')


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0


    def get_current(self) -> Optional[Token]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None


    def check_current(self):
        current = self.get_current()
        if current is None:
            return False
        return True


    def match_type(self, expected_types: List[TokenEnum]):
        token = self.get_current()
        if token is None:
            return None
        if token.token_type in expected_types:
            self.pos += 1
            return token
        return None


    def parse_query(self):
        node = {'type': 'query'}
        select_word = self.parse_select_word()
        columns = self.parse_columns()
        from_val = self.parse_from()
        where, group_by, order, limit = None, None, None, None
        if self.check_current():
            where = self.parse_where()
        if self.check_current():
            group_by = self.parse_group_by()
        if self.check_current():
            order = self.parse_order()
        if self.check_current():
            limit = self.parse_limit()

        node['select_word'] = select_word
        node['columns'] = columns
        node['from'] = from_val
        if where:
            node['where'] = where
        if group_by:
            node['group_by'] = group_by
        if order:
            node['order'] = order
        if limit:
            node['limit'] = limit

        if self.get_current() is not None:
            raiser('Лишние токены в конце')
        return node


    def parse_select_word(self):
        token = self.match_type([TokenEnum.SELECT_WORD])
        if token:
            return {'type': 'select_word', 'value': token.text}
        raiser(TokenEnum.SELECT_WORD.value, self.get_current().text if self.get_current() else 'Конец строки')


    def parse_columns(self):
        token = self.match_type([TokenEnum.QUANTIFIER])
        if token:
            return {'type': 'quantifier', 'value': token.text}
        columns = self.parse_name_columns()
        return {'type': 'columns', 'value': columns}


    def parse_name_columns(self):
        column_name = self.parse_column_name()
        column_extension = self.parse_column_extension()
        if column_extension:
            return {'type': 'name_columns', 'column_name': column_name, 'column_extension': column_extension}
        return {'type': 'name_columns', 'column_name': column_name}


    def parse_column_name(self):
        token = self.match_type([TokenEnum.UNKNOWN])
        if token:
            token.token_type = TokenEnum.COLUMN_NAME
            return {'type': 'column_name', 'value': token.text}
        raiser(TokenEnum.COLUMN_NAME.value, self.get_current().text if self.get_current() else 'Конец строки')


    def parse_column_extension(self):
        separator = self.parse_separator()
        if separator:
            name_columns = self.parse_name_columns()
            return {'type': 'column_extension', 'separator': separator, 'name_columns': name_columns}
        return None


    def parse_separator(self):
        token = self.match_type([TokenEnum.SEPARATOR])
        if token:
            return {'type': 'separator', 'value': token.text}
        return None


    def parse_from(self):
        from_word = self.parse_from_word()
        tables = self.parse_tables()
        return {'type': 'from', 'from_word': from_word, 'tables': tables}


    def parse_from_word(self):
        token = self.match_type([TokenEnum.FROM_WORD])
        if token:
            return {'type': 'from_word', 'value': token.text}
        raiser(TokenEnum.FROM_WORD.value, self.get_current().text if self.get_current() else 'Конец строки')


    def parse_tables(self):
        table_name = self.parse_table_name()
        table_extension = self.parse_table_extension()
        if table_extension:
            return {'type': 'tables', 'table_name': table_name, 'table_extension': table_extension}
        return {'type': 'tables', 'table_name': table_name}


    def parse_table_name(self):
        token = self.match_type([TokenEnum.UNKNOWN])
        if token:
            token.token_type = TokenEnum.TABLE_NAME
            return {'type': 'table_name', 'value': token.text}
        raiser(TokenEnum.TABLE_NAME.value, self.get_current().text if self.get_current() else 'Конец строки')


    def parse_table_extension(self):
        join_word = self.parse_join_word()
        if join_word is None:
            return None

        tables = self.parse_tables()
        return {'type': 'table_extension', 'join_word': join_word, 'tables': tables}


    def parse_join_word(self):
        token = self.match_type([TokenEnum.JOIN_WORD])
        if token:
            return {'type': 'join_word', 'value': token.text}

        token = self.parse_and_connector()
        if token:
            return {'type': 'join_word', 'and_connector': token}
        return None


    def parse_and_connector(self):
        token = self.match_type([TokenEnum.AND_CONNECTOR, TokenEnum.SEPARATOR])
        if token:
            token.token_type = TokenEnum.AND_CONNECTOR
            return {'type': 'and_connector', 'value': token.text}
        return None


    def parse_where(self):
        where_word = self.parse_where_word()
        if where_word is None:
            return None
        conditions = self.parse_conditions()
        return {'type': 'where', 'where_word': where_word, 'conditions': conditions}


    def parse_where_word(self):
        token = self.match_type([TokenEnum.WHERE_WORD])
        if token:
            return {'type': 'where_word', 'value': token.text}
        return None


    def parse_conditions(self):
        column_name = self.parse_column_name()
        comparison = self.parse_comparison()
        right_condition = self.parse_right_condition()
        condition_extension = self.parse_condition_extension()
        if condition_extension:
            return {'type': 'conditions', 'column_name': column_name, 'comparison': comparison, 'right_condition': right_condition, 'condition_extension': condition_extension}
        return {'type': 'conditions', 'column_name': column_name, 'comparison': comparison, 'right_condition': right_condition}


    def parse_comparison(self):
        token = self.match_type([TokenEnum.COMPARISON])
        if token:
            return {'type': 'comparison', 'value': token.text}
        raiser(TokenEnum.COMPARISON.value, self.get_current().text if self.get_current() else 'Конец строки')


    def parse_right_condition(self):
        number = self.parse_number()
        if number:
            return {'type': 'right_condition', 'value': number}
        column_name = self.parse_column_name()
        if column_name:
            return {'type': 'right_condition', 'value': column_name}
        word = self.parse_word()
        if word:
            return {'type': 'right_condition', 'value': word}
        raiser(TokenEnum.RIGHT_CONDITION.value, self.get_current().text if self.get_current() else 'Конец строки')


    def parse_number(self):
        token = self.match_type([TokenEnum.NUMBER])
        if token:
            return {'type': 'number', 'value': token.text}
        return None


    def parse_word(self):
        token = self.match_type([TokenEnum.UNKNOWN])
        if token:
            token.token_type = TokenEnum.WORD
            return {'type': 'word', 'value': token.text}
        return None


    def parse_condition_extension(self):
        connector = self.parse_connector()
        if connector is None:
            return None
        conditions = self.parse_conditions()
        return {'type': 'condition_extension', 'connector': connector, 'conditions': conditions}


    def parse_connector(self):
        token = self.match_type([TokenEnum.CONNECTOR, TokenEnum.AND_CONNECTOR, TokenEnum.SEPARATOR])
        if token:
            token.token_type = TokenEnum.CONNECTOR
            return {'type': 'connector', 'value': token.text}
        return None


    def parse_group_by(self):
        group_word = self.parse_group_word()
        if group_word is None:
            return None
        group_columns = self.parse_group_columns()
        return {'type': 'group_by', 'group_word': group_word, 'group_columns': group_columns}


    def parse_group_word(self):
        token = self.match_type([TokenEnum.GROUP_WORD])
        if token:
            return {'type': 'group_word', 'value': token.text}
        return None


    def parse_group_columns(self):
        column_name = self.parse_column_name()
        group_extension = self.parse_group_extension()
        if group_extension:
            return {'type': 'group_extension', 'column_name': column_name, 'group_extension': group_extension}
        return {'type': 'group_extension', 'column_name': column_name}


    def parse_group_extension(self):
        and_connector = self.parse_and_connector()
        if and_connector is None:
            return None
        group_columns = self.parse_group_columns()
        return {'type': 'group_extension', 'and_connector': and_connector, 'group_columns': group_columns}


    def parse_order(self):
        order_word = self.parse_order_word()
        if order_word is None:
            return None
        order_columns = self.parse_order_columns()
        return {'type': 'order_word', 'order_word': order_word, 'order_columns': order_columns}


    def parse_order_word(self):
        token = self.match_type([TokenEnum.ORDER_WORD])
        if token:
            return {'type': 'order_word', 'value': token.text}
        return None


    def parse_order_columns(self):
        column_name = self.parse_column_name()
        indicator = self.parse_indicator()
        order_extension = self.parse_order_extension()
        if order_extension:
            if indicator:
                return {'type': 'order_columns', 'column_name': column_name, 'indicator': indicator, 'order_extension': order_extension}
            return {'type': 'order_columns', 'column_name': column_name, 'order_extension': order_extension}
        if indicator:
            return {'type': 'order_columns', 'column_name': column_name, 'indicator': indicator}
        return {'type': 'order_columns', 'column_name': column_name}


    def parse_indicator(self):
        order_pointer = self.parse_order_pointer()
        if order_pointer is None:
            return None
        desc_any = self.parse_desc_any()
        return {'type': 'indicator', 'order_pointer': order_pointer, 'desc_any': desc_any}


    def parse_order_pointer(self):
        token = self.match_type([TokenEnum.ORDER_POINTER])
        if token:
            return {'type': 'order_pointer', 'value': token.text}
        return None


    def parse_desc_any(self):
        token = self.match_type([TokenEnum.DESC_ANY])
        if token:
            return {'type': 'desc_any', 'value': token.text}
        raiser(TokenEnum.DESC_ANY.value, self.get_current().text if self.get_current() else 'Конец строки')


    def parse_order_extension(self):
        and_connector = self.parse_and_connector()
        if and_connector is None:
            return None
        order_columns = self.parse_order_columns()
        return {'type': 'order_extension', 'and_connector': and_connector, 'order_columns': order_columns}


    def parse_limit(self):
        limit_word = self.parse_limit_word()
        if limit_word is None:
            return None
        number = self.parse_number()
        return {'type': 'limit', 'limit_word': limit_word, 'number': number}


    def parse_limit_word(self):
        token = self.match_type([TokenEnum.LIMIT_WORD])
        if token:
            return {'type': 'limit_word', 'value': token.text}
        return None


