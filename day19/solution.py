import re
import operator
import copy
from collections import defaultdict, deque
from math import prod

input_file = 'input.txt'
with open(input_file, 'r') as f:
    input = [line.strip() for line in f.readlines()]


class rule():
    def __init__(self, result, attribute=None, op=None, value=None):
        self.result = result
        self.attribute = attribute
        self.op = op
        self.value = int(value) if value else None

    def __call__(self, obj):
        return self.result if ops[self.op](obj.get(self.attribute, None), self.value) else None


WORKFLOW_PATTERN = r'^(?P<workflow>\w+)\S+[,{]{1}(?P<end_rule>\w+)}$'
RULE_PATTERN = r'((?P<attribute>\w+)(?P<op>[><])(?P<value>\d+):(?P<result>\w+),?)'


def parse_input(input):
    workflow_input = input[:input.index('')]
    objects_input = input[input.index('') + 1:]
    workflows = {}
    for line in workflow_input:
        workflow_match = re.match(WORKFLOW_PATTERN, line)
        workflow_name, last_rule_result = workflow_match.group(
            'workflow', 'end_rule')
        rules = [rule(**(rule_match.groupdict()))
                 for rule_match in re.finditer(RULE_PATTERN, line)]
        rules.append(rule(last_rule_result))
        workflows[workflow_name] = rules

    objects = [dict(item.split('=')
                    for item in obj.strip('{}').split(',')) for obj in objects_input]
    objects = [{k: int(v) for k, v in obj.items()}
               for obj in objects]

    return workflows, objects


def always_true(a, b):
    return True


ops = defaultdict(lambda: always_true)
ops['>'] = operator.gt
ops['<'] = operator.lt


def run_pipeline(object, workflows):
    current_workflow = workflows['in']
    while True:
        for rule in current_workflow:
            result = rule(object)
            if result:
                if result == 'R':
                    return 0
                elif result == 'A':
                    return sum(object.values())
                else:
                    current_workflow = workflows[result]
                    break


def part_one():
    workflows, objects = parse_input(input)
    total_rating = 0
    for obj in objects:
        total_rating += run_pipeline(obj, workflows)

    return total_rating


print(f'Part One: {part_one()}')


def get_valid_ranges(workflows):
    queue = deque()
    full_range_obj = {k: [1, 4000] for k in ['x', 'm', 'a', 's']}
    queue.append((full_range_obj, 'in', 0))
    acceptable = []
    while queue:
        obj, workflow, rule_index = queue.popleft()
        if workflow == 'A':
            acceptable.append(obj)
            continue
        elif workflow == 'R':
            continue

        current_workflow = workflows[workflow]
        rule = current_workflow[rule_index]
        # if rule is a range rule
        if rule.op == '>':
            # if min range value is greater than rule value, add to queue applied rule result
            if obj[rule.attribute][0] > rule.value:
                queue.append((obj, rule.result, 0))
            # else if max range value is less or equal than rule value, add to queue next rule in workflow
            elif obj[rule.attribute][1] <= rule.value:
                queue.append((obj, workflow, rule_index + 1))
            # else range is between the rule value, split the range and add to queue
            else:
                false_obj = copy.deepcopy(obj)
                false_obj[rule.attribute][1] = rule.value
                queue.append((false_obj, workflow, rule_index + 1))
                obj[rule.attribute][0] = rule.value + 1
                queue.append((obj, rule.result, 0))
        elif rule.op == '<':
            # if max range value is less than rule value, add to queue applied rule result
            if obj[rule.attribute][1] < rule.value:
                queue.append((obj, rule.result, 0))
            # else if min range value is greater or equal than rule value, add to queue next rule in workflow
            elif obj[rule.attribute][0] >= rule.value:
                queue.append((obj, workflow, rule_index + 1))
            # else range is between the rule value, split the range and add to queue
            else:
                false_obj = copy.deepcopy(obj)
                false_obj[rule.attribute][0] = rule.value
                queue.append((false_obj, workflow, rule_index + 1))
                obj[rule.attribute][1] = rule.value - 1
                queue.append((obj, rule.result, 0))
        # else rule is a always true rule, apply it
        else:
            queue.append((obj, rule.result, 0))

    return acceptable


def part_two():
    workflows, _ = parse_input(input)
    acceptable_ranges = get_valid_ranges(workflows)

    result = 0
    for obj in acceptable_ranges:
        result += prod(range[1] - range[0] + 1 for range in obj.values())

    return result


print(f'Part Two: {part_two()}')
