import wolframalpha
import checking as num
import webbrowser
import requests
from bs4 import BeautifulSoup
import re
from gtts import gTTS
import playsound
import os
import weather as wt
import string
import random
import jokes as jk
import day
import time
import youtube
import socket


def voice_output_calculator(answer):
    if answer == 'None':
        audiocreated = gTTS(text=f'Sorry, your term did not bring up any calculation result. Please try again',
                            lang='en', slow=False)
    elif answer == 'Error':
        audiocreated = gTTS(text=f"Sorry, your term did not bring up any result. Try simplifying the question.",
                            lang='en', slow=False)
    elif 'playing a video' in answer or 'playing a music' in answer:
        audiocreated = gTTS(text=f"{answer}")
    elif (len(answer) > 10 and not re.match(r'\s*(\d+)\s*', answer)):
        audiocreated = gTTS(text=f"{answer}, {num.randomize}", lang='en', slow=False)
    else:
        for i in answer:
            if i in string.digits:
                audiocreated = gTTS(text=f"The answer is {answer}", lang='en', slow=False)
                break
            else:
                aftermath_text = num.after_search[answer]
                audiocreated = gTTS(text=f"Here are what I found. {aftermath_text}", lang='en', slow=False)
                break
    a = random.randint(1, 999)
    audiocreated.save(f'tts_temp-{a}.mp3')
    playsound.playsound(f'tts_temp-{a}.mp3')
    os.remove(f'tts_temp-{a}.mp3')


def basic_tasks(usr_input):
    def voice(usrinput):
        audiocreated = gTTS(text=f"{usrinput}", lang='en', slow=False)
        audiocreated.save('test.mp3')
        playsound.playsound('test.mp3')
        os.remove('test.mp3')

    if 'what can you do' in usr_input:
        text = f"Hello {socket.gethostname()}, I am still in development. I can search the web, open Windows's pre-installed desktop apps, " \
               "make list, make an alarm, and many more! I will be here to assist you."
        print(text)  # will return the text to be displayed on the GUI after it's finished.
        voice(text)
        return text  # note to self -> this return will be used to display the text in the GUI

    elif 'who are you' in usr_input or 'what is your name' in usr_input:
        text = f"Hello {socket.gethostname()}, I am Wolf. Nice to meet you!"
        print(text)  # will return the text to be displayed on the GUI after it's finished.
        voice(text)
        return text  # note to self -> this return will be used to display the text in the GUI

    elif 'what is my name' in usr_input:
        text = f'I recognize you as {socket.gethostname()}. I hope I spelled your name correctly ...'
        print(text)
        voice(text)
        return text

    elif 'tell me a joke' in usr_input:
        text = jk.jokes()
        print(text)
        voice(text)
        return text

    return ''


def output(userinput):
    rawinput = userinput

    try:
        # I separated the basic_tasks and the search function to ease the management of the codes
        # it was confusing as heck before I split them into their own respective functions.
        init = basic_tasks(userinput)
        if init != '':
            return None, init
        else:
            pass

        # I also separated the weather input so that it's easier to manage
        weather_check = wt.check_userinput(userinput)
        if weather_check[0] >= 3:
            this_list = wt.weather(weather_check)
            new_string = f'The current weather of {this_list[0]}, {this_list[1]} is {this_list[5]}, with the temperature of {this_list[2]}°C/{this_list[3]}°F'
            print(this_list)
            print(new_string)
            return wt.voice_output_weather(new_string), this_list
        else:
            pass

        # also the time
        check_time = day.check_userinput(userinput)
        if type(check_time) == str:
            voice_asis = day.voice_output_time(check_time)
            return None, voice_asis
        else:
            if check_time >= 2:
                time = day.day_now()
                print(time[0])
                return None, time
            else:
                pass

        # splitting the input to make it easier to manage.
        userinput = userinput.split()
        print(userinput)

        # checking whether the international_number keys is in userinput or not
        def check_input(userinput):
            for items in userinput:
                if items in num.websites:
                    return False
                else:
                    pass
            for keys in num.international_number.keys():
                if keys in userinput:
                    return True
                else:
                    pass
            return False

        # checking whether the international_number values is in userinput or not
        def check_input_2(userinput):
            for items in userinput:
                if items in num.websites:
                    return False
                else:
                    pass
            for values in num.international_number.values():
                for digits in userinput:
                    for each_digit in digits:
                        if each_digit == str(values):
                            return True
                        else:
                            pass
            return False

        # checking whether the international_operands item is in userinput or not
        def check_input_3(userinput):
            for items in userinput:
                if items in num.websites:
                    return False
                else:
                    pass
            for operand in num.international_operands:
                for operand_2 in userinput:
                    if operand_2 == operand:
                        return True
                    else:
                        pass
            return False

        # for calculating result inputted by the user using the wolfram API
        if check_input_3(userinput) and check_input(userinput) or check_input_3(userinput) and check_input_2(userinput):
            try:
                calculation = ''
                # this for loop is to re-construct the items inside the split 'userinput' into a new string,
                # wolfram doesn't accept list
                for items in userinput:
                    calculation += items + ' '
                app_id = 'AH3H6J-X2E9J7GRV3'
                client = wolframalpha.Client(app_id)
                res = client.query(calculation)
                answer = next(res.results).text
                return voice_output_calculator(answer), f'the answer is {answer}'
            except:
                return voice_output_calculator(
                    'None'), f'Sorry, your term did not bring up any calculation result. Please try again.'

        elif 'who' in userinput or 'what' in userinput or 'define' in userinput:
            try:
                # i am going to use web-scraping using the BeautifulSoup module in this if statement so it can act as a
                # quick explanation to the user if they're lazy enough to read on the web.
                search = ''
                if len(userinput) > 1:
                    for contents in userinput:
                        if contents == 'what':
                            search = 'define '
                        elif contents == 'who':
                            search = 'who is '
                        elif contents == 'is':
                            pass
                        elif contents == 'if':
                            search = 'what happens if '
                        elif contents == 'happened' or contents == 'happen' or contents == 'happens':
                            search = 'what happened '
                        elif contents == 'can':
                            search = 'what can '
                        elif contents == 'will':
                            search = f'{userinput[0]} will '
                        else:
                            search += f'{contents}+'

                    # request to google using 'request' module > extract it to a html using beautifulsoup module > prettify it
                    google_search = requests.get(f'https://www.google.com/search?q={search}')
                    soup = BeautifulSoup(google_search.text, 'html.parser')
                    soup = soup.prettify()
                else:

                    # the only difference with the above section is that if the user only inputted one keyword, it will go
                    # to this section, otherwise it will go to above section
                    search = userinput[-1]
                    google_search = requests.get(f'https://www.google.com/search?q={search}')
                    soup = BeautifulSoup(google_search.text, 'html.parser')
                    soup = soup.prettify()

                # this is where the webscraping comes into play
                scraping = re.findall(r'<div class="BNeawe s3v9rd AP7Wnd">\n\s*(.*?)\n', soup)
                final_scrap = ''
                for items in scraping:

                    # if statement to filter the result. It will pick the first longest sequence of letters.
                    if len(items) > 50:

                        # re to determine a special occasion (ex. title of a person on the first half of the sentence).
                        # it is to prevent the program for cutting the sentence in that title of the person.
                        special_occs = re.findall(r'[A-Z][a-z]{0,3}\.', items)
                        if special_occs == []:
                            special_occs = '. '
                        else:
                            pass
                        final_scrap += items[:items.find('. ', items.index(special_occs[-1]) + 2)] + '.' + '\n'
                        break
                    else:
                        pass

                # calling the gTTS module which will read the scrapped text from the web
                webbrowser.open_new_tab(f'https://www.google.com/search?q={search}')
                return voice_output_calculator(final_scrap), final_scrap
            except:
                voice_output_calculator('Error')
                return None, 'Sorry, your term did not bring up any result. Try simplifying the question.'

        elif userinput[0] or userinput[1] or userinput[2] or userinput[-1] or userinput[-2] in num.predictions:
            search = ''
            web = 'google'
            browse = ''
            search_check = None
            if 'youtube' and 'music' in userinput or 'yt' and 'music' in userinput:
                browse = num.searches['youtube']['music']
                web = 'youtube music'
                if 'play' in userinput:
                    search_check = 'music'
            elif 'youtube' in userinput or 'yt' in userinput:
                browse = num.searches['youtube']['youtube']
                web = 'youtube'
                if 'play' in userinput:
                    search_check = 'youtube'
            elif 'stack' and 'overflow' in userinput or 'stackoverflow' in userinput:
                browse = num.searches['stackoverflow']
                web = 'stackoverflow'
            else:
                for input in num.searches.keys():
                    if input in userinput:
                        web = input
                        browse = num.searches[web]
                        break
                    else:
                        continue
                browse = num.searches[web]
            for content in num.yt_case:
                if content in userinput:
                    userinput.remove(content)
            for prediction in num.predictions:
                if prediction in userinput:
                    if userinput[0] == 'is':
                        pass
                    else:
                        userinput = list(filter((prediction).__ne__, userinput))
                else:
                    pass
            for final_items in userinput:
                search += f'{final_items}+'
            if search_check == 'youtube':
                search_new = ''
                for term in search.split('+'):
                    search_new += f'{term} '
                yt = youtube.playonyt(search)
                voice_output_calculator(f'{yt} {search_new}')
            elif search_check == 'music':
                search_new = ''
                for term in search.split('+'):
                    search_new += f'{term} '
                ytmusic = youtube.play_yt_music(search)
                voice_output_calculator(f'{ytmusic} {search_new}')
            else:
                webbrowser.open_new_tab(f'{browse}{search}')
                voice_output_calculator(web)

        else:
            """if 'google' in userinput: userinput.remove('google')
            print(userinput)
            search = ''
            for items in userinput:
                search += f'{items}+'
            webbrowser.open_new_tab(f'https://www.google.com/search?q={search}')"""
            pass

        """
            elif userinput[0] == 'search':
                for i in num.preposition:
                    if i in userinput:
                        userinput.remove(i)
                search = ''
                if 'for' in userinput: userinput.remove('for')
                print(userinput)
                if 'youtube' in userinput:
                    for i in range(userinput.index('search') + 1, len(userinput) - 1):
                        search += f'{userinput[i]}+'
                    webbrowser.open_new_tab(f'https://www.youtube.com/results?search_query={search}')
                else:
                    for i in range(userinput.index('search') + 1, len(userinput)):
                        search += f'{userinput[i]}+'
                    web = userinput[-1]
                    if web == 'yahoo':
                        webbrowser.open_new_tab(f'https://search.yahoo.com/search?p={search}')
                    elif web == 'bing':
                        webbrowser.open_new_tab(f'https://www.bing.com/search?q={search}')
                    else:
                        if 'google' in web:
                            webbrowser.open_new_tab(f'https://www.google.com/search?q={search}')
                        else:
                            webbrowser.open_new_tab(f'https://www.google.com/search?q={search}{web}')
                            
            elif 'youtube' in userinput:
                search = ''
                if 'search' in userinput:
                    if 'for' in userinput: userinput.remove('for')
                    if len(userinput[userinput.index('search') + 1:]) > 1:
                        print(userinput[userinput.index('search'):])
                        for i in range(userinput.index('search') + 1, len(userinput)):
                            search += f'{userinput[i]}+'
                        webbrowser.open_new_tab(f'https://www.youtube.com/results?search_query={search}')
                    else:
                        search = userinput[-1]
                        webbrowser.open_new_tab(f'https://www.youtube.com/results?search_query={search}')
                else:
                    webbrowser.open_new_tab(f'https://www.youtube.com/')
                """
    except:
        pass


"""
time.sleep(1)
while 1:
    input_temp = input('enter your question')
    output(input_temp)
# """