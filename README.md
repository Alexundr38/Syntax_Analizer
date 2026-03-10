# Syntax_Analizer

Синтаксический анализатор КС-грамматики:
```
<query> ::= <select_word> <columns> <from> <where> <group_by> <order> <limit>

<select_word> ::= ‘найти’ | ‘показать’ | ‘вывести’

 <columns> ::= <quantifier> | <name_columns>
<quantifier> ::= ‘всё’
<name_columns> ::= <column_name> <column_extension>
<column_name> ::= название столбца (существительное)
<column_extension> ::= <separator> <name_columns> | e
<separator> ::= ‘,’ | ‘;’

<from> ::= <from_word> <tables>
<from_word> ::= ‘из’
<tables> ::= <table_name> <table_extension>
<table_name> ::= название таблицы (существительное)
<table_extension> ::= <join_word> <tables> | e
<join_word> ::= ‘соединяя с’ | ‘вместе с’ | <and_connector>
<and_connector> ::= ‘и’ | <separator>

<where> ::= <where_word> <conditions> | e
<where_word> ::= ‘где’ | ‘в который’
<conditions> ::= <column_name> <comparison> <right_condition> <condition_extension>
<comparison> ::= ‘<’ | ‘>’ | ‘<=’ | ‘>=’ | ‘==’ | ‘<>’
<right_condition> ::= <number> | <column_name> | <word>
<number> ::= число
<word> ::= слово (существительное)
<condition_extension> ::= <connector> <conditions> | e
<connector> ::= ‘или’ | ‘также’ | <and_connector>

<group_by> ::= <group_word> <group_columns> | e
<group_word> ::= ‘сгруппировать по’ | ‘группировать по’
<group_columns> = <column_name> <group_extension>
<group_extension> ::= <and_connector> <group_by> | e

<order> ::= <order_word> <order_columns> | e 
<order_word> ::= ‘сортировать по’
<order_columns> ::= <column_name> <indicator> <order_extension>
<indicator> ::= <order_pointer> <desc_any> | e
<order_pointer> ::= ‘в порядок’
<desc_any> ::= ‘возрастание’ | ‘убывание’
<order_extension> ::= <and_connector> <order> | e

<limit> ::= <limit_word> <number>
<limit_word> ::= ‘ограничиваться’ | ‘первый’
```

Для запуска программы:
```
python3 -m venv venv
sourde ./venv/bin/activate
pip install -r requirements.txt
python3 -m src.main
```

Ввод своих запросов происходит в отдельную строку в файле data/queries.txt