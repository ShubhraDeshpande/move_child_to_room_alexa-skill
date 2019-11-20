import logging
import ask_sdk_core.utils as ask_utils
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

spaces ={"hufflepuff":[], "azkaban":[], "slytherin":[]}

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "where do you want to move the child?"
        reprompt_text = "slytherin or hufflepuff?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

# class HasBirthdayLaunchRequestHandler(AbstractRequestHandler):
#     """Handler for launch after they have set their birthday"""

#     def can_handle(self, handler_input):
#         # extract persistent attributes and check if they are all present
#         attr = handler_input.attributes_manager.persistent_attributes
#         attributes_are_present = ("year" in attr and "month" in attr and "day" in attr)

#         return attributes_are_present and ask_utils.is_request_type("LaunchRequest")(handler_input)

#     def handle(self, handler_input):
#         attr = handler_input.attributes_manager.persistent_attributes
#         year = attr['year']
#         month = attr['month'] # month is a string, and we need to convert it to a month index later
#         day = attr['day']

#         # TODO:: Use the settings API to get current date and then compute how many days until user's bday
#         # TODO:: Say happy birthday on the user's birthday

#         speak_output = "Welcome back it looks like there are X more days until your y-th birthday."
#         handler_input.response_builder.speak(speak_output)

#         return handler_input.response_builder.response

class GetLocationIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetLocationIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        roomName = slots["roomName"].value
        

        attributes_manager = handler_input.attributes_manager

        birthday_attributes = {
            "roomName": roomName,
            
            
        }

        attributes_manager.persistent_attributes = birthday_attributes
        attributes_manager.save_persistent_attributes()
        if roomName in spaces:
            speak_output = 'great! who do you want to move to {roomName}'.format(roomName=roomName)
        else:
            speak_output = "oh! we do not have {roomName} at our center! Try with other room".format(roomName=roomName)
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class GetChildNameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
    # extract persistent attributes and check if they are all present
        attr = handler_input.attributes_manager.persistent_attributes
        attributes_are_present = ("roomName" in attr )
        return attributes_are_present and ask_utils.is_intent_name("GetChildNameIntent")(handler_input)

    def handle(self, handler_input):
        attr = handler_input.attributes_manager.persistent_attributes
        roomName = attr['roomName']
        
        slots = handler_input.request_envelope.request.intent.slots
        fname = slots["fname"].value
        lname = slots["lname"].value
        
        #updating children in dict
        
        spaces[roomName].append(fname)
        attributes_manager = handler_input.attributes_manager

        birthday_attributes = {
            "roomName": roomName,
            "spaces": spaces,
            
            
        }

        attributes_manager.persistent_attributes = birthday_attributes
        attributes_manager.save_persistent_attributes()
        

        # TODO:: Use the settings API to get current date and then compute how many days until user's bday
        # TODO:: Say happy birthday on the user's birthday

        speak_output = "cool! I will get {fname} moved ,  by the way now we have {no} children in {roomName}, do you want to move more children? ".format(fname=fname , roomName=roomName, no= len(spaces[roomName]))
        handler_input.response_builder.speak(speak_output)

        return handler_input.response_builder.response

class MoveMoreChildrenIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("MoveMoreChildrenIntent")(handler_input)
        
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        affirm = slots["affirm"].value
        

        # attributes_manager = handler_input.attributes_manager

        # birthday_attributes = {
        #     "number": number,
            
        # }

        # attributes_manager.persistent_attributes = birthday_attributes
        # attributes_manager.save_persistent_attributes()
        if affirm.lower() == "yes" or affirm.lower() == "yes please" or affirm.lower() == "sure":
            speak_output = "cool! what is the name of next child?"
        else:
            speak_output = "awesome! we have moved children, please check in the app"
        handler_input.response_builder.speak(speak_output)

        return handler_input.response_builder.response
    

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

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
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


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
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

# sb.add_request_handler(HasBirthdayLaunchRequestHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetLocationIntentHandler())
sb.add_request_handler(GetChildNameIntentHandler())
sb.add_request_handler(MoveMoreChildrenIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
