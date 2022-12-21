# Описание языка запросов

### Абстрактный синтаксис

```
prog = List<stmt>

stmt =
    Bind of string * expr
  | Print of expr

val =
    String  of string
  | Int     of int

expr =
    Var of string                // переменные
  | Const of val                 // константы
  | Set_start of expr * expr     // задать множество стартовых состояний
  | Set_final of expr * expr     // задать множество финальных состояний
  | Add_start of expr * expr     // добавить состояния в множество стартовых
  | Add_final of expr * expr     // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of string               // загрузка графа (по строковому пути к файлу)
  | Regex of string              // преобразование строкового выражения к регулярному выражению
  | CFG of string                // преобразование строкового выражения к грамматике
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | List of List<expr>           // множество элементов (например для Set_start, Set_final)
  | Logic of logic               // логическое выражение

logic =
    In  of string * expr          // проверка, лежит ли переменная (задаваемая как имя) в множестве значений expr
  | And of logic * logic          // логическое "и"
  | Or  of logic * logic          // логическое "или"
  | Not of logic                  // логическое "не"

args =
    Wildcard of string                      // аргумент любого вида
  | Edge     of args * string * args        // аргумент ребро, содержащее две вершины и метку
  | List     of List<args>                  // аргумент, являющийся списком элементов

lambda =
    Lambda of args * expr         // лямбда как функция с аргументами и выражением
```

### Конкретный синтаксис

```
PROG -> (((PRINT | BIND) ';') | COMMENT)*

COMMENT -> '/*' .* '*/'

PRINT -> 'print' EXPR
BIND  -> IDENT ':=' EXPR

IDENT   -> [_a-zA-Z0-9]+
STRING  -> '"' .* '"'
DECIMAL -> [0-9]+

CONST ->
    STRING
  | DECIMAL

EXPR  ->
    IDENT
  | CONST
  | LAMBDA
  | 'set_start' '(' EXPR ',' EXPR ')'
  | 'set_final' '(' EXPR ',' EXPR ')'
  | 'add_start' '(' EXPR ',' EXPR ')'
  | 'add_final' '(' EXPR ',' EXPR ')'
  | 'get_start' '(' EXPR ')'
  | 'get_final' '(' EXPR ')'
  | 'get_reachable' '(' EXPR ')'
  | 'get_vertices' '(' EXPR ')'
  | 'get_edges' '(' EXPR ')'
  | 'gel_labels' '(' EXPR ')'
  | 'map' EXPR 'with' EXPR
  | 'filter' EXPR 'with' EXPR
  | 'load' STRING
  | 'regex' STRING
  | 'cfg' STRING
  | 'intersect' EXPR 'and' EXPR
  | 'concat' EXPR 'and' EXPR
  | 'union' EXPR 'and' EXPR
  | 'kleene' 'closure' 'of' EXPR
  | '[' (EXPR (',' EXPR)*))? ']'
  | LOGIC
  | '(' EXPR ')'

LOGIC ->
    STRING 'in' EXPR
  | LOGIC 'and' LOGIC
  | LOGIC 'or' LOGIC
  | 'not' LOGIC

ARGS ->
    IDENT
  | '[' (ARGS (',' ARGS)*))? ']'

LAMBDA ->
    'lambda' '(' ARGS ')' 'of' EXPR 'fo'

```

### Примеры

Получить все вершины, достижимые из 0 вершины, и напечатать:

```
/* Загружаем граф и устанавливаем ему стартовой вершиной 0 */
graph           := set_start (load "skos", [0]);
/* Получаем пары всех достиимых вершин (пары это лист из листов по 2 элемента-вершины) */
reachable_pairs := get_reachable (graph);
/* Получаем из пар достижимых вершин вторую компоненту (так как первая это вершина из начального множества, то есть 0) */
reachable_list  := map reachable_pairs with lambda ([a, b]) of b fo;
print reachable_list;

```

Найти все вершины, достижимые из начального множества, по которым существует путь удовлетворяющий регулярному выражению:

```
/* Загружаем граф и устанавливаем ему стартовое множество */
graph                               := set_start (load "skos", [0, 1, 2]);
regular_expr                        := regex "subClassOf*";
/* Пересекаем граф и регекс, получаем новый конечный автомат */
graph_and_regular_expr_intersection := intersect graph and regular_expr;
/* Получем пары вершин достижимых в получившемся автомате - пересечении регекса и графа */
reachable_pairs_intersection        := get_reachable (graph_and_regular_expr_intersection);
/* Оставляем только те пары достижимых вершин в пересечении, которые понадобятся для ответа */
reachable_pairs_from_start_set      := filter reachable_pairs_intersection with
                                            lambda ([[graph_s, regex_s], [graph_f, regex_f]]) of
                                                graph_s in get_start (graph) and regex_s in get_start (regular_expr)
                                                and regex_f in get_final (regular_expr)
                                            fo;
/* Напечатаем результат */
print map reachable_pairs_from_start_set with lambda ([[graph_s, regex_s], [graph_f, regex_f]]) of graph_f fo
```
