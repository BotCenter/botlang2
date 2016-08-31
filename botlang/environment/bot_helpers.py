# -*- coding: utf-8 -*-


def validate_rut(rut):

    try:
        rut_dv = rut.lower().replace('.', '').strip().split('-')
        rut_str = rut_dv[0]
        dv_str = rut_dv[1]

        series = [2, 3, 4, 5, 6, 7]
        dv = 11 - sum(
            [
                series[index % 6] * int(digit)
                for index, digit in enumerate(reversed(rut_str))
            ]
        ) % 11

        if dv == 10:
            return dv_str == 'k'
        return int(dv_str) % 11 == dv

    except:
        return False


validate_in_options = """
[function (options)
    (define simplified-options (map plain options))
    (function (option)
        (member? simplified-options option)
    )
]
"""

ask_with_retries = """
[function
    (
        data
        message
        validation-fun
        input-id
        next-node-fun
        max-retries
        retry-msg
        exit-result-fun
    )
    (define validate-input-node
        [bot-node (data)
            (define to-validate [input-message])
            (define is-valid? [validation-fun to-validate])
            (if is-valid?
                (next-node-fun (put data input-id to-validate))
                (begin
                    (define counter (get data '__retries-counter))
                    (if (>= counter max-retries)
                        (exit-result-fun data)
                        (node-result
                            (put data '__retries-counter (+ counter 1))
                            retry-msg
                            validate-input-node
                        )
                    )
                )
            )
        ]
    )
    (node-result
        (put data '__retries-counter 0)
        message
        validate-input-node
    )
]
"""


def option(key, description, node):
    return [key, description, node]


node_option_selection = """
[function
    (
        data
        message
        list-of-options
    )
    [define options-message
        (reduce
            (fun (acc next) (append acc "\n" next))
            (map
                [fun (option)
                    (append
                        (str (get option 0))
                        ") "
                        (get option 1)
                    )
                ]
                list-of-options
            )
        )
    ]
    [define failure-node
        (bot-node (data)
            (node-result
                data
                (append
                    "Opción inválida. Elija entre:\n\n"
                    options-message
                )
                selection-node
            )
        )
    ]
    [define selection-node
        (bot-node (data)
            [define input-option (input-message)]
            [define find-fun
                (fun (option) [equal? (str (get option 0)) input-option])
            ]
            [define selected-option (find find-fun list-of-options)]
            (if (nil? selected-option)
                (failure-node data)
                ((get selected-option 2) data)
            )
        )
    ]
    (node-result
        data
        (append message "\n\n" options-message)
        selection-node
    )
]
"""

node_binary_selection = """
[function
    (
        data
        initial-message
        choose-node-message
        yes-node
        no-node
    )
    [define choose-node-message (append choose-node-message " (si/no)")]
    [define selection-node
        (bot-node (data)
            (if (equal? (plain [input-message]) "si")
                (yes-node data)
                (if (equal? (plain [input-message]) "no")
                    (no-node data)
                    (node-result
                        data
                        (append
                            "Opción inválida.\n\n"
                            choose-node-message
                        )
                        selection-node
                    )
                )
            )
        )
    ]
    (node-result
        data
        (append
            initial-message
            "\n\n"
            choose-node-message
        )
        selection-node
    )
]
"""


class BotHelpers(object):

    @classmethod
    def load_on_dsl(cls, dsl_instance):

        return cls.add_code_definitions_to_dsl(
            cls.add_primitives_to_dsl(dsl_instance)
        )

    @classmethod
    def add_primitives_to_dsl(cls, dsl_instance):

        dsl_instance.environment.add_primitives({
            'validate-rut': validate_rut,
            'option': option
        })
        return dsl_instance

    @classmethod
    def add_code_definitions_to_dsl(cls, dsl_instance):

        return dsl_instance.add_code_definition(
            'ask-with-retries', ask_with_retries
        ).add_code_definition(
            'in-options', validate_in_options
        ).add_code_definition(
            'node-selection', node_option_selection
        ).add_code_definition(
            'node-yes-no', node_binary_selection
        )
