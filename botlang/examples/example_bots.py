# -*- coding: utf-8 -*-
class ExampleBots(object):

    bank_bot_code = r"""
[define log-nodes-trace
    (function (nodes-path)
        (list)
    )
]

[define add-step
    (function (data step-id)
        [define nodes-path (get data "nodes-path")]
        (put data "nodes-path" (extend nodes-path step-id))
    )
]

[define pop-step
    (function (data)
        [define nodes-path (get data "nodes-path")]
        (put data "nodes-path" (init nodes-path))
    )
]

[define reset-path
    (function (data)
        [define nodes-path (get data "nodes-path")]
        (put data "nodes-path" (list))
    )
]

[define log-path
    (function (data)
        [define nodes-path (get data "nodes-path")]
        (log-nodes-trace nodes-path)
    )
]

[define derive-ticket
    (function (data)
        [define nodes-path (get data "nodes-path")]
        (log-nodes-trace nodes-path)
        (log-event (append (join "_" nodes-path) "_DERIVED"))
        (log-derive-ticket (get data "ticket-open-time"))
        (terminal-node "ASSIGN_TO_CM")
    )
]

[define close-ticket
    (function (data)
        (log-path data)
        (terminal-node "CLOSE_TICKET")
    )
]

[defun format-quick-replies (first-message quick-replies)
    (make-dict (list
        (cons "text" first-message)
        (list "quick_replies"
            (map
                (function (r)
                    (make-dict (list
                        (cons "content_type" "text")
                        (cons "title" r)
                        (cons "payload" r)
                    ))
                )
                quick-replies
            )
        )
    ))
]

[defun format-quick-replies-with-images (first-message quick-replies)
    (make-dict (list
        (cons "text" first-message)
        (list "quick_replies"
            (map
                (function (r)
                    (make-dict (list
                        (cons "content_type" "text")
                        (cons "title" (get r 0))
                        (cons "payload" (get r 0))
                        (cons "image_url" (get r 1))
                    ))
                )
                quick-replies
            )
        )
    ))
]

[defun ask-location (message)
    (make-dict (list
        (cons "text" message)
        (list "quick_replies"
            (list
                (make-dict (list
                    (cons "content_type" "location")
                ))
            )
        )
    ))
]

[define format-image
    (function (image-url)
        (make-dict (list
            (cons "attachment"
                (make-dict (list
                    (cons "type" "image")
                    (cons "payload" (make-dict (list
                        (cons "url" image-url)
                        (cons "is_reusable" #t)
                    )))
                ))
            )
        ))
    )
]

[define format-location
    (function (info)
        [define name (get info 0)]
        [define latitude (str (get info 1))]
        [define longitude (str (get info 2))]
        [define address (get info 3)]
        [define map-img-url (append
            "https://maps.googleapis.com/maps/api/staticmap?size=640x336&maptype=roadmap&markers="
            latitude "," longitude
        )]
        [define gmaps-url (append
            "https://www.google.cl/maps/search/"
            latitude "," longitude
        )]
        (make-dict (list
            (cons "attachment"
                (make-dict (list
                    (cons "type" "template")
                    (cons "payload"
                        (make-dict (list
                            (cons "template_type" "generic")
                            (list "elements" (list
                                (make-dict (list
                                    (cons "title" name)
                                    (cons "subtitle" address)
                                    (cons "image_url" map-img-url)
                                    (list "buttons" (list
                                        (make-dict (list
                                            (cons "type" "web_url")
                                            (cons "url" gmaps-url)
                                            (cons "title" "Abrir Mapa")
                                            (cons "webview_height_ratio" "full")
                                        ))
                                    ))
                                ))
                            ))
                        ))
                    )
                ))
            )
        ))
    )
]

(define THUMBS_UP_EMOJI
    "https://emojipedia-us.s3.amazonaws.com/thumbs/160/facebook/65/thumbs-up-sign_1f44d.png"
)
(define THUMBS_DOWN_EMOJI
    "https://emojipedia-us.s3.amazonaws.com/thumbs/160/facebook/65/thumbs-down-sign_1f44e.png"
)

[define was-answer-useful-msg
    (function (data)
        (format-quick-replies-with-images
            (translate data "TE_SIRVIO?")
            (list
                (list "Sí" THUMBS_UP_EMOJI)
                (list "No" THUMBS_DOWN_EMOJI)
            )
        )
    )
]

[define answer-useful-response-node
    (bot-node (data)
        [define response (plain (input-message))]
        (cond
            [(match? "(no)|(nada)" response)
                (node-result
                    (no-entendi-reset data)
                    (list
                        (translate data "DESPEDIDA_NEGATIVA")
                    )
                    (begin
                        (log-event "TERMINO_INSATISFECHO")
                        (close-ticket data)
                    )
                )
            ]
            [else
                (node-result
                    (no-entendi-reset data)
                    (list
                        (translate data "DESPEDIDA")
                    )
                    (begin
                        (close-ticket data)
                    )
                )
            ]
        )
    )
]

[define was-answer-useful?
    (function (data)
        (node-result
            data
            (was-answer-useful-msg data)
            answer-useful-response-node
        )
    ) 
]

[define back-to-menu?-response-node
    (bot-node (data)
        [define response (plain (input-message))]
        (cond
            [(match? "(si\s?.*)|(afirmativo)" response)
                (begin
                    (log-path data)
                    (node-result
                        (no-entendi-reset (reset-path data))
                        (list
                            (translate data "QUE_OTRA_COSA_NECESITAS?")
                            (entry-menu data)
                        )
                        entry-menu-response-node
                    )
                )
            ]
            [(match? "(no)|(nada)" response)
                (was-answer-useful? data)
            ]
            [else
                (no-entendi-node
                    data
                    (list (translate data "NO_ENTENDI") (back-to-menu-msg data))
                    back-to-menu?-response-node
                )
            ]
        )
    )
]

[defun back-to-menu-msg (data)
    (format-quick-replies
        (translate data "ALGO_MAS?")
        (list "Sí" "No")
    )
]

[define back-to-menu?
    (function (data previous-messages)
        (node-result
            data
            (extend
                previous-messages
                (back-to-menu-msg data)
            )
            back-to-menu?-response-node
        )
    ) 
]

[define block-card-node
    (bot-node (data)
        [define msg (plain (input-message))]
        (cond
            [(match? ".*credito.*" msg)
                (back-to-menu?
                    (no-entendi-reset (add-step data "CREDITO"))
                    (list
                        (translate data "SIGUIENTES_PASOS")
                        (translate data "BLOQUEAR_CREDITO_PASO_1")
                        (translate data "BLOQUEAR_CREDITO_PASO_2")
                        (translate data "BLOQUEAR_CREDITO_PASO_3")
                        (format-image (translate data "BLOQUEAR_CREDITO_IMAGEN"))
                        (translate data "BLOQUEAR_CREDITO_PASO_4")
                        (translate data "BLOQUEAR_CREDITO_PASO_5")
                        (translate data "BLOQUEAR_CREDITO_PASO_6")
                    )
                )
            ]
            [(match? ".*debito.*" msg)
                (back-to-menu?
                    (no-entendi-reset (add-step data "DEBITO"))
                    (list
                        (translate data "SIGUIENTES_PASOS")
                        (translate data "BLOQUEAR_DEBITO_PASO_1")
                        (translate data "BLOQUEAR_DEBITO_PASO_2")
                        (translate data "BLOQUEAR_DEBITO_PASO_3")
                    )
                )
            ]
            [else
                (no-entendi-node
                    data
                    (list (translate data "OPCION_INVALIDA") (tarjeta-a-bloquear? data))
                    block-card-node
                )
            ]
        )
    )
]

[defun tarjeta-a-bloquear? (data)
    (format-quick-replies
        (translate data "TARJETA_A_BLOQUEAR?")
        (list "T. Crédito" "T. Débito")
    )
]

[define emergencies-response-node
    (bot-node (data)
        [define msg (plain (input-message))]
        (cond
            [(match? "(.*desbloque.*)|(.*clave.*)" msg)
                (back-to-menu?
                    (no-entendi-reset (add-step data "CLAVE"))
                    (list
                        (translate data "SIGUIENTES_PASOS")
                        (translate data "INGRESAR_A_BANCO_EN_LINEA")
                        (format-image (translate data "BANCO_EN_LINEA_IMAGEN"))
                        (translate data "INGRESA_DATOS_SIGUE_PASOS")
                    )
                )
            ]
            [(match? ".*tarjeta.*" msg)
                (node-result
                    (no-entendi-reset (add-step data "TARJETA"))
                    (tarjeta-a-bloquear? data)
                    block-card-node
                )
            ]
            [(match? "(.*auto.*)|(.*siniestro.*)" msg)
                (back-to-menu?
                    (no-entendi-reset (add-step data "AUTO"))
                    (list
                        (translate data "SIGUIENTES_PASOS")
                        (translate data "SINIESTRO_AUTO_PASO_1_TITULO")
                        (translate data "SINIESTRO_AUTO_PASO_1_CUERPO")
                        (translate data "SINIESTRO_AUTO_PASO_1_CUERPO2")
                        (translate data "SINIESTRO_AUTO_PASO_2_TITULO")
                        (translate data "SINIESTRO_AUTO_PASO_2_CUERPO1")
                        (translate data "SINIESTRO_AUTO_PASO_2_CUERPO2")
                    )
                )
            ]
            [else
                (no-entendi-node
                    data
                    (list
                        (translate data "NO_ENTENDI")
                        (emergencies-menu (translate data "EMERGENCIAS_MANEJADAS") data)
                    )
                    emergencies-response-node
                )
            ]
        )
    )
]

[define emergencies-menu
    (function (heading data)
        (list
            heading
            "DESBLOQUEO_CLAVE"
            "BLOQUEO_TARJETA"
            "SINIESTRO_AUTOMOTRIZ"
        )
    )
]

[define cuenta-response-node
    (bot-node (data)
        [define msg (plain (input-message))]
        (cond
            [(match? "(si)|(afirmativo)|(claro)|(exacto)" msg)
                (back-to-menu?
                    (no-entendi-reset (add-step data "OTRO-BANCO"))
                    (list
                        (translate data "SIGUIENTES_PASOS")
                        (translate data "CUENTA_CLIENTE_OTRO_BANCO_1")
                        (translate data "CUENTA_CLIENTE_OTRO_BANCO_2")
                        (translate data "CUENTA_CLIENTE_OTRO_BANCO_3")
                    )
                )
            ]
            [(match? "(no)|(negativo)|(nones)" msg)
                (node-result
                    (no-entendi-reset (add-step data "BCI"))
                    (translate data "CUENTA_CLIENTE_BCI")
                    (derive-ticket data)
                )
            ]
            [else
                (no-entendi-node
                    data
                    (list (translate data "NO_ENTENDI") (cuenta-menu data))
                    cuenta-response-node
                )
            ]
        )
    )
]

[defun cuenta-menu (data)
    (format-quick-replies
        (translate data "CLIENTE_OTRO_BANCO?")
        (list "Sí" "No")
    )
]

[define entry-menu-response-node
    (bot-node (data)
        [define msg (plain (input-message))]
        (cond
            [(match? ".*emergencia.*" msg)
                (node-result
                    (no-entendi-reset (add-step data "EMERGENCIA"))
                    (emergencies-menu (translate data "EMERGENCIAS_CABECERA") data)
                    emergencies-response-node
                )
            ]
            [(match? ".*cuenta.*" msg)
                (node-result
                    (no-entendi-reset (add-step data "CUENTA"))
                    (cuenta-menu data)
                    cuenta-response-node
                )
            ]
            [else
                (no-entendi-node
                    data
                    (list (translate data "NO_ENTENDI") (entry-menu data))
                    entry-menu-response-node
                )
            ]
        )
    )
]

[defun no-entendi-reset (data) (put data "NO_ENTENDI_COUNTER" 0)]

[define NO_ENTENDI_RETRY_LIMIT 1]

[define no-entendi-node
    (function (data messages next-node)
        (define no-entendi-counter (get data "NO_ENTENDI_COUNTER"))
        (if (>= no-entendi-counter NO_ENTENDI_RETRY_LIMIT)
            (node-result
                data
                (translate data "EJECUTIVO_TE_CONTACTARA")
                (derive-ticket data)
            )
            (node-result
                (put data "NO_ENTENDI_COUNTER" (+ no-entendi-counter 1))
                messages
                next-node
            )
        )
    )
]

[define entry-menu
    (function (data)
        (make-dict (list
            (cons "attachment"
                (make-dict (list
                    (cons "type" "template")
                    (cons "payload"
                        (make-dict (list
                            (cons "template_type" "generic")
                            (list "elements" (list
                                (make-dict (list
                                    (cons "title" (translate data "MENU_ENTRADA_TITULO"))
                                    (cons "image_url" (translate data "MENU_ENTRADA_IMAGEN"))
                                    (list "buttons" (list
                                        (make-dict (list
                                            (cons "title" (translate data "MENU_ENTRADA_EMERGENCIAS"))
                                            (cons "type" "postback")
                                            (cons "payload" "emergencias")
                                        ))
                                        (make-dict (list
                                            (cons "title" (translate data "MENU_ENTRADA_CUENTA"))
                                            (cons "type" "postback")
                                            (cons "payload" "cuenta")
                                        ))
                                    ))
                                ))
                            ))
                        ))
                    )
                ))
            )
        ))
    )
]

[defun translate (data identifier) identifier] 

[define entry-node
    (bot-node (input-data)
        [define data
            (put
                (no-entendi-reset input-data)
                "nodes-path"
                (list)
            )
        ]
        [define msg (input-message)]
        (cond
            [(match? ".*emergencia.*" msg)
                (node-result
                    (add-step data "EMERGENCIA")
                    (emergencies-menu (translate data "EMERGENCIAS_CABECERA") data)
                    emergencies-response-node
                )
            ]
            [(match? ".*cuenta.*" msg)
                (node-result
                    (add-step data "CUENTA")
                    (cuenta-menu data)
                    cuenta-response-node
                )
            ]
            [else
                (node-result
                    data
                    (list
                        (translate data "ENTRY_MESSAGE")
                        (entry-menu data)
                    )
                    entry-menu-response-node
                ) 
            ]
        )
    )
]

entry-node"""