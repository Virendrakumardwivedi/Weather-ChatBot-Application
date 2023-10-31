# from flask import Flask, request, jsonify
# import requests
# import openai
# import json

# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app) 

# # Replace these keys with your actual API keys
# WEATHER_KEY = 'aba0359b16180c5a0a561032fe8c3883'

# # Configure OpenAI
# openai.api_key = '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'

# # Example dummy function hard coded to return the same weather
# # In production, this could be your backend API or an external API
# def get_current_weather(location):
#     base_url = "https://api.openweathermap.org/data/2.5/weather"
#     params = {
#         "q": location,
#         "appid": WEATHER_KEY,
#         "units": "metric",  # Request temperature in Celsius
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         data = response.json()

#         if response.status_code == 200:
#             # Extract relevant weather information from the response
#             temperature = data["main"]["temp"]
#             weather_description = data["weather"][0]["description"]
#             humidity = data["main"]["humidity"]

#             return json.dumps({
#                 "location": location,
#                 "temperature": temperature,
#                 "description": weather_description,
#                 "humidity": humidity,
#                 "information": data,
#                 "explain": "explain it like a news forecast",
#             })
#         else:
#             return {"error": f"Failed to fetch weather data for {location}"}

#     except requests.exceptions.RequestException as e:
#         return {"error": f"Request error: {e}"}
    
# @app.route('/get_weather', methods=['POST'])
# def chat():
#     user_message = request.json.get("content", "")  # Get the user's message from the request
#     messages = [{"role": "user", "content": user_message}]
#     # data = request.json
#     # if data.get("content"):
#     #     messages = [
#     #         {"role": "user", "content": data["content"]}
#     #     ]
#     functions = [
#             {
#                 "name": "get_current_weather",
#                 "description": "Get the current weather in a given location",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "location": {
#                             "type": "string",
#                             "description": "The city and state, e.g. New Delhi, India",
#                         },
#                     },
#                     "required": ["location"],
#                 },
#             }
#         ]
#     response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#             functions=functions,
#             function_call="auto"
#         )
#     response_message = response["choices"][0]["message"]
#     if response_message.get("function_call"):
#         available_functions = {
#         "get_current_weather": get_current_weather,
#     }  # only one function in this example, but you can have multiple
#     function_name = response_message["function_call"]["name"]
#     function_to_call = available_functions[function_name]
#     function_args = json.loads(response_message["function_call"]["arguments"])
#     function_response = function_to_call(
#         location=function_args.get("location"),
#         )
            
#             # available_functions = {
#             # "get_current_weather": get_current_weather,
#             # }
            
#             # function_name = response_message["function_call"]["name"]
#             # function_args = json.loads(response_message["function_call"]["arguments"])
#             # ##location = function_args.get("location")
         
            
#     messages.append(response_message)  # extend conversation with assistant's reply
#     messages.append(
#         {
#             "role": "function",
#             "name": function_name,
#             "content": function_response,
#         }
#     )  # extend conversation with function response
#     second_response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo-0613",
#         messages=messages,
#     ) 
#     # get a new response from GPT where it can see the function response
#     print("success")
#     return json.dumps({"message": second_response["choices"][0]["message"]["content"]})
        

# if __name__ == "__main__":
#     app.run(debug=True)
##-------------------------------------------------------------



import openai
import json
from flask import Flask,request,jsonify,render_template
import requests




app = Flask(__name__)

# openai.api_key = "OPENAI_KEY"  # Set your OpenAI API key here
# WEATHER_KEY = "WEATHER_API_KEY"  # Set your weather API key here

openai.api_key = 'submit your API here...!'
WEATHER_KEY = 'aba0359b16180c5a0a561032fe8c3883'

# openai.apiKey = api_key

@app.route('/')
def home():
    return render_template('index.html')

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": WEATHER_KEY,
        "units": "metric",  # Request temperature in Celsius
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            # Extract relevant weather information from the response
            temperature = data["main"]["temp"]
            weather_description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]

            return json.dumps({
                "location": location,
                "temperature": temperature,
                "description": weather_description,
                "humidity": humidity,
                "information": data,
                "explain": "explain it like a news forcast",
            })
        else:
            return {"error": f"Failed to fetch weather data for {location}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Request error: {e}"}

@app.route("/get_weather", methods=["POST"])
def chat():
    # Step 1: send the conversation and available functions to GPT
    # messages = [{"role": "user", "content":""}]
    user_message = request.json.get("content", "")  # Get the user's message from the request
    messages = [{"role": "user", "content": user_message}]
   
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]
    print(response_message)



    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        
        
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            location=function_args.get("location")
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return jsonify({"message": second_response["choices"][0]["message"]["content"]})

    return jsonify({"message": response_message["content"]})

    # def app():
    #      message = chat()
    #      print(message)

    # app()
if __name__ == '__main__':
    app.run(debug=True)