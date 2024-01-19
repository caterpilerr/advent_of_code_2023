import math
import re
from collections import defaultdict, deque, Counter

input_file = 'input.txt'
with open(input_file, 'r') as f:
    data = [line.strip() for line in f.readlines()]


class Module:
    def __init__(self, module_id, recivers):
        self.module_id = module_id
        self.recivers = recivers
        self.inputs = []

    def add_inputs(self, module_ids):
        self.inputs.extend(module_ids)

    def __str__(self):
        class_name = self.__class__.__name__
        module_id = self.module_id
        inputs = ', '.join(map(str, self.inputs))
        receivers = ', '.join(map(str, self.recivers))

        return (
            f'ID: {module_id}\n'
            f' Module: {class_name}\n'
            f' Input Module IDs: {inputs}\n'
            f' Output Module IDs: {receivers}\n'
        )


class FlipFlop(Module):
    def __init__(self, module_id, recivers):
        self.state = False
        Module.__init__(self, module_id, recivers)

    def __call__(self, signal, sender_id):
        signals = []
        if not signal:
            self.state = not self.state
            for reciver in self.recivers:
                signals.append((self.state, reciver))

        return signals


class Conjunction(Module):
    def __init__(self, module_id, recivers):
        self.state = defaultdict(bool)
        Module.__init__(self, module_id, recivers)

    def __call__(self, signal, sender_id):
        signals = []
        self.state[sender_id] = signal
        output = False if all(self.state[input]
                              for input in self.inputs) else True
        for reciver in self.recivers:
            signals.append((output, reciver))

        return signals


class Broadcaster(Module):
    def __call__(self, signal, sender_id):
        signals = []
        for reciver in self.recivers:
            signals.append((signal, reciver))

        return signals


class Button(Module):
    def __call__(self, signal, sender_id):
        signals = []
        for reciver in self.recivers:
            signals.append((False, reciver))

        return signals


MODULE_PATTERN = r'(?P<type>[%&]?)(?P<id>\w+)* -> (?P<recievers>\D+)'

module_types = {
    'button': Button,
    '%': FlipFlop,
    '&': Conjunction,
    'broadcaster': Broadcaster,
}


def parse_data(input):
    modules = {}
    module_inputs = defaultdict(list)
    for line in input + ['button -> broadcaster']:
        match = re.match(MODULE_PATTERN, line).groupdict()
        module_id = match['id']
        receiver_ids = match['recievers'].split(', ')

        module_type = module_types.get(match['type'], None)
        module_type = module_type or module_types[module_id]

        module = module_type(module_id, receiver_ids)
        modules[module_id] = module
        for receiver_id in receiver_ids:
            module_inputs[receiver_id].append(module_id)

    for module_id, module in modules.items():
        if module_id in module_inputs:
            module.add_inputs(module_inputs[module_id])

    return modules


def solve(steps=None, to_activate=None):
    modules = parse_data(data)
    button_pressed = 0
    signal_queue = deque()
    activator_high_data = defaultdict(list)
    activator_cycle_start = defaultdict(int)
    pulse_counter = Counter()
    while True:
        signal_queue.append(('button', True, ''))
        button_pressed += 1
        while signal_queue:
            module_id, signal, sender_id = signal_queue.popleft()
            module = modules.get(module_id)
            if not module:
                continue

            outputs = module(signal, sender_id)
            for output_signal, destination_id in outputs:
                pulse_counter[output_signal] += 1
                signal_queue.append((destination_id, output_signal, module_id))

            if not to_activate:
                continue

            if module_id == to_activate and signal and not activator_cycle_start[sender_id]:
                input_data = activator_high_data[sender_id]
                input_data.append(button_pressed)
                if len(input_data) > 2:
                    first_range = input_data[-1] - input_data[-2]
                    second_range = input_data[-2] - input_data[-3]
                    if first_range == second_range:
                        activator_cycle_start[sender_id] = input_data[-3]

                    if len(activator_cycle_start) == len(module.inputs) and all(activator_cycle_start.values()):
                        return math.lcm(*activator_cycle_start.values())

        if button_pressed == steps:
            return pulse_counter[False] * pulse_counter[True]


def part_one():
    return solve(steps=1000)


print(f'Part One: {part_one()}')


def part_two():
    return solve(to_activate='cn')


print(f'Part Two: {part_two()}')
