from nltk.chat.util import Chat, reflections
import re
import random
import requests
import ast

# === This is the extension code for the NLTK library ===
#        === You dont have to understand it ===

class ContextChat(Chat):
    def respond(self, str, language):
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response

                if callable(resp):
                    resp = resp(match.groups())
                
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'

                payload = {'key': 'trnsl.1.1.20190117T132741Z.eb29b4e0109365dc.2bbd22b38b491ee6da903085ed4e941c6ab051d0', 'text': resp, 'lang':'en-'+language}
                r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=payload)
                output = ast.literal_eval(r.text)
                resp = output.get("text")[0]
                return resp

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos+1:pos+2])
            response = response[:pos] + \
                self._substitute(match.group(num + 1)) + \
                response[pos+2:]
            pos = response.find('%')
        return response

    def converse(self, language, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try: user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                payload = {'key': 'trnsl.1.1.20190117T132741Z.eb29b4e0109365dc.2bbd22b38b491ee6da903085ed4e941c6ab051d0', 'text': user_input, 'lang':language+'-en'}
                r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=payload)
                output = ast.literal_eval(r.text)
                user_input = output.get("text")[0]
                while user_input[-1] in "!.": user_input = user_input[:-1]    
                print(self.respond(user_input, language))

# === Your code should go here ===

shopping_list = []

def add_to_list(item):
    '''
    This function adds an item to the shopping list.
    If given item is already in the list it returns
    False, otherwise it returns True
    '''
    if item in shopping_list:
        return False
    else:
        shopping_list.append(item)
        return True

pairs = [
    # answer to questions
    [
        r'(where)(.*)(school|asw)(.*)', 
        [lambda matches: 'We are located right on the edge of Warsaw, next to the small town of Konstancin-Jeziorna. Our street adress is Warszawska 202 05-520 Konstancin-Jeziorna, Poland. Here is a link to our school on maps. http://bit.ly/aswmap'],
    ],
    [
        r'(.*)(how)(.*)(much)(.*)(tuition|tuiton|tution)(.*)',
        [lambda matches: 'Tuition varies from grade to grade. The chart can be found here: http://bit.ly/aswadmissionscost'],
    ],
    [
        r'(.*)(when)(.*)(school)(.*)(year)(.*)',
        [lambda matches: 'The school year varies from year to year, but starts in late August, and goes through mid June. We do have a three week Christmas break, as well as several week long breaks throughout the year.'],
    ],
    [
        r'(.*)(how)(.*)(apply)(.*)',
        [lambda matches: 'Please download and follow the step-by- step User Guide to Admissions 2019-2020 for specific information on each step: \n> http://bit.ly/ASWAdmissionsGuide <\nIf you have any questions or queries about the application process, please contact the Admissions team.'],
    ],
        [
        r'(.*)(when)(.*)(apply)(.*)',
        [lambda matches: 'Annual application process: Applications for the 2019-2020 school year can be submitted starting from September 2018. Families applying for mid-year enrolment can also apply one year ahead.\nIf you are interested in enrolling your child in more than 12 months from now, please complete our online inquiry form and we will contact you when applications open: http://bit.ly/ASWinquire\nMost of the spaces are allocated by April but openings may become available in the months after that.'],
    ],
    [
        r'(.*)(bus)(.*)',
        [lambda matches: 'A door-to-door bus service is available for a fee for students living in the wider Warsaw area. At the end of the school day buses depart right after school and again at the end of after-school activities.'],
    ],
    [
        r'(.*)(uniform)(.*)',
        [lambda matches: 'At ASW students do not wear a school uniform but are required to dress appropriately for school. Middle and High School students have a Physical Education uniform.'],
    ],
    [
        r'(.*)(placement test)(.*)',
        [lambda matches: 'Students applying for Grades 6-12 whose mother tongue is not English or who have not been using English as their primary academic language, will be asked to complete an English language test. Tests in math and foreign language may also be administered to determine appropriate placement in these courses.'],
    ],
    [
        r'(.*)(medical)(.*)',
        [lambda matches: 'Each newly admitted student must have a medical check-up prior to enrolling. The Physical Examination form must be completed by a qualified, licensed health care provider. The check-up should be done no more than 12 months prior to the student’s start date. It must include proof of a Tuberculosis screening and a copy of the child’s vaccination record. A student is not authorised to start school unless the completed Physical Examination form has been submitted to ASW.'],
    ],
    [
        r'(.*)(boarding)(.*)',
        [lambda matches: 'ASW does not offer boarding. Students enrolled at ASW must reside with their parents or a legal guardian.'],
    ],
    [
        r'(.*)(meals)(.*)',
        [lambda matches: 'Fresh, healthy meals and snacks are offered in our cafeteria for a fee. Students may also bring their own lunch from home.'],
    ],
    [
        r'(.*)(how)(.*)(long)(.*)(day)(.*)',
        [lambda matches: 'School starts at 8:30 and ends at 15:30. For grades 11 and 12, the school day starts at 8:20 and finishes at 15:20. On Wednesdays, all students start school at 9:30 and end at 15:30. There are a variety of after-school activities at the end of the school day.'],
    ],
    [
        r'(.*)(after school|extra|activities)(.*)',
        [lambda matches: 'In order to see the list of after school activities visit the school website: https://www.aswarsaw.org/learning/athletics'],
    ],
    [
        r'(.*)(accept)(.*)(special)(.*)(needs)(.*)',
        [lambda matches: 'ASW welcomes students with a wide range of abilities and interests. Each division, Elementary, Middle and High School, has a Learning Support Program. The program is designed to provide assistance to struggling learners and students who have an identified mild to moderate learning disability or learning difference that requires educational support. ASW currently does not have the personnel capacity to support children with intense learning disabilities. Students with significant social-emotional difficulties who need a special learning environment may not be eligible for admission.'],
    ],
    [
        r'(.*)(application)(.*)(fee)(.*)(refundable|refund)(.*)',
        [lambda matches: 'In short, no. The application fee is a non-refundable administrative fee, charged to cover the costs of processing your child’s application, including testing and interviewing if required.'],
    ],
    [
        r'(.*)(different)(year)(.*)(transition)(.*)',
        [lambda matches: 'Each student’s record is considered carefully. Normally, students who have just completed a grade level (American system equivalent) in their home country will not be promoted to the next grade level mid-year at ASW as this would mean skipping months or even a full semester of that year’s work and leading to gaps in learning. Additionally, students who in future years return to an alternative calendar are often significantly impacted even more. Review of a student’s full record, relevant assessments, and other pertinent information may be used in making an alternative placement, if the body of evidence supports that decision after being reviewed by school administration.'],
    ],

    # conversation stuff
    [
        r'(.*)(hello|hi|greetings|sup|howdy)(.*)', 
        [lambda matches: 'Hello, what can I help you with?'],
    ],
    [
        r'(.*)(what)(.*)(your)(.*)(name)(.*)', 
        [lambda matches: 'I\'m Admissions Bot. It\'s a pleasure to meet you.'],
    ],
    [
        r'(.*)(what)(.*)(you)(.*)(do)(.*)', 
        [lambda matches: 'I am a bot intended to answer your questions about admission. Go ahead, ask me something about admissions.'],
    ],
    [
        r'(.*)(are)(.*)(you)(.*)(alive)(.*)', 
        [lambda matches: 'It depends on what you count as alive.'],
    ],
    [
        r'(.*)(are)(.*)(you)(.*)(real)(.*)', 
        [lambda matches: 'It depends on what you count as real.'],
    ],
    [
        r'(.*)(are)(.*)(you)(.*)(bot|robot)(.*)', 
        [lambda matches: 'Indeed I am, and my purpose is to help you find out more about admissions.'],
    ],
    [
        r'(.*)(find|learn|ask)(.*)(admissions|admission)(.*)', 
        [lambda matches: "That's what I'm here for, feel free to ask me anything about admissions."],
    ],
    [
        r'(.*)(how)(.*)(quit|exit|leave)(.*)', 
        [lambda matches: 'In order to quit simply type: quit.'],
    ],
    [
        r'(.*)(how)(.*)(contact)(.*)(admissions|people)(.*)', 
        [lambda matches: 'In order to contact the good people at the admissions office please email admissions@aswarsaw.org or call +48 22 702 8500.'],
    ],

    # quit and error, they must be last
    [
        r'(quit)',
        ["Goodbye."],
    ],
    [
        r'(.*)',
        ["I'm sorry, I'm not sure I understand. Make sure you didn't misspell something."],
    ],
]

if __name__ == "__main__":
    while True:
        print("1) Polski") # polish
        print("2) 한국어") # korean
        print("3) 中文") # chinese
        print("4) Español") # spanish
        print("5) Deutsch") # german
        print("6) Français") # french
        print("7) English") # english
        translate = input("Please choose the number by the language you would like.\n>")
        try:
            translate = int(translate)
        except ValueError:
            translate = input("Please only type a number.\n>")
        else:
            if translate == 1:
                language = "pl"
                break
            elif translate == 2:
                language = "ko"
                break
            elif translate == 3:
                language = "zh"
                break
            elif translate == 4:
                language = "es"
                break
            elif translate == 5:
                language = "de"
                break
            elif translate == 6:
                language = "fr"
                break
            elif translate == 7:
                language = "en"
                break
            else:
                print("{} is not a number you can choose.".format(translate))
    greeting = "Hi, I'm Admissions Bot. It's a pleasure to meet you."
    payload = {'key': 'trnsl.1.1.20190117T132741Z.eb29b4e0109365dc.2bbd22b38b491ee6da903085ed4e941c6ab051d0', 'text': greeting, 'lang':'en-'+language}
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=payload)
    output = ast.literal_eval(r.text)
    greeting = output.get("text")[0]
    print(greeting)
    greeting2 = "What can I help you with?"
    greeting = "Hi, I'm Admissions Bot. It's a pleasure to meet you."
    payload = {'key': 'trnsl.1.1.20190117T132741Z.eb29b4e0109365dc.2bbd22b38b491ee6da903085ed4e941c6ab051d0', 'text': greeting2, 'lang':'en-'+language}
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=payload)
    output = ast.literal_eval(r.text)
    greeting2 = output.get("text")[0]
    print(greeting2)
    chat = ContextChat(pairs, reflections)
    chat.converse(language)
