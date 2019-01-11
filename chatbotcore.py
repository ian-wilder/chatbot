from nltk.chat.util import Chat, reflections
import re
import random

# === This is the extension code for the NLTK library ===
#        === You dont have to understand it ===

class ContextChat(Chat):
    def respond(self, str):
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

    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try: user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                while user_input[-1] in "!.": user_input = user_input[:-1]    
                print(self.respond(user_input))

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
        r'(quit)',
        ["Goodbye."],
    ],
    [
        r'(.*)',
        ["I'm sorry. I'm not sure I can help with that."],
    ],
]

if __name__ == "__main__":
    print("Hi, I'm Admissions Bot. It's a pleasure to meet you.")
    print("What can I help you with?")
    chat = ContextChat(pairs, reflections)
    chat.converse()
    
