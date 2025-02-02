grammar STQL;

prog: (((print_stmt | bind) SEMICOLON) | comment)*;

comment: '/*' .*? '*/' ;

print_stmt: PRINT expr;
bind: IDENT ASSIGN expr;

const: STRING | DECIMAL;

list_expr: LEFT_SQUARE_BRACKET (expr (COMMA expr)*)? RIGHT_SQUARE_BRACKET;

two_args_builtin: SET_START | SET_FINAL | ADD_START | ADD_FINAL;

one_args_builtin: GET_START | GET_FINAL | GET_REACHABLE | GET_VERTICES | GET_EDGES | GET_LABELS;

with_builtin: MAP | FILTER;

string_arg_builtin: LOAD | REGEX | CFG;

two_args_language_builtin: INTERSECT | CONCAT | UNION;

one_args_language_builtin: KLEENE_CLOSURE;

expr:
    const
  | lambda_expr
  | two_args_builtin LEFT_BRACKET expr COMMA expr RIGHT_BRACKET
  | one_args_builtin LEFT_BRACKET expr RIGHT_BRACKET
  | with_builtin expr WITH expr
  | string_arg_builtin STRING
  | two_args_language_builtin expr AND expr
  | one_args_language_builtin expr
  | list_expr
  | logic
  | LEFT_BRACKET expr RIGHT_BRACKET
  | IDENT;


logic_atom: IDENT IN expr;

logic:
    logic_atom
  | logic_atom AND logic
  | logic_atom OR logic
  | NOT logic
  | LEFT_BRACKET logic RIGHT_BRACKET;

args:
    IDENT
  | LEFT_SQUARE_BRACKET (args (COMMA args)*)? RIGHT_SQUARE_BRACKET;

lambda_expr:
    LAMBDA LEFT_BRACKET args RIGHT_BRACKET OF expr FO;

SEMICOLON: ';';
PRINT: 'print';
STRING: '"' .*? '"' ;
DECIMAL: [0-9]+;
ASSIGN: ':=';
KLEENE_CLOSURE : 'kleene';
UNION : 'union' ;
CONCAT : 'concat' ;
INTERSECT : 'intersect' ;
CFG : 'cfg' ;
REGEX : 'regex' ;
LOAD : 'load' ;
FILTER : 'filter' ;
MAP : 'map' ;
GET_LABELS : 'gel_labels' ;
GET_EDGES : 'get_edges' ;
GET_VERTICES : 'get_vertices' ;
GET_REACHABLE : 'get_reachable' ;
GET_FINAL : 'get_final' ;
GET_START : 'get_start' ;
ADD_FINAL : 'add_final' ;
ADD_START : 'add_start' ;
SET_FINAL : 'set_final' ;
SET_START : 'set_start' ;
LEFT_BRACKET : '(' ;
RIGHT_BRACKET : ')' ;
LEFT_SQUARE_BRACKET : '[' ;
RIGHT_SQUARE_BRACKET : ']' ;
COMMA : ',';
WITH : 'with';
AND : 'and';
OR : 'or';
NOT : 'not';
IN : 'in';
LAMBDA : 'lambda';
OF : 'of';
FO : 'fo';

IDENT: [_a-zA-Z0-9]+;
WS : [ \n\r\t\f]+ -> skip ;
