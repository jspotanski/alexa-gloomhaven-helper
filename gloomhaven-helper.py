#------------------------------Part1--------------------------------
# In this part we define a list that contains the player names, and 
# a dictionary with player biographies
Rule_LIST = [
    "poison",
    "stun",
    "retire"
  ]
  
Rule_DEFINITION = {
  "poison": "All enemies add +1 to all of their attacks on the affected figure",
  "stun": "Cannot do any ability or use Items (immediate effect). Character must do Long Rest or discard two Hand cards on their next turn",

}

Flow_LIST = [
    "newCharacter",
    "make a new character",
    "retire",
    # "levelUp", 
    # "applyEnhancement",
    # "donate",
    # "buyAndSell",
    # "retire",
    # "roadAndCityEvents"
]


Flow_WALKTHROUGH = {
    "make a new character":
    [
        "Pick an unlocked class (can’t play duplicate classes in same scenario) [p6]",
        "Pick a starting level. May start at any level up to the city’s Prosperity Level",
        "Record character name and level in a new Character Sheet",
        "Receive Gold = 15 x (L+1) (L = character’s level)",
        "Receive XP = minimum required for level (as per Character Sheet)",
        "Choose 1 Perk for every character the player has retired. If 1 player controlling 2 characters, count each character’s retirement lineage separately [p48]",
        "Draw 2 random Personal Quest cards and choose one, shuffling the other to the deck (if deck is empty, no quest is received).",
        "A player may keep their Personal Quest secret or public as desired [FAQ]","Create Active Card Pool with Level 1 and Level X Ability Cards",
        "Follow the Level Up a Character steps below for the remaining levels"
    ],
    "retire":
    [
        "end", 
        "the character"
    ]
}

#------------------------------Part2--------------------------------
# Here we define our Lambda function and configure what it does when 
# an event with a Launch, Intent and Session End Requests are sent. # The Lambda function responses to an event carrying a particular 
# Request are handled by functions such as on_launch(event) and 
# intent_scheme(event).
def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()

#------------------------------Part3--------------------------------
# Here we define the Request handler functions
def on_start():
    print("Session Started.")

def on_launch(event):
    onlunch_MSG = "Welcome to Gloomhaven Helper.  Ask me about rules like: " + ', '.join(map(str, Rule_LIST)) + " by saying how does " + Rule_LIST[1] + " work?"
    reprompt_MSG = "Do you want to hear more about a particular rule?"
    card_TEXT = "Ask about a rule"
    card_TITLE = "Choose a rule"
    return output_json_builder_with_reprompt_and_card(onlunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")
#-----------------------------Part3.1-------------------------------
# The intent_scheme(event) function handles the Intent Request. 
# Since we have a few different intents in our skill, we need to 
# configure what this function will do upon receiving a particular 
# intent. This can be done by introducing the functions which handle 
# each of the intents.
def intent_scheme(event):
    
    intent_name = event['request']['intent']['name']

    if intent_name == "getRule":
        return ruleDefinition(event)
    elif intent_name == "getFlow":
        return flowWalkthrough(event)    
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)
#---------------------------Part3.1.1-------------------------------
# Here we define the intent handler functions
def ruleDefinition(event):
    rule=event['request']['intent']['slots']['ruleName']['value']
    rule_list_lower=[w.lower() for w in Rule_LIST]
    if rule.lower() in rule_list_lower:
        reprompt_MSG = "Do you want to hear more about a particular rule?"
        card_TEXT = "You've picked " + rule.lower()
        card_TITLE = "You've picked " + rule.lower()
        return output_json_builder_with_reprompt_and_card(Rule_DEFINITION[rule.lower()], card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        wrongname_MSG = "I don't know about that rule."
        reprompt_MSG = "Do you want to hear more about a different rule?"
        card_TEXT = "Try again."
        card_TITLE = "Unknown rule."
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def flowWalkthrough(event):
    flow=event['request']['intent']['slots']['flowName']['value']
    flow_list_lower=[w.lower() for w in Flow_LIST]
    if flow.lower() in flow_list_lower:
        reprompt_MSG = "Do you want to hear more about a particular flow?"
        card_TEXT = "You've picked " + flow.lower()
        card_TITLE = "You've picked " + flow.lower()
        return output_json_builder_with_reprompt_and_card(Flow_WALKTHROUGH[flow.lower()], card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        wrongname_MSG = "I don't know about that flow."
        reprompt_MSG = "Do you want to hear more about a different flow?"
        card_TEXT = "Try again."
        card_TITLE = "Unknown flow."
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def stop_the_skill(event):
    stop_MSG = "Thank you. Bye!"
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
    
def assistance(event):
    assistance_MSG = "You can choose among these rules: " + ', '.join(map(str, Flow_LIST))
    reprompt_MSG = "Do you want to hear more about a particular rule?"
    card_TEXT = "You've asked for help."
    card_TITLE = "Help"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Do you want to hear more about a particular rule?"
    card_TEXT = "I don't know about that rule."
    card_TITLE = "Unknown rule"
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
#------------------------------Part4--------------------------------
# The response of our Lambda function should be in a json format. 
# That is why in this part of the code we define the functions which 
# will build the response in the requested format. These functions
# are used by both the intent handlers and the request handlers to 
# build the output.
def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    if isinstance(text_dict['text'], str):
        text_dict['text'] = text_body
    elif isinstance(text_dict['text'], list):
        text_dict['text'] =  '. '.join(map(str, text_dict['text']))
    else:
        text_dict['text'] = "Unrecognized types"
    print (type(text_dict['text']))
    return text_dict

def ssml_builder(text_body):
    ssml_dict = {}
    ssml_dict['type'] = "SSML"

    return ssml_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
    
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict    

def response_field_builder_with_reprompt_and_card(outputSpeech_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeech_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeech_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeech_text, card_text, card_title, reprompt_text, value)
    return response_dict