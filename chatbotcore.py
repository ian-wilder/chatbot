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
        r'(quit)',
        ["Goodbye."],
    ],
]

if __name__ == "__main__":
    print("Hi, I'm Admissions Bot. It's a pleasure to meet you.")
    print("What can I help you with?")
    chat = ContextChat(pairs, reflections)
    chat.converse()
    
