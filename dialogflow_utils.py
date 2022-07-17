from google.cloud import dialogflow


def get_dialogflow_reply(session, session_client, text, language_code='ru-RU'):
    text_input = dialogflow.TextInput(text=text,
                                      language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )
    return (response.query_result.fulfillment_text,
            response.query_result.intent.is_fallback)
