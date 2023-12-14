# Agregar sonido de opening
WELCOME = ("<audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_intro_01\"/><say-as interpret-as=\"interjection\">buenas</say-as>."
			" Ingresaste a Mujeres Ocultas. El juego donde encontrarás mujeres que han impactado al mundo. Conócelas a medida que vas compartiendo entre amigos."
			" <break time=\"0.7s\" /> Antes de iniciar, cada uno debe ingresar a la web: mujeresocultas.com,"
			" y estar preparados.<break time=\"0.8s\"/> ¿Qué quieres hacer? ¿Empezar a jugar, o conocer las reglas del juego?."
            )

WELCOME_IRRELEVANT = ("<say-as interpret-as=\"interjection\">uups</say-as>. No te entendí. ¿Qué quieres hacer? ¿Empezar a jugar, o conocer las reglas del juego?."
                      )

WELCOME_REPROMPT = ("¿Aún no sabes qué quieres hacer?.  Mujeres Ocultas hará que te diviertas mientras aprendes sobre mujeres que han impactado el mundo. <break time=\"0.8s\"/> Elige una opción: empezar a jugar, o conocer las reglas del juego."
                    )

# Sonido de espera
FIRST_ROUND = ("¡Manos a la obra!. Cada participante o equipo debe ingresar el código de la sala y su nombre en la"
				" web: mujeresocultas.com. <break time=\"0.4s\"/>"
				" El código es <say-as interpret-as=\"digits\">{pin}</say-as>. <break time=\"0.8s\"/> Puedes decirme 'listo' cuando todos los participantes hayan ingresado."
				" <break time=\"0.4s\"/> <audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_countdown_loop_64s_full_01\"/>"
                 )

FIRST_ROUND_IRRELEVANT = ("<say-as interpret-as=\"interjection\">uups</say-as>. No te entendí. Puedes decirme 'listo' cuando todos los participantes hayan ingresado.")

# Sonido de error
# Sonido de espera (final)
ROUND_NOT_READY = ("<audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_negative_response_01\"/><say-as interpret-as=\"interjection\">uups</say-as>."
					" parece que no estaban dentro de la sala. Deben ser al menos dos participantes en: mujeresocultas.com con"
                    " el código <say-as interpret-as=\"digits\">{pin}</say-as>."
                    " Puedes decirme 'listo' cuando todos los participantes hayan ingresado."
                    "<break time=\"0.4s\"/> <audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_countdown_loop_64s_full_01\"/>"
                    )

# Sonido de espera
FIRST_ROUND_REPROMPT = ("Recuerden que deben ingresar todos a la web: mujeresocultas punto com con el código"
						" de sala <say-as interpret-as=\"digits\">{pin}</say-as>. <break time=\"0.2s\"/> Estaré esperando.<break time=\"0.2s\"/> Puedes "
						"decirme 'listo' cuando todos los participantes hayan ingresado <audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_countdown_loop_32s_full_01\"/>"
                        )

# Redoble (antes de los nombres)
# Sonido de espera 1 (50 segundos)
TURN_CONFIGURE = ("<say-as interpret-as=\"interjection\">okey dokey</say-as>. Comencemos. "
					"<audio src=\"soundbank://soundlibrary/foley/amzn_sfx_clock_ticking_01\"/> {p_mimic} en tu móvil encontrarás a la mujer oculta de este turno. "
					" Deberás intentar que {p_guess} adivine y me diga quién es. {p_mimic}, ¡sin trampas! <audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_countdown_loop_64s_full_01\"/>"
					)

# Sonido de que se te acabó el tiempo
# ESTE NO VA EN LOS REMPROMPTS
WOMAN_INFO = ("Parece que alguien no hizo su tarea hoy. Se ha acabado el tiempo. {woman}")

# Tic tac
# Sonido de espera (50 segundos)
# POner nombre de guess
TURN_CONFIGURE_REPROMPT = ("<audio src=\"soundbank://soundlibrary/clocks/ticks/ticks_05\"/> ¿Es muy difícil?. {p_guess}, siempre puedes pedirme alguna pista."
							" <audio src=\"soundbank://soundlibrary/clocks/ticks/ticks_05\"/><audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_waiting_loop_30s_01\"/>"
                            )

#Cortina 
MIDDLE_TURN = ("<say-as interpret-as=\"interjection\">okey</say-as>. Es el turno de adivinar de <audio src=\"soundbank://soundlibrary/foley/amzn_sfx_clock_ticking_01\"/>"
				" {p_guess} y recibirá la información de <audio src=\"soundbank://soundlibrary/foley/amzn_sfx_clock_ticking_01\"/> {p_mimic}. {p_mimic} si miras tu móvil"
				" encontrarás a la mujer asignada e información sobre ella. ¡Sin trampas! <audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_countdown_loop_64s_full_01\"/>"
              )

# Sonido de espera
# POner nombre de guess
MIDDLE_TURN_REPROMPT = ("<audio src=\"soundbank://soundlibrary/clocks/ticks/ticks_05\"/><say-as interpret-as=\"interjection\">vaya</say-as> "
						"<say-as interpret-as=\"interjection\">vaya</say-as>... esta parece difícil. {p_guess}, puedes pedirme una pista si la necesitas. <audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_waiting_loop_30s_01\"/>"
                        )

TURN_IRRELEVANT = ("<say-as interpret-as=\"interjection\">uups</say-as>. No te entendí. ¿Necesitas una pista?")

# Sonido de felicitaciones
CORRECT_TRIVIA = ("<audio src=\"soundbank://soundlibrary/alarms/chimes_and_bells/chimes_bells_06\"/><say-as interpret-as=\"interjection\">oh sí</say-as>.<break time=\"0.2s\"/> "
					"Alguien sabe mucho de mujeres inspiradoras. ¡Respuesta correcta! {woman} {final}")

INCORRECT_TRIVIA = ("<audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_negative_response_02\"/><say-as interpret-as=\"interjection\">uups</say-as>.<break time=\"0.2s\"/> "
					"Respuesta incorrecta. Nunca es tarde para aprender algo nuevo. {woman} {final}")

ROUND_ENDED = ("<audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_positive_response_02\"/> Ya finalizamos la ronda {round}. ¿Quieren seguir a una próxima ronda?")

ROUND_ENDED_IRRELEVANT = ("<say-as interpret-as=\"interjection\">uups</say-as>. Lo siento, no te entendí. ¿Quieren seguir a una próxima ronda?")

TURN_ENDED = ("<audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_positive_response_02\"/> ¿Quieren empezar el siguiente turno?")

TURN_ENDED_IRRELEVANT = ("<say-as interpret-as=\"interjection\">uups</say-as>. Lo siento, no te entendí. ¿Quieren empezar el siguiente turno?")

# Sonido de espera
WANT_OTHER_ROUND = ("<say-as interpret-as=\"interjection\">okey dokey</say-as> <audio src=\"soundbank://soundlibrary/foley/amzn_sfx_clock_ticking_01\"/> Es el turno de que {p_mimic} intente que {p_guess} adivine a nuestra mujer oculta. "
                     " <say-as interpret-as=\"interjection\">buena suerte</say-as>.<audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_countdown_loop_64s_full_01\"/>")


# Redoble antes del ganador
ONE_WINNER = ("<audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_outro_01\"/>¡Hasta aquí llega el juego de hoy! La victoria es para {player}, con {score} puntos. <say-as interpret-as=\"interjection\">felicidades</say-as><audio src=\"soundbank://soundlibrary/human/amzn_sfx_crowd_applause_02\"/>¡Vuelvan pronto! <audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_intro_01\"/>")

SEVERAL_WINNERS = ("<audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_outro_01\"/>¡Sus deseos son órdenes! La partida de hoy estuvo reñida, tenemos un empate en el primer lugar con {score}"
					" puntos. <say-as interpret-as=\"interjection\">felicidades</say-as>. {players} <audio src=\"soundbank://soundlibrary/human/amzn_sfx_crowd_applause_02\"/>¡Vuelvan pronto! <audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_intro_01\"/>")


RULES = ("Yo seré la moderadora, por lo tanto, deben estar atentos a mis instrucciones. <break time=\"0.2s\"/> "
            "El juego es de dos o más jugadores. <break time=\"0.2s\"/> Por cada turno, escogeré a dos personas: "
            "uno tendrá que presentar y el otro adivinar. En sus móviles tendrán el rol que les he asignado por turno. "
            "<break time=\"0.2s\"/> Quien presente, describirá a la mujer oculta, pero... sin decir su nombre. <break time=\"0.2s\"/> "
            "La otra persona deberá escuchar las pistas e intentar adivinar quién es la mujer oculta. <break time=\"0.2s\"/> El resto, "
            "esperará para participar en los próximos turnos. Ambos ganan puntos por cada acierto. <break time=\"0.2s\"/> La partida la ganará "
            "quien conozca, o sepa describir mejor a la mayor cantidad de mujeres ocultas. <break time=\"0.2s\"/><say-as interpret-as=\"interjection\">buena suerte</say-as> ")

CANCEL_ALL = ("<say-as interpret-as=\"interjection\">okey dokey</say-as>. ¡Vuelvan pronto!")

FALLBACK = ("Hmm, I'm not sure. You can say Hello or Help. What would you like to do?")

FALLBACK_REPROMPT = ("Hmm, I'm not sure. You can say Hello or Help. What would you like to do?")

EXCEPTION = ("<audio src=\"soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_negative_response_01\"/><break time=\"0.2s\"/><say-as interpret-as=\"interjection\">ostras</say-as>. Algo anda mal, intenta nuevamente.")
