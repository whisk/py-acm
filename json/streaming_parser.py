import sys

P_START = 0
P_END = 1
P_ARR = 10
P_ARR_NEXT = 11
P_HASH = 20

T_START = 0
T_STR = 1
T_NUM = 2


def parse_json(fh):
    state = P_START
    stack = []
    state_stack = []
    while True:
        for token, err in _next_token(fh):
            if token is None:
                if _is_finished(state):
                    return stack.pop()
                else:
                    raise Exception('invalid json: ' + err)
            state, err = _process_token(token, state, stack, state_stack)
            if err is not None:
                raise Exception('invalid syntax: ' + err)


def _next_token(fh):
    state = T_START
    val = None
    want_next = True
    escaped = False
    while True:
        if want_next:
            c = fh.read(1)
        want_next = True
        if state == T_START:
            if c in ('[', ']', '{', '}', ','):
                yield (('syn', c), None)
            elif c == "'":
                state = T_STR
                val = ''
            elif c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                state = T_NUM
                val = c
            elif c == '':
                yield (None, 'eof')
                break
            else:
                yield (None, 'unknown symbol')
                break
        elif state == T_STR:
            if c == "'" and not escaped:
                yield (('str', val), None)
                state = T_START
            elif c == '\\':
                escaped = True
                continue
            elif c == '':
                yield (None, 'unexpected end')
                break
            else:
                val += c
                escaped = False
        elif state == T_NUM:
            if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'):
                val += c
            elif c == '':
                yield (None, 'unexpected end')
                break
            else:
                yield (('num', float(val)), None)
                state = T_START
                want_next = False
        else:
            yield (None, 'tokenizer bug')
            break


def _is_finished(state):
    return state == P_START or state == P_END


def _process_token(token, state, stack, state_stack):
    print(token, state, stack, state_stack)
    t, token_val = token
    if state == P_START:
        if t == 'syn':
            if token_val == '[':
                stack.append(list())
                return (P_ARR, None)
            elif token_val == '{':
                stack.append(dict())
                return (P_HASH, None)
            else:
                return (None, 'expecting [ or {')
        else:
            return (None, 'expecting [ or }')
    elif state == P_ARR:
        if t == 'str' or t == 'num':
            stack[-1].append(token_val)
            return (P_ARR_NEXT, None)
        elif t == 'syn' and (token_val == ']'):
            if len(stack) == 0:
                return (None, 'parser bug')
            if len(stack) == 1:
                return (P_END, None)
            else:
                tmp = stack.pop()
                stack[-1].append(tmp)
                return (state_stack.pop(), None)
        elif t == 'syn' and (token_val == '[' or token_val == '{'):
            state_stack += [P_ARR_NEXT]
            new_state, err = _process_token(token, P_START, stack, state_stack)
            if err:
                return (None, err)
            else:
                return (new_state, None)
        else:
            return (None, 'expecting a value')
    elif state == P_ARR_NEXT:
        if t == 'syn':
            if token_val == ',':
                return (P_ARR, None)
            elif token_val == ']':
                if len(stack) == 0:
                    return (None, 'parser bug')
                if len(stack) == 1:
                    return (P_END, None)
                else:
                    tmp = stack.pop()
                    stack[-1].append(tmp)
                    return (state_stack.pop(), None)
            else:
                return (None, 'expecting comma or closing bracket')
    elif state == P_END:
        return (None, 'unexpected token')
    else:
        return (None, 'parser bug: unexpected state')


if __name__ == '__main__':
    data = parse_json(sys.stdin)
    print(data)
