# -*- coding: utf-8 -*-
class ExampleBots(object):

    dog_bot_code = """
        (define ask-rut
            [function (data ask-rut-message next-node-fun)
                (define validate-rut-node
                    [bot-node (data)
                        (define rut [input-message])
                        (define valid-rut? [validate-rut rut])
                        (if valid-rut?
                            (next-node-fun (put data 'rut rut))
                            (node-result
                                data
                                "Rut inválido. Intente nuevamente."
                                validate-rut-node
                            )
                        )
                    ]
                )
                (node-result
                    data
                    ask-rut-message
                    validate-rut-node
                )
            ]
        )

        (define has-dog-node
            (bot-node (data)
                (define valid-answer
                    [or (equal? [input-message] "si") (equal? [input-message] "no")]
                )
                (if (not valid-answer)
                    (node-result
                        data
                        "Debe responder si o no. ¿Tiene perro?"
                        has-dog-node
                    )
                    [if (equal? [input-message] "si")
                        (node-result
                            (put data 'dog #t)
                            (append "Wauf, " (get data 'name) "!")
                            end-node
                        )
                        (node-result
                            (put data 'dog #f)
                            (append "Miau, " (get data 'name) " :3")
                            end-node
                        )
                    ]
                )
            )
        )

        (bot-node (data)
            (node-result
                data
                "Bienvenido a Botcenter! ¿Con quién tengo el gusto de hablar?"
                (bot-node (data)
                    (define name [input-message])
                    [ask-rut
                        (put data 'name name)
                        (append "Mucho gusto " name ". Indíqueme su RUT, por favor.")
                        (function (data)
                            (node-result
                                data
                                "Muchas gracias. ¿Tiene perro? (si/no)"
                                has-dog-node
                            )
                        )
                    ]
                )
            )
        )
    """