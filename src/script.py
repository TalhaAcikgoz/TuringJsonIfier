import PySimpleGUI as sg
import json
import sys

def create_col(alphabet, transition_names, actions):
    read = [
        [sg.Text('Okuma')],
        [sg.Combo(alphabet, key=f'read')]
    ]
    to_state = [
        [sg.Text('state')],
        [sg.Combo(transition_names, key=f'state')],
    ]
    write = [
        [sg.Text('write')],
        [sg.Combo(alphabet, key=f'write')],
    ]
    action = [
        [sg.Text('action')],
        [sg.Combo(actions, key=f'action')],
    ]

    col = [
        [sg.Column(read), sg.Column(to_state), sg.Column(write), sg.Column(action)]
    ]
    return col

def main():
    file_name = sys.argv[1]
    layout = [
        [sg.Text("Name:")],
        [sg.Input(key='Name')],
        [sg.Text("Alphabet:")],
        [sg.Input(key='Alphabet')],
        [sg.Text("Blank:")],
        [sg.Input(key='Blank')],
        [sg.Text("States:")],
        [sg.Button("Add"), sg.Button("Submit"), sg.Button("Cancel")],
        [sg.Input(key='-INPUT0-')],
    ]

    window = sg.Window("Input fill", layout)
    input_counter = 1
    my_dict = dict()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Cancel":
            break
        if event == "Add":
            new_input = [sg.Input(key=f'-INPUT{input_counter}-')]
            window.extend_layout(window, [new_input])
            input_counter += 1
        if event == "Submit":
            my_dict['name'] = values['Name']
            my_dict['alphabet'] = [i for i in values['Alphabet']]
            my_dict['blank'] = values['Blank']
            my_dict['states'] = [values[f'-INPUT{i}-'] for i in range(input_counter)]
            my_dict['states'].append("HALT")
            break
    window.close()
    my_dict['finals'] = ["HALT"]

    # Second window

    def getTabLayout(state_dict):
        mytab = lambda state : sg.Tab(state, [[sg.Button(f"ADDto{state}"), sg.Table(values=[], headings=["read", "to_state","write", "action"], auto_size_columns=True, key=f'TABLE{state}')]])
        tab_layout = [
            [mytab(state) for state in state_dict["states"] if state != "HALT"],
        ]
        layout2 = [
            [sg.TabGroup(tab_layout, key="tabGroup")],
        ]
        return layout2

    layout2 = [
        create_col(my_dict["alphabet"], my_dict["states"], ["LEFT", "RIGHT"]),
        getTabLayout(my_dict),
    ]

    window2 = sg.Window("States fill", layout2)

    transitions = {}
    my_dict['initial'] = my_dict['states'][0]
    data = {i:[]  for i in my_dict['states']}

    while True:
        event, values = window2.read()
        if event == sg.WINDOW_CLOSED or event == "Cancel":
            break
        if event == f"ADDto{values['tabGroup']}":
            data[f'{values["tabGroup"]}'].append([values['read'], values['state'], values['write'], values['action']])
            window2[str(f'TABLE{values["tabGroup"]}')].update(values=data[f'{values["tabGroup"]}'])

    window2.close()

    my_dict["transitions"] = dict()
    for state, transitions in data.items():
        if state == 'HALT':
            continue
        if state in my_dict['states']:
            my_dict['transitions'][state] = [
                {'read': t[0], 'to_state': t[1], 'write': t[2], 'action': t[3]} for t in transitions
            ]
        else:
            my_dict['transitions'][state] = [
                {'read': t[0], 'to_state': t[1], 'write': t[2], 'action': t[3]} for t in transitions
            ]
    with open(f'{file_name}.json', 'w') as json_file:
        json.dump(my_dict, json_file, indent=4)




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 <name.py> <name_of_file> ")
        exit(1)
    main()