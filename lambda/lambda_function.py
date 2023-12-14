# -*- coding: utf-8 -*-

import logging, os
import json
import requests
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from utils import s3, Person, Room
import dialogs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

UPDATE_URL = '<URL HERE>'

# SKILL STATES 
# HOME: Está en el inicio y no ha comentado que quiere empezar
# CONFIGURING_GAME: Ya indicaron que iban a empezar y están en el proceso de registro en la app
#                   esperando la confirmación de inicio
# TURN_IN_PROGRESS: El turno ya inicio y están en el proceso de adivinar
# TURN_ENDING: Fin del turno, donde se muestra en la app y se espera a que avisen que empiece el siguiente
# ROUND_ENDING: Fin de una ronda, se pregunta si quieren jugar una nueva

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["skill_state"] = "HOME"
        
        speak_output = dialogs.WELCOME
        reprompt_output = dialogs.WELCOME_REPROMPT
        return (    
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_output)
                .response
                
        )

class StartGameIntentHandler(AbstractRequestHandler):
    """Handler for Start Game Intent. 
        It's used when:
        1.- Initial game configuration, while waiting for all the players to log in the web.
        2.- Then in the web, when the game choose the first pair of players and starts the first round.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        skill_state = session_attr.get('skill_state')
        return ask_utils.is_intent_name("StartGameIntent")(handler_input) and \
                skill_state!='ROUND_ENDING' and skill_state!='TURN_IN_PROGRESS'

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        session_attr = handler_input.attributes_manager.session_attributes
        
        skill_state = session_attr.get('skill_state')
        # Case when the game starts from scratch, it came from HOME.
        # Here we generate and share the pin and wait until players say that have entered the room.
        if skill_state=='HOME':
            room = Room().create_room()
            session_attr['room_pin'] = room['pin']
            session_attr['count_rounds'] = 1
            speak_output = dialogs.FIRST_ROUND.format(pin=room['pin'])
            session_attr['skill_state'] = 'CONFIGURING_GAME'
            
            return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(dialogs.FIRST_ROUND_REPROMPT.format(pin=room['pin']))
                .response
            )
            
        # This case is when the players notify that everyone has entered the app
        # and the turn is assigned
        elif skill_state=='CONFIGURING_GAME':
            room = Room().start_game(session_attr['room_pin'])
            
            if (room):
                requests.get(UPDATE_URL+session_attr["room_pin"]+"/update")
                player_mimic = room["players"][room["player_mimic"]]
                player_guess = room["players"][room["player_guess"]]
                session_attr["current_card"] = room["current_card"]
                
                speak_output = dialogs.TURN_CONFIGURE.format(p_guess=player_guess["name"], p_mimic=player_mimic["name"])
                reprompt_output = dialogs.TURN_CONFIGURE_REPROMPT.format(p_guess=player_guess["name"])
                session_attr['skill_state'] = 'TURN_IN_PROGRESS'
            else:
                speak_output = dialogs.ROUND_NOT_READY.format(pin=session_attr['room_pin'])
                reprompt_output = dialogs.ROUND_NOT_READY.format(pin=session_attr['room_pin'])
                
            return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_output)
                .response
            )
        elif skill_state=='TURN_ENDING':
            room = Room().next_couple(session_attr["room_pin"])
            requests.get(UPDATE_URL+session_attr["room_pin"]+"/update")
            player_mimic = room["players"][room["player_mimic"]]
            player_guess = room["players"][room["player_guess"]]
            session_attr["current_card"] = room["current_card"]
            
            speak_output = dialogs.MIDDLE_TURN.format(p_guess=player_guess["name"], p_mimic=player_mimic["name"])
            reprompt_output = dialogs.MIDDLE_TURN_REPROMPT.format(p_guess=player_guess["name"])
            session_attr['skill_state'] = 'TURN_IN_PROGRESS'
            return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_output)
                .response
            )

class AskClueIntentHandler(AbstractRequestHandler):
    """Handler for Ask Clue Intent.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (ask_utils.is_intent_name("AskClueIntent")(handler_input) or \
                    ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)) and \
                (session_attr.get('skill_state')=='TURN_IN_PROGRESS')

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # Look for the current card in the room and get the clue
        session_attr = handler_input.attributes_manager.session_attributes
        
        speak_output = session_attr["current_card"]["clue"]
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class TriviaAnswerIntentHandler(AbstractRequestHandler):
    """Handler for Trivia Answer Intent. It is validated if the answer is correct.
    Then it is validated if we have to go to the next turn,
    the next round or if it is the end of the game.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return ask_utils.is_intent_name("TriviaAnswerIntent")(handler_input) and \
                session_attr.get('skill_state')=='TURN_IN_PROGRESS'

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        print("Current card", str(session_attr))
        current_names = session_attr["current_card"]["synonyms"]
        slots = handler_input.request_envelope.request.intent.slots
        current_answer = slots["persona"].value
        
        # It is validated if there are more turns or rounds
        # Can change to turn_ending or round_ending depending on the situation
        # It is the last turn of the current round

        # Check if the answer is correct
        if (current_answer in current_names):
            room = Room().add_points(session_attr['room_pin'], 5)
            requests.get(UPDATE_URL+session_attr["room_pin"]+"/show_card")
            
            if room['turn']==0:
                speak_end = dialogs.ROUND_ENDED.format(round=session_attr['count_rounds'])
                session_attr['skill_state'] = 'ROUND_ENDING'
                print("End of next round")
                
            else:
                speak_end = dialogs.TURN_ENDED
                session_attr['skill_state'] = 'TURN_ENDING'
                print("End of next turn")
            speak_output = dialogs.CORRECT_TRIVIA.format(woman=session_attr["current_card"]["description-alexa"],
                                                            final=speak_end)
        else:
            room = Room().get(session_attr['room_pin'])
            requests.get(UPDATE_URL+session_attr["room_pin"]+"/show_card")
            
            if room['turn']==0:
                speak_end = dialogs.ROUND_ENDED.format(round=session_attr['count_rounds'])
                session_attr['skill_state'] = 'ROUND_ENDING'
                print("End of next round")
                
            else:
                speak_end = dialogs.TURN_ENDED
                session_attr['skill_state'] = 'TURN_ENDING'
                print("End of next turn")
            speak_output = dialogs.INCORRECT_TRIVIA.format(woman=session_attr["current_card"]["description-alexa"],
                                                            final=speak_end)
            
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_end)
                .response
            )

class YesIntentHandler(AbstractRequestHandler):
    """Handler for Yes Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input) and \
                (session_attr.get('skill_state')=='ROUND_ENDING' or session_attr.get('skill_state')=='TURN_ENDING')

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        session_attr = handler_input.attributes_manager.session_attributes
        skill_state = session_attr.get('skill_state')
        
        room = Room().next_couple(session_attr["room_pin"])
        requests.get(UPDATE_URL+session_attr["room_pin"]+"/update")
        player_mimic = room["players"][room["player_mimic"]]
        player_guess = room["players"][room["player_guess"]]
        session_attr["current_card"] = room["current_card"]
        
        if skill_state=='ROUND_ENDING':
            # New pairs are calculated
            # A summary of the points can be given
            session_attr['count_rounds'] += 1
            
            speak_output = dialogs.WANT_OTHER_ROUND.format(p_guess=player_guess["name"], p_mimic=player_mimic["name"])
            session_attr['skill_state'] = 'TURN_IN_PROGRESS'
            
        elif skill_state=='TURN_ENDING':
            speak_output = dialogs.MIDDLE_TURN.format(p_guess=player_guess["name"], p_mimic=player_mimic["name"])
            
            woman_msg = dialogs.WOMAN_INFO.format(woman=session_attr["current_card"]["description-alexa"])
            reprompt_output = woman_msg + dialogs.MIDDLE_TURN_REPROMPT
            session_attr['skill_state'] = 'TURN_IN_PROGRESS'
        
        return (
        handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

class NoIntentHandler(AbstractRequestHandler):
    """Handler for No Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input) and \
                (session_attr.get('skill_state')=='ROUND_ENDING' or session_attr.get('skill_state')=='TURN_ENDING')

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        session_attr = handler_input.attributes_manager.session_attributes
        
        score, players = Room().get_winner(session_attr['room_pin'])
        requests.get(UPDATE_URL+session_attr["room_pin"]+"/end_game")
        
        if (len(players) == 1):
            speak_output = dialogs.ONE_WINNER.format(winner=players[0], score=score)
        else:
            aux_answer = players[0]
            for p in players[1:-1]:
                aux_answer += ", " + p
            aux_answer += " y " + players[-1]
            
            speak_output = dialogs.SEVERAL_WINNERS.format(score=score, players=aux_answer)
        
        session_attr['skill_state'] = 'HOME'
        
        return (
        handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input) 

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = dialogs.RULES

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = dialogs.CANCEL_ALL

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = dialogs.FALLBACK
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class IrrelevantRequestHandler(AbstractRequestHandler):
    """Irrelevant Node
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return True

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr = handler_input.attributes_manager.session_attributes
        skill_state = session_attr['skill_state']
        
        if skill_state=='HOME':
            speak_output = dialogs.WELCOME_IRRELEVANT
            
        elif skill_state=='CONFIGURING_GAME':
            speak_output = dialogs.FIRST_ROUND_IRRELEVANT
            
        elif skill_state=='TURN_IN_PROGRESS':
            speak_output = dialogs.TURN_IRRELEVANT
        elif skill_state=='TURN_ENDING':
            speak_output = dialogs.TURN_ENDED_IRRELEVANT
        elif skill_state=='ROUND_ENDING':
            speak_output = dialogs.ROUND_ENDED_IRRELEVANT
        else:
            speak_output = dialogs.EXCEPTION
        
        
        logger.error(exception, exc_info=True)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        
        session_attr = handler_input.attributes_manager.session_attributes
        skill_state = session_attr['skill_state']
        
        if skill_state=='HOME':
            speak_output = dialogs.WELCOME_IRRELEVANT
            
        elif skill_state=='CONFIGURING_GAME':
            speak_output = dialogs.FIRST_ROUND_IRRELEVANT
            
        elif skill_state=='TURN_IN_PROGRESS':
            speak_output = dialogs.TURN_IRRELEVANT
        elif skill_state=='TURN_ENDING':
            speak_output = dialogs.TURN_ENDED_IRRELEVANT
        elif skill_state=='ROUND_ENDING':
            speak_output = dialogs.ROUND_ENDED_IRRELEVANT
        else:
            speak_output = dialogs.EXCEPTION

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CacheResponseForRepeatInterceptor(AbstractResponseInterceptor):
    """Cache the response sent to the user in session.

    The interceptor is used to cache the handler response that is
    being sent to the user. This can be used to repeat the response
    back to the user, in case a RepeatIntent is being used and the
    skill developer wants to repeat the same information back to
    the user.
    """
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["recent_response"] = response

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(StartGameIntentHandler())
sb.add_request_handler(AskClueIntentHandler())
sb.add_request_handler(TriviaAnswerIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IrrelevantRequestHandler())
# sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_response_interceptor(CacheResponseForRepeatInterceptor())

lambda_handler = sb.lambda_handler()